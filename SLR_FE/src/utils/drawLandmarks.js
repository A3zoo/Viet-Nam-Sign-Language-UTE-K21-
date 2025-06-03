import { drawConnectors, drawLandmarks } from "@mediapipe/drawing_utils";
import { POSE_CONNECTIONS, HAND_CONNECTIONS } from "@mediapipe/holistic";
import speak from "../static/images/speaking_426426.png";

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
      color: "#00FF00",
      fillColor: "#00FF00",
      radius: 0.5,
    });
  }

  // console.log(results.poseLandmarks[0].x * canvasCtx.canvas.width);
  // console.log(results.poseLandmarks[0].y * canvasCtx.canvas.height);

  if (results.rightHandLandmarks) {
    drawConnectors(canvasCtx, results.rightHandLandmarks, HAND_CONNECTIONS, {
      color: "#00FF00",
      lineWidth: 1,
    });
    drawLandmarks(canvasCtx, results.rightHandLandmarks, {
      color: "#00FF00",
      fillColor: "#00FF00",
      radius: 1,
    });
  }

  if (results.leftHandLandmarks) {
    drawConnectors(canvasCtx, results.leftHandLandmarks, HAND_CONNECTIONS, {
      color: "#00FF00",
      lineWidth: 1,
    });
    drawLandmarks(canvasCtx, results.leftHandLandmarks, {
      color: "#00FF00",
      fillColor: "#00FF00",
      radius: 1,
    });
    // console.log(results.leftHandLandmarks[8].x * canvasCtx.canvas.width);
    // console.log(results.leftHandLandmarks[8].y * canvasCtx.canvas.height);
  }
  // const img = new Image();
  // img.src = speak;
  // canvasCtx.drawImage(img, 10, 15, 30, 30);
};
