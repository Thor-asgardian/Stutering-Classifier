import { useEffect, useRef, useState } from "react";

type Props = {
  disabled?: boolean;
  onCapture: (file: File) => void;
};

export default function Camera({
  disabled = false,
  onCapture,
}: Props) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const [cameraOn, setCameraOn] = useState(false);
  const [captured, setCaptured] = useState<string | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    return () => stopCamera();
  }, []);

  useEffect(() => {
    async function attachStream() {
      if (
        cameraOn &&
        streamRef.current &&
        videoRef.current
      ) {
        videoRef.current.srcObject = streamRef.current;

        try {
          await videoRef.current.play();
        } catch (err) {
          console.error("Unable to play video:", err);
        }
      }
    }

    attachStream();
  }, [cameraOn]);

  async function startCamera() {
    try {
      setError("");

      const media = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: "user",
          width: { ideal: 640 },
          height: { ideal: 480 },
        },
        audio: false,
      });

      streamRef.current = media;
      setCameraOn(true);
    } catch (err) {
      console.error(err);
      setError("Unable to access the camera. Please allow camera permission.");
    }
  }

  function stopCamera() {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }

    setCameraOn(false);
  }

  function captureImage() {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;

    if (video.videoWidth === 0 || video.videoHeight === 0) {
      setError("Camera is not ready yet.");
      return;
    }

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.drawImage(video, 0, 0);

    canvas.toBlob(
      (blob) => {
        if (!blob) return;

        const preview = URL.createObjectURL(blob);
        setCaptured(preview);

        const file = new File(
          [blob],
          "captured_face.jpg",
          {
            type: "image/jpeg",
          }
        );

        stopCamera();
        onCapture(file);
      },
      "image/jpeg",
      0.95
    );
  }

  function retake() {
    if (captured) {
      URL.revokeObjectURL(captured);
    }

    setCaptured(null);
    startCamera();
  }

  return (
    <div
      style={{
        background: "#fff",
        padding: 25,
        borderRadius: 15,
        boxShadow: "0 10px 25px rgba(0,0,0,.08)",
      }}
    >
      <h2>Autism Spectrum Disorder (ASD) Screening</h2>

      {error && (
        <p style={{ color: "red" }}>
          {error}
        </p>
      )}

      {!cameraOn && !captured && (
        <button
          onClick={startCamera}
          disabled={disabled}
        >
          Open Camera
        </button>
      )}

      <video
        ref={videoRef}
        autoPlay
        playsInline
        muted
        style={{
          display: cameraOn ? "block" : "none",
          width: "100%",
          maxWidth: 640,
          borderRadius: 12,
          background: "#000",
          marginTop: 20,
        }}
      />

      {cameraOn && (
        <button
          onClick={captureImage}
          disabled={disabled}
          style={{ marginTop: 20 }}
        >
          Capture Photo
        </button>
      )}

      {captured && (
        <>
          <img
            src={captured}
            alt="Captured"
            style={{
              width: "100%",
              maxWidth: 640,
              borderRadius: 12,
              marginTop: 20,
            }}
          />

          <button
            onClick={retake}
            disabled={disabled}
            style={{ marginTop: 20 }}
          >
            Retake Photo
          </button>
        </>
      )}

      <canvas
        ref={canvasRef}
        style={{ display: "none" }}
      />
    </div>
  );
}