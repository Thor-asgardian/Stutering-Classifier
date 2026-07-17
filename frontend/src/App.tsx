import { useState } from "react";

import Camera from "./Camera";
import Results from "./components/Results";

import {
  predictImage,
  PredictionResult,
} from "./api";

export default function App() {
  const [loading, setLoading] = useState(false);

  const [result, setResult] =
    useState<PredictionResult | null>(null);

  const [capturedImage, setCapturedImage] =
    useState<File | null>(null);

  const [error, setError] =
    useState("");

  async function handleCapture(file: File) {
    setCapturedImage(file);
    setLoading(true);
    setResult(null);
    setError("");

    try {
      const prediction = await predictImage(file);

      setResult(prediction);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Prediction failed.");
      }
    } finally {
      setLoading(false);
    }
  }

  function resetPrediction() {
    setCapturedImage(null);
    setResult(null);
    setError("");
    setLoading(false);
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#eef2ff",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: 40,
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: 900,
        }}
      >
        <h1
          style={{
            textAlign: "center",
            marginBottom: 30,
            color: "#1e3a8a",
          }}
        >
          Autism Spectrum Disorder (ASD) Screening
        </h1>

        <Camera
          disabled={loading}
          onCapture={handleCapture}
        />

        {loading && (
          <div
            style={{
              marginTop: 30,
              textAlign: "center",
              fontWeight: "bold",
            }}
          >
            Analysing image...
          </div>
        )}

        {error && (
          <div
            style={{
              marginTop: 25,
              color: "red",
              textAlign: "center",
            }}
          >
            {error}
          </div>
        )}

        {result && capturedImage && (
          <Results
            image={capturedImage}
            result={result}
            onReset={resetPrediction}
          />
        )}
      </div>
    </div>
  );
}