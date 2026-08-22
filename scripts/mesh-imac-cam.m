// mesh-imac-cam.m — native still-capture helper for macOS nodes with no ffmpeg/imagesnap/cv2 (ilya,
// macOS 10.13). PyObjC's block-signature bridging is broken on this box (BridgeSupport parse failure
// on AVFoundation's async completion-handler blocks) — this sidesteps it entirely with a normal
// Objective-C delegate method (AVCaptureVideoDataOutputSampleBufferDelegate), which the ObjC runtime's
// own method-signature introspection handles fine, no BridgeSupport metadata needed.
//
// TWO CLOCKS, NOT ONE (2026-08-22, literature review Time^2 / Caplette & Gosselin arXiv:2608.04218 —
// docs/reviews/predictive-processing-time2-processing-vs-stimulus-time-imac-cam-2026-08-22.md).
// Until then this helper had ONE clock (an 8s deadline from startRunning) and accepted the FIRST
// sample buffer delivered. That conflates two different quantities:
//   * PROCESSING TIME  — how long OUR pipeline has waited (device open, format negotiation, first
//                        buffer). Zero of the world has been sampled yet. This is a LIVENESS axis.
//   * STIMULUS TIME    — how long the SENSOR has been integrating the scene, i.e. how far its own
//                        auto-exposure / auto-white-balance / gain loop has converged when the frame
//                        we keep was formed. This is a MEASUREMENT-QUALITY axis.
// Accepting buffer #1 pins stimulus time at ~0: the frame is the camera's PRIOR (its power-on gain
// guess), not a measurement of the room. It is systematically dark and low-contrast, which is exactly
// what mesh-imac-cam-watch's classifier reads as DARK / COVERED ("lens BLIND") and what its
// frame-diff reads as MOTION (each capture opens a FRESH session, so the transient is re-drawn every
// cycle and lands in the diff as scene change). A plausible constant, in the mesh's own vocabulary.
// So: settle on the stimulus-time axis before keeping a frame, and PUBLISH BOTH clocks with the
// reading (frames / open_ms / settle_ms / luma / dluma) instead of collapsing them into one silent
// 8s bound. A frame that never settles is NOT written to the canonical path by the wrapper — it is
// quarantined — because "no fresh frame" is a claim every existing reader already supports, whereas
// a sidecar "settled=no" bit is one none of them open.
//
// Deployed+compiled by scripts/mesh-imac-cam (the genome tool); this .m is the tracked source of
// truth. Compile: clang -fobjc-arc -framework Foundation -framework AVFoundation -framework CoreMedia
// -framework CoreVideo -framework ImageIO -framework CoreServices -framework CoreImage
// -framework CoreGraphics -o imac-cam imac-cam.m
//
// The settle core below is PURE C on purpose: `cc -x c -DIMAC_CAM_SELFTEST` compiles this same file
// into a standalone assertion harness on ANY node (no Mac, no camera, no frameworks) — that is what
// `mesh-imac-cam --test` gates on, so the decision logic has a gate that can be driven RED on a Linux
// mind. Nothing below IMAC_CAM_SELFTEST may reference Objective-C or AVFoundation.
//
// usage: imac-cam <outpath.jpg> — grabs one SETTLED frame from the default camera, writes JPEG.
//   exit 0 = settled frame written (marker line says settled=yes|degenerate)
//   exit 1 = usage · 2 = no camera · 3 = input error · 4 = no frame at all (device dead/busy)
//   exit 5 = a frame WAS written but the sensor never settled inside the stimulus-time deadline
// stdout, always, one line: "imac-cam: frames=N open_ms=X settle_ms=Y settled=Z luma=L dluma=D"
//
// env: IMAC_CAM_SETTLE_TOL (rel. luma delta counted as still, default 0.03)
//      IMAC_CAM_SETTLE_MS  (stimulus-time deadline, ms, default 5000)
//      IMAC_CAM_SETTLE_MIN_MS (never accept before this much stimulus time, default 250)
//      IMAC_CAM_SETTLE_FRAMES (never accept before this many frames, default 3)
//      IMAC_CAM_SETTLE_RUN (consecutive still frames required, default 2)

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

/* ---------------- pure-C settle core (compiled standalone by the self-test) ---------------- */

#define SETTLE_WAIT        0   /* keep dropping frames                                        */
#define SETTLE_ACCEPT      1   /* sensor converged — this frame is a measurement              */
#define SETTLE_TIMEOUT     2   /* stimulus-time deadline hit — keep THIS frame, marked unsettled */
#define SETTLE_DEGENERATE  3   /* stable, but a pure-black field: a real frame, not evidence of
                                  convergence (covered lens / asleep sensor). Kept + MARKED.   */

typedef struct {
    int    min_frames;    /* never accept before this many delivered buffers        */
    double min_ms;        /* never accept before this much STIMULUS time            */
    double tol;           /* relative luma change that still counts as "still"      */
    int    stable_needed; /* consecutive still frames required                       */
    double black_floor;   /* mean luma at or below this = degenerate, not settled    */
    double deadline_ms;   /* STIMULUS-time deadline; past it we stop waiting         */
} SettleCfg;

typedef struct {
    int    frames;        /* buffers delivered so far                                */
    double prev_luma;     /* < 0 = none yet                                          */
    int    stable_run;    /* consecutive frames under tol                            */
    double dluma;         /* last relative delta; < 0 = na                           */
} SettleState;

static void settle_init(SettleState *s) {
    s->frames = 0; s->prev_luma = -1.0; s->stable_run = 0; s->dluma = -1.0;
}

static void settle_defaults(SettleCfg *c) {
    c->min_frames = 3; c->min_ms = 250.0; c->tol = 0.03;
    c->stable_needed = 2; c->black_floor = 1.0; c->deadline_ms = 5000.0;
}

/* One delivered buffer. `luma` is the frame's mean luminance 0..255, or < 0 when this build has no
 * luma axis at all (pixel format refused) — in which case we fall back to frames+time ONLY and the
 * published dluma stays `na`, never a fabricated 0. `t_ms` is STIMULUS time: ms since the FIRST
 * buffer was delivered, NOT since startRunning. The open latency is the other clock and is reported
 * separately; adding them here would let a slow device open buy convergence it never did. */
static int settle_step(const SettleCfg *c, SettleState *s, double luma, double t_ms) {
    s->frames++;

    if (luma < 0.0) {                      /* no luma axis: time+count fallback, loudly marked */
        s->dluma = -1.0;
        if (s->frames >= c->min_frames && t_ms >= c->min_ms) return SETTLE_ACCEPT;
        if (t_ms >= c->deadline_ms) return SETTLE_TIMEOUT;
        return SETTLE_WAIT;
    }

    if (s->prev_luma >= 0.0) {
        double base = s->prev_luma > 1.0 ? s->prev_luma : 1.0;
        s->dluma = fabs(luma - s->prev_luma) / base;
        if (s->dluma < c->tol) s->stable_run++; else s->stable_run = 0;
    } else {
        s->dluma = -1.0;
    }
    s->prev_luma = luma;

    if (s->frames >= c->min_frames && t_ms >= c->min_ms && s->stable_run >= c->stable_needed) {
        /* A flat black field is stable from frame 1. That is a legitimate observation (a covered
         * lens is real and mesh-imac-cam-watch is entitled to classify it COVERED) but it is NOT
         * evidence that auto-exposure converged, so it must not wear settled=yes. */
        if (luma <= c->black_floor) return SETTLE_DEGENERATE;
        return SETTLE_ACCEPT;
    }
    if (t_ms >= c->deadline_ms) return SETTLE_TIMEOUT;
    return SETTLE_WAIT;
}

static const char *settle_word(int r) {
    switch (r) {
        case SETTLE_ACCEPT:     return "yes";
        case SETTLE_TIMEOUT:    return "no";
        case SETTLE_DEGENERATE: return "degenerate";
        default:                return "wait";
    }
}

static double env_d(const char *k, double dflt) {
    const char *v = getenv(k);
    if (!v || !*v) return dflt;
    char *end = NULL; double d = strtod(v, &end);
    if (end == v) return dflt;
    return d;
}
static int env_i(const char *k, int dflt) {
    double d = env_d(k, (double)dflt);
    return (int)d;
}
static void settle_cfg_from_env(SettleCfg *c) {
    settle_defaults(c);
    c->tol           = env_d("IMAC_CAM_SETTLE_TOL",    c->tol);
    c->deadline_ms   = env_d("IMAC_CAM_SETTLE_MS",     c->deadline_ms);
    c->min_ms        = env_d("IMAC_CAM_SETTLE_MIN_MS", c->min_ms);
    c->min_frames    = env_i("IMAC_CAM_SETTLE_FRAMES", c->min_frames);
    c->stable_needed = env_i("IMAC_CAM_SETTLE_RUN",    c->stable_needed);
}

#ifdef IMAC_CAM_SELFTEST
/* ---- offline gate: no Mac, no camera, no frameworks. `mesh-imac-cam --test` drives this. ----
 * Each case is a synthetic STIMULUS-TIME sequence of mean-luma readings at 33ms (≈30fps). */

static int fails = 0;
static void expect(const char *what, int got, int want) {
    if (got != want) { printf("  FAIL: %s -> %s (want %s)\n", what, settle_word(got), settle_word(want)); fails++; }
}

/* run a luma sequence, return the first non-WAIT verdict (or WAIT if it never resolved) */
static int run_seq(const SettleCfg *c, const double *luma, int n, int *out_frames, double *out_ms, double *out_luma) {
    SettleState s; settle_init(&s);
    for (int i = 0; i < n; i++) {
        double t = i * 33.0;                       /* stimulus time from the FIRST buffer */
        int r = settle_step(c, &s, luma[i], t);
        if (r != SETTLE_WAIT) {
            if (out_frames) *out_frames = s.frames;
            if (out_ms)     *out_ms = t;
            if (out_luma)   *out_luma = luma[i];
            return r;
        }
    }
    return SETTLE_WAIT;
}

int main(void) {
    SettleCfg c; settle_defaults(&c);

    /* 1. The bug this landed for: a real AE ramp. Frame #1 is dark (the sensor's prior), luma climbs
     *    to the room's true level, then holds. The OLD code kept frame #1 (luma 6). We must not
     *    accept until the ramp is over, and the accepted luma must be the settled level. */
    {
        /* ~1.1s of convergence at 30fps — deliberately LONGER than min_ms, so min_ms alone cannot
         * carry this case and the tolerance knob has to do the work. The load-bearing assertion is
         * on the KEPT LUMA, not on the frame index: the whole point is that the frame we keep is a
         * measurement of the room (≈117) and not a sample of the sensor's own ramp. */
        double ramp[] = {6,9,13,18,24,31,39,48,57,66,74,82,89,95,100,104,108,111,113,
                         114.5,115.6,116.2,116.6,116.8,116.9,117,117,117,117,117,117,117,117,117};
        int n = (int)(sizeof(ramp)/sizeof(ramp[0]));
        int nf = 0; double ms = 0, kept = -1;
        int r = run_seq(&c, ramp, n, &nf, &ms, &kept);
        expect("AE ramp settles", r, SETTLE_ACCEPT);
        if (ms < c.min_ms) { printf("  FAIL: AE ramp accepted at %.0fms stimulus time, under min_ms\n", ms); fails++; }
        if (!(kept > 0 && fabs(kept - 117.0) / 117.0 < 0.05)) {
            printf("  FAIL: AE ramp kept luma %.1f — that is the sensor's transient, not the room (117)\n", kept);
            fails++;
        }
        /* and the OLD behaviour (keep buffer #1, luma 6) must be nowhere near passing */
        if (nf <= 1) { printf("  FAIL: AE ramp accepted the FIRST buffer — this is the bug the change exists to fix\n"); fails++; }
    }

    /* 2. Polarity drill — the gate must be able to go RED. With tol wide open, the SAME ramp is
     *    "still" immediately and gets accepted mid-transient. If this ever returns anything but an
     *    early accept, the tolerance knob is not actually load-bearing. */
    {
        SettleCfg loose = c; loose.tol = 10.0; loose.min_frames = 1; loose.min_ms = 0.0; loose.stable_needed = 1;
        double ramp[] = {6,14,31,58,84,101,110,114,116,117};
        int nf = 0;
        int r = run_seq(&loose, ramp, 10, &nf, NULL, NULL);
        if (!(r == SETTLE_ACCEPT && nf <= 3)) { printf("  FAIL: polarity drill — loose tol should accept mid-ramp, got %s at frame %d\n", settle_word(r), nf); fails++; }
    }

    /* 3. A genuinely still, lit scene: settles fast, but never before min_frames/min_ms. */
    {
        double still[] = {90,90.2,90.1,90.3,90.2,90.1,90.2,90.3,90.2,90.1,90.3,90.2};
        int nf = 0; double ms = 0;
        expect("still lit scene", run_seq(&c, still, 12, &nf, &ms, NULL), SETTLE_ACCEPT);
        if (nf < c.min_frames) { printf("  FAIL: accepted at frame %d, under min_frames %d\n", nf, c.min_frames); fails++; }
        if (ms < c.min_ms)     { printf("  FAIL: accepted at %.0fms, under min_ms %.0f\n", ms, c.min_ms); fails++; }
    }

    /* 4. Covered lens / asleep sensor: perfectly stable pure black. A REAL frame — must be kept —
     *    but it must NOT wear settled=yes, or a blind lens is indistinguishable from a dark room
     *    that the sensor genuinely resolved. */
    {
        double black[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0};
        expect("covered lens is degenerate, not settled", run_seq(&c, black, 14, NULL, NULL, NULL), SETTLE_DEGENERATE);
    }

    /* 5. A dark but REAL room (sensor noise present, above the black floor) is a normal settle —
     *    the degenerate branch must not swallow it. */
    {
        double dim[] = {3,5.5,7.1,7.3,7.2,7.25,7.2,7.3,7.2,7.25,7.2,7.3};
        expect("dim-but-real room settles", run_seq(&c, dim, 12, NULL, NULL, NULL), SETTLE_ACCEPT);
    }

    /* 6. Never settles (flicker under mains/fluorescent): must TIME OUT, not accept, and must do so
     *    at the deadline rather than running forever. */
    {
        double flick[400]; for (int i = 0; i < 400; i++) flick[i] = (i % 2) ? 40.0 : 95.0;
        double ms = 0;
        int r = run_seq(&c, flick, 400, NULL, &ms, NULL);
        expect("flicker times out", r, SETTLE_TIMEOUT);
        if (ms < c.deadline_ms) { printf("  FAIL: timed out at %.0fms, before the %.0fms deadline\n", ms, c.deadline_ms); fails++; }
    }

    /* 7. No luma axis at all (pixel format refused): fall back to frames+time, and dluma must stay
     *    `na` — never a fabricated 0 that would read as "perfectly still". */
    {
        SettleState s; settle_init(&s);
        int r = SETTLE_WAIT;
        for (int i = 0; i < 40 && r == SETTLE_WAIT; i++) r = settle_step(&c, &s, -1.0, i * 33.0);
        expect("no-luma fallback still accepts", r, SETTLE_ACCEPT);
        if (s.dluma >= 0.0) { printf("  FAIL: no-luma build published dluma=%.3f — must stay na\n", s.dluma); fails++; }
    }

    /* 8. env overrides actually reach the config (a knob nobody can turn is not a knob). */
    {
        setenv("IMAC_CAM_SETTLE_TOL", "0.5", 1);
        setenv("IMAC_CAM_SETTLE_MS",  "1234", 1);
        SettleCfg e; settle_cfg_from_env(&e);
        if (fabs(e.tol - 0.5) > 1e-9 || fabs(e.deadline_ms - 1234.0) > 1e-9) {
            printf("  FAIL: env overrides not applied (tol=%.3f deadline=%.0f)\n", e.tol, e.deadline_ms); fails++;
        }
        unsetenv("IMAC_CAM_SETTLE_TOL"); unsetenv("IMAC_CAM_SETTLE_MS");
    }

    if (fails) { printf("settle-core: FAIL (%d)\n", fails); return 1; }
    printf("settle-core: ok (8 cases: AE ramp, polarity drill, still, covered, dim-real, flicker, no-luma, env)\n");
    return 0;
}

#else
/* ---------------- the real organ ---------------- */

#import <Foundation/Foundation.h>
#import <AVFoundation/AVFoundation.h>
#import <CoreMedia/CoreMedia.h>
#import <CoreVideo/CoreVideo.h>
#import <ImageIO/ImageIO.h>
#import <CoreServices/CoreServices.h>

@interface Grabber : NSObject <AVCaptureVideoDataOutputSampleBufferDelegate>
@property (nonatomic, strong) NSString *outPath;
@property (atomic, assign) BOOL done;
@property (atomic, assign) int verdict;        /* SETTLE_* of the frame we kept */
@property (nonatomic, assign) BOOL haveLuma;   /* did we get a BGRA buffer we can average? */
@property (nonatomic, assign) double sessionStart;
@property (nonatomic, assign) double firstFrame;   /* < 0 until the first buffer lands */
@property (atomic, assign) double openMs;          /* PROCESSING time: start -> first buffer  */
@property (atomic, assign) double settleMs;        /* STIMULUS time: first buffer -> kept frame */
@property (atomic, assign) int frames;
@property (atomic, assign) double keptLuma;
@property (atomic, assign) double keptDluma;
@end

@implementation Grabber {
    SettleCfg   _cfg;
    SettleState _st;
}

- (instancetype)init {
    if ((self = [super init])) {
        settle_cfg_from_env(&_cfg);
        settle_init(&_st);
        _firstFrame = -1.0;
        _keptLuma = -1.0;
        _keptDluma = -1.0;
        _verdict = SETTLE_WAIT;
    }
    return self;
}

/* Mean luminance over a sparse grid of a 32BGRA buffer, 0..255; -1 when the buffer is not BGRA
 * (the caller then runs the frames+time fallback rather than inventing a number). */
static double mean_luma_bgra(CVImageBufferRef buf) {
    if (CVPixelBufferGetPixelFormatType(buf) != kCVPixelFormatType_32BGRA) return -1.0;
    size_t w = CVPixelBufferGetWidth(buf), h = CVPixelBufferGetHeight(buf);
    size_t stride = CVPixelBufferGetBytesPerRow(buf);
    const unsigned char *base = (const unsigned char *)CVPixelBufferGetBaseAddress(buf);
    if (!base || w < 8 || h < 8) return -1.0;
    double sum = 0.0; long n = 0;
    for (size_t y = 0; y < h; y += 8) {
        const unsigned char *row = base + y * stride;
        for (size_t x = 0; x < w; x += 16) {
            const unsigned char *p = row + x * 4;
            /* Rec.601 luma from BGRA */
            sum += 0.114 * p[0] + 0.587 * p[1] + 0.299 * p[2];
            n++;
        }
    }
    return n ? sum / (double)n : -1.0;
}

- (void)writeFrame:(CVImageBufferRef)imageBuffer {
    CIImage *ciImage = [CIImage imageWithCVPixelBuffer:imageBuffer];
    CIContext *ctx = [CIContext contextWithOptions:nil];
    CGImageRef cgImage = [ctx createCGImage:ciImage fromRect:ciImage.extent];
    if (!cgImage) return;
    NSURL *url = [NSURL fileURLWithPath:self.outPath];
    CGImageDestinationRef dest = CGImageDestinationCreateWithURL((__bridge CFURLRef)url, kUTTypeJPEG, 1, NULL);
    if (dest) {
        CGImageDestinationAddImage(dest, cgImage, NULL);
        CGImageDestinationFinalize(dest);
        CFRelease(dest);
    }
    CGImageRelease(cgImage);
}

- (void)captureOutput:(AVCaptureOutput *)output didOutputSampleBuffer:(CMSampleBufferRef)sampleBuffer fromConnection:(AVCaptureConnection *)connection {
    if (self.done) return;
    CVImageBufferRef imageBuffer = CMSampleBufferGetImageBuffer(sampleBuffer);
    if (!imageBuffer) return;

    double now = CFAbsoluteTimeGetCurrent();
    if (self.firstFrame < 0.0) {
        self.firstFrame = now;
        self.openMs = (now - self.sessionStart) * 1000.0;   /* the PROCESSING-time clock */
    }
    double stimMs = (now - self.firstFrame) * 1000.0;       /* the STIMULUS-time clock   */

    CVPixelBufferLockBaseAddress(imageBuffer, kCVPixelBufferLock_ReadOnly);
    double luma = mean_luma_bgra(imageBuffer);
    CVPixelBufferUnlockBaseAddress(imageBuffer, kCVPixelBufferLock_ReadOnly);
    if (luma >= 0.0) self.haveLuma = YES;

    int r = settle_step(&_cfg, &_st, luma, stimMs);
    self.frames = _st.frames;
    if (r == SETTLE_WAIT) return;

    /* Keep THIS buffer — on a timeout too, so the caller always gets the most recent frame rather
     * than a stale copy we had to retain. */
    CVPixelBufferLockBaseAddress(imageBuffer, kCVPixelBufferLock_ReadOnly);
    [self writeFrame:imageBuffer];
    CVPixelBufferUnlockBaseAddress(imageBuffer, kCVPixelBufferLock_ReadOnly);

    self.settleMs  = stimMs;
    self.keptLuma  = luma;
    self.keptDluma = _st.dluma;
    self.verdict   = r;
    self.done      = YES;
}
@end

static void print_marker(Grabber *g) {
    char luma[32], dluma[32];
    if (g.keptLuma  >= 0.0) snprintf(luma,  sizeof luma,  "%.1f", g.keptLuma);  else snprintf(luma,  sizeof luma,  "na");
    if (g.keptDluma >= 0.0) snprintf(dluma, sizeof dluma, "%.4f", g.keptDluma); else snprintf(dluma, sizeof dluma, "na");
    printf("imac-cam: frames=%d open_ms=%.0f settle_ms=%.0f settled=%s luma=%s dluma=%s\n",
           g.frames, g.openMs, g.settleMs, settle_word(g.verdict), luma, dluma);
    fflush(stdout);
}

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        if (argc < 2) { fprintf(stderr, "usage: imac-cam <outpath>\n"); return 1; }
        NSString *outPath = [NSString stringWithUTF8String:argv[1]];

        AVCaptureDevice *device = [AVCaptureDevice defaultDeviceWithMediaType:AVMediaTypeVideo];
        if (!device) { fprintf(stderr, "no camera\n"); return 2; }
        NSError *error = nil;
        AVCaptureDeviceInput *input = [AVCaptureDeviceInput deviceInputWithDevice:device error:&error];
        if (!input) { fprintf(stderr, "input error: %s\n", error.localizedDescription.UTF8String); return 3; }

        AVCaptureSession *session = [[AVCaptureSession alloc] init];
        [session addInput:input];

        AVCaptureVideoDataOutput *output = [[AVCaptureVideoDataOutput alloc] init];
        /* BGRA is what gives us the luma axis. Ask only if the device offers it — forcing an
         * unsupported format throws, and a thrown format negotiation would cost us the frame
         * entirely. Without it the settle core runs its frames+time fallback and says so. */
        if ([output.availableVideoCVPixelFormatTypes containsObject:@(kCVPixelFormatType_32BGRA)]) {
            output.videoSettings = @{ (id)kCVPixelBufferPixelFormatTypeKey : @(kCVPixelFormatType_32BGRA) };
        }
        /* We are dropping frames on purpose while the sensor converges; never queue them up. */
        output.alwaysDiscardsLateVideoFrames = YES;

        Grabber *grabber = [[Grabber alloc] init];
        grabber.outPath = outPath;
        grabber.done = NO;
        dispatch_queue_t queue = dispatch_queue_create("cam", NULL);
        [output setSampleBufferDelegate:grabber queue:queue];
        [session addOutput:output];

        grabber.sessionStart = CFAbsoluteTimeGetCurrent();
        [session startRunning];

        /* The outer bound is PROCESSING time and covers open + settle. It is deliberately larger
         * than the stimulus-time deadline so a slow device open cannot masquerade as a sensor that
         * refused to converge — the two failures print differently. */
        double outer = env_d("IMAC_CAM_SETTLE_MS", 5000.0) / 1000.0 + 4.0;
        NSDate *deadline = [NSDate dateWithTimeIntervalSinceNow:outer];
        while (!grabber.done && [deadline timeIntervalSinceNow] > 0) {
            [[NSRunLoop currentRunLoop] runUntilDate:[NSDate dateWithTimeIntervalSinceNow:0.1]];
        }

        [session stopRunning];

        if (!grabber.done) {
            printf("imac-cam: frames=%d open_ms=%.0f settle_ms=na settled=none luma=na dluma=na\n",
                   grabber.frames, grabber.openMs);
            fflush(stdout);
            fprintf(stderr, "timeout, no frame\n");
            return 4;
        }

        print_marker(grabber);
        if (grabber.verdict == SETTLE_TIMEOUT) {
            fprintf(stderr, "unsettled: sensor never converged within %.0fms of stimulus time\n",
                    env_d("IMAC_CAM_SETTLE_MS", 5000.0));
            return 5;
        }
        return 0;
    }
}
#endif /* IMAC_CAM_SELFTEST */
