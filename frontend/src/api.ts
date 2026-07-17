const API_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000";

export interface PredictionResult {
  prediction: string;
  confidence: number;
  probabilities: Record<string, number>;
  disclaimer: string;
}

export async function predictImage(
  image: File
): Promise<PredictionResult> {
  const formData = new FormData();
  formData.append("image", image);

  const response = await fetch(`${API_URL}/predict`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    let message = "Prediction failed.";

    try {
      const error = await response.json();
      if (error.detail) message = error.detail;
    } catch {}

    throw new Error(message);
  }

  return response.json();
}