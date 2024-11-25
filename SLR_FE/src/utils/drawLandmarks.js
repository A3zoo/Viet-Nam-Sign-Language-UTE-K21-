import { drawConnectors, drawLandmarks } from "@mediapipe/drawing_utils";
import { POSE_CONNECTIONS, HAND_CONNECTIONS } from "@mediapipe/holistic";

export const drawLandmarksOnCanvas = (canvasCtx, results) => {
  canvasCtx.clearRect(0, 0, canvasCtx.canvas.width, canvasCtx.canvas.height);
  canvasCtx.drawImage(
    results.image,
    0,
    0,
    canvasCtx.canvas.width,
    canvasCtx.canvas.height
  );

  if (results.poseLandmarks) {
    drawConnectors(canvasCtx, results.poseLandmarks, POSE_CONNECTIONS, {
      color: "#00FF00",
      lineWidth: 1,
    });
    drawLandmarks(canvasCtx, results.poseLandmarks, {
      color: "#FF0000",
      fillColor: "#FF0000",
      radius: 0.5,
    });
  }

  if (results.rightHandLandmarks) {
    drawConnectors(canvasCtx, results.rightHandLandmarks, HAND_CONNECTIONS, {
      color: "#00FF00",
      lineWidth: 1,
    });
    drawLandmarks(canvasCtx, results.rightHandLandmarks, {
      color: "#00FF00",
      fillColor: "#FF0000",
      radius: 1,
    });
  }

  if (results.leftHandLandmarks) {
    drawConnectors(canvasCtx, results.leftHandLandmarks, HAND_CONNECTIONS, {
      color: "#FF0000",
      lineWidth: 1,
    });
    drawLandmarks(canvasCtx, results.leftHandLandmarks, {
      color: "#FF0000",
      fillColor: "#00FF00",
      radius: 1,
    });
  }
};
