// macmic — record N seconds of the default mic to an .m4a on macOS, headless-friendly.
// Usage: macmic <out.m4a> <seconds>
// Exit 0 = wrote a file; 2 = no audio device / capture could not start (honest n/a).
import AVFoundation
import Foundation

let args = CommandLine.arguments
guard args.count >= 3, let dur = Double(args[2]) else {
    FileHandle.standardError.write("usage: macmic <out.m4a> <seconds>\n".data(using: .utf8)!)
    exit(64)
}
let outPath = args[1]
let outURL = URL(fileURLWithPath: outPath)
try? FileManager.default.removeItem(at: outURL)

guard let device = AVCaptureDevice.default(for: .audio) else {
    FileHandle.standardError.write("macmic: no audio capture device\n".data(using: .utf8)!)
    exit(2)
}

let session = AVCaptureSession()
do {
    let input = try AVCaptureDeviceInput(device: device)
    guard session.canAddInput(input) else { FileHandle.standardError.write("macmic: cannot add mic input\n".data(using: .utf8)!); exit(2) }
    session.addInput(input)
} catch {
    FileHandle.standardError.write("macmic: input error \(error)\n".data(using: .utf8)!)
    exit(2)
}

let output = AVCaptureAudioFileOutput()
guard session.canAddOutput(output) else { FileHandle.standardError.write("macmic: cannot add file output\n".data(using: .utf8)!); exit(2) }
session.addOutput(output)

final class Delegate: NSObject, AVCaptureFileOutputRecordingDelegate {
    var done = false
    var ok = false
    // macOS 10.13 signature
    func fileOutput(_ output: AVCaptureFileOutput, didFinishRecordingTo outputFileURL: URL, from connections: [AVCaptureConnection], error: Error?) {
        if let e = error { FileHandle.standardError.write("macmic: finish error \(e)\n".data(using: .utf8)!) }
        else { ok = true }
        done = true
    }
}
let delegate = Delegate()

session.startRunning()
// give the session a beat to warm the mic
Thread.sleep(forTimeInterval: 0.4)
output.startRecording(to: outURL, outputFileType: .m4a, recordingDelegate: delegate)
Thread.sleep(forTimeInterval: dur)
output.stopRecording()

// pump the run loop until the delegate reports the file is finalized (or a timeout)
let deadline = Date().addingTimeInterval(10)
while !delegate.done && Date() < deadline {
    RunLoop.current.run(mode: .default, before: Date().addingTimeInterval(0.1))
}
session.stopRunning()

if delegate.ok, let attrs = try? FileManager.default.attributesOfItem(atPath: outPath),
   let size = attrs[.size] as? Int, size > 0 {
    print(size)
    exit(0)
}
exit(2)
