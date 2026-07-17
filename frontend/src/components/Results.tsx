import { useEffect, useState } from "react";
import type { PredictionResult } from "../api";

type Props = {
  image: File;
  result: PredictionResult;
  onReset: () => void;
};

export default function Results({
  image,
  result,
  onReset,
}: Props) {
  const [preview, setPreview] = useState("");

  useEffect(() => {
    const url = URL.createObjectURL(image);
    setPreview(url);

    return () => URL.revokeObjectURL(url);
  }, [image]);

  const sortedProbabilities = Object.entries(result.probabilities).sort(
    (a, b) => b[1] - a[1]
  );

  return (
    <div
      style={{
        marginTop: 30,
        background: "#ffffff",
        borderRadius: 20,
        padding: 30,
        boxShadow: "0 10px 30px rgba(0,0,0,0.08)",
      }}
    >
      <h2
        style={{
          textAlign: "center",
          marginBottom: 25,
          color: "#1e40af",
        }}
      >
        Prediction Result
      </h2>

      <div
        style={{
          display: "flex",
          gap: 30,
          flexWrap: "wrap",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <img
          src={preview}
          alt="Captured Face"
          style={{
            width: 260,
            borderRadius: 15,
            objectFit: "cover",
            boxShadow: "0 5px 15px rgba(0,0,0,.15)",
          }}
        />

        <div style={{ flex: 1, minWidth: 280 }}>
          <h3
            style={{
              color: "#0f172a",
              marginBottom: 15,
            }}
          >
            Prediction
          </h3>

          <div
            style={{
              fontSize: 28,
              fontWeight: "bold",
              color:
                result.prediction === "ASD"
                  ? "#dc2626"
                  : "#16a34a",
            }}
          >
            {result.prediction}
          </div>

          <p
            style={{
              marginTop: 10,
              fontSize: 18,
            }}
          >
            Confidence:
            <strong> {result.confidence.toFixed(2)}%</strong>
          </p>

          <div style={{ marginTop: 25 }}>
            {sortedProbabilities.map(([label, probability]) => (
              <div
                key={label}
                style={{ marginBottom: 15 }}
              >
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    marginBottom: 5,
                    fontWeight: 600,
                  }}
                >
                  <span>{label}</span>

                  <span>{probability.toFixed(2)}%</span>
                </div>

                <div
                  style={{
                    height: 12,
                    background: "#e5e7eb",
                    borderRadius: 20,
                    overflow: "hidden",
                  }}
                >
                  <div
                    style={{
                      width: `${Math.min(probability, 100)}%`,
                      height: "100%",
                      background:
                        label === "ASD"
                          ? "linear-gradient(90deg,#ef4444,#dc2626)"
                          : "linear-gradient(90deg,#22c55e,#16a34a)",
                    }}
                  />
                </div>
              </div>
            ))}
          </div>

          {result.disclaimer && (
            <div
              style={{
                marginTop: 25,
                padding: 15,
                borderRadius: 10,
                background: "#fff8e1",
                color: "#7c5a00",
                fontSize: 14,
                lineHeight: 1.5,
              }}
            >
              <strong>Disclaimer:</strong> {result.disclaimer}
            </div>
          )}

          <button
            onClick={onReset}
            style={{
              marginTop: 30,
              width: "100%",
              padding: 14,
              border: "none",
              borderRadius: 12,
              cursor: "pointer",
              background: "#2563eb",
              color: "#fff",
              fontSize: 16,
              fontWeight: 600,
            }}
          >
            Analyse Another Image
          </button>
        </div>
      </div>
    </div>
  );
}