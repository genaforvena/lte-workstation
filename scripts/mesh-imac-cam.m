// mesh-imac-cam.m — native still-capture helper for macOS nodes with no ffmpeg/imagesnap/cv2 (ilya,
// macOS 10.13). PyObjC's block-signature bridging is broken on this box (BridgeSupport parse failure
// on AVFoundation's async completion-handler blocks) — this sidesteps it entirely with a normal
// Objective-C delegate method (AVCaptureVideoDataOutputSampleBufferDelegate), which the ObjC runtime's
// own method-signature introspection handles fine, no BridgeSupport metadata needed.
//
// Deployed+compiled by scripts/mesh-imac-cam (the genome tool); this .m is the tracked source of
// truth. Compile: clang -fobjc-arc -framework Foundation -framework AVFoundation -framework CoreMedia
// -framework CoreVideo -framework ImageIO -framework CoreServices -framework CoreImage
// -framework CoreGraphics -o imac-cam imac-cam.m
//
// usage: imac-cam <outpath.jpg> — grabs one frame from the default camera, writes JPEG, exits 0.
#import <Foundation/Foundation.h>
#import <AVFoundation/AVFoundation.h>
#import <CoreMedia/CoreMedia.h>
#import <CoreVideo/CoreVideo.h>
#import <ImageIO/ImageIO.h>
#import <CoreServices/CoreServices.h>

@interface Grabber : NSObject <AVCaptureVideoDataOutputSampleBufferDelegate>
@property (nonatomic, strong) NSString *outPath;
@property (nonatomic, assign) BOOL done;
@end

@implementation Grabber
- (void)captureOutput:(AVCaptureOutput *)output didOutputSampleBuffer:(CMSampleBufferRef)sampleBuffer fromConnection:(AVCaptureConnection *)connection {
    if (self.done) return;
    CVImageBufferRef imageBuffer = CMSampleBufferGetImageBuffer(sampleBuffer);
    CVPixelBufferLockBaseAddress(imageBuffer, 0);
    CIImage *ciImage = [CIImage imageWithCVPixelBuffer:imageBuffer];
    CIContext *ctx = [CIContext contextWithOptions:nil];
    CGImageRef cgImage = [ctx createCGImage:ciImage fromRect:ciImage.extent];
    CVPixelBufferUnlockBaseAddress(imageBuffer, 0);

    NSURL *url = [NSURL fileURLWithPath:self.outPath];
    CGImageDestinationRef dest = CGImageDestinationCreateWithURL((__bridge CFURLRef)url, kUTTypeJPEG, 1, NULL);
    CGImageDestinationAddImage(dest, cgImage, NULL);
    CGImageDestinationFinalize(dest);
    CFRelease(dest);
    CGImageRelease(cgImage);
    self.done = YES;
}
@end

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
        Grabber *grabber = [[Grabber alloc] init];
        grabber.outPath = outPath;
        grabber.done = NO;
        dispatch_queue_t queue = dispatch_queue_create("cam", NULL);
        [output setSampleBufferDelegate:grabber queue:queue];
        [session addOutput:output];

        [session startRunning];

        NSDate *deadline = [NSDate dateWithTimeIntervalSinceNow:8.0];
        while (!grabber.done && [deadline timeIntervalSinceNow] > 0) {
            [[NSRunLoop currentRunLoop] runUntilDate:[NSDate dateWithTimeIntervalSinceNow:0.1]];
        }

        [session stopRunning];

        if (!grabber.done) { fprintf(stderr, "timeout, no frame\n"); return 4; }
        return 0;
    }
}
