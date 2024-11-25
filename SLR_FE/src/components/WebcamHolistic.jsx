import React, { useRef, useEffect, useState } from "react";
import { Camera } from "@mediapipe/camera_utils";
import {
  Holistic,
  POSE_CONNECTIONS,
  HAND_CONNECTIONS,
} from "@mediapipe/holistic";
import { drawConnectors, drawLandmarks } from "@mediapipe/drawing_utils";
import ProgressBar from "./ProgressBar";
import { drawLandmarksOnCanvas } from "../utils/drawLandmarks";
import { makeLandmarkTimestep } from "../utils/makeLandmarkTimestep";
import { predict } from "../api/Landmarks";
import { test } from "../api/test";

const WebcamHolistic = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [holistic, setHolistic] = useState(null);
  const [message, setMessage] = useState("Waiting for hand detection..."); // Thông báo hiển thị
  const isRecording = useRef(false);
  const isRest = useRef(false);
  const startTime = useRef(null);
  const countdown = useRef(null);
  const cameraRef = useRef(null);
  const [progress, setProgress] = useState(0);
  const coordinates = useRef([]); // Lưu tọa độ các landmarks

  useEffect(() => {
    const holisticInstance = new Holistic({
      locateFile: (file) =>
        `https://cdn.jsdelivr.net/npm/@mediapipe/holistic/${file}`,
    });

    holisticInstance.setOptions({
      selfieMode: true,
      upperBodyOnly: false,
      smoothLandmarks: true,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5,
    });

    holisticInstance.onResults(onResults);
    setHolistic(holisticInstance);

    return () => {
      holisticInstance.close();
    };
  }, []);

  useEffect(() => {
    if (videoRef.current && holistic) {
      const camera = new Camera(videoRef.current, {
        onFrame: async () => {
          await holistic.send({ image: videoRef.current });
        },
        width: 1280,
        height: 720,
      });
      camera.start();
      cameraRef.current = camera;

      if (cameraRef.current) {
        cameraRef.current.stop();
      }
    }
  }, [holistic]);

  const startRecording = () => {
    coordinates.current = [];
    // Reset dữ liệu tọa độ
    isRecording.current = true;
    countdown.current = 3000;
    startTime.current = Date.now();
    setMessage("Recording coordinates for 3 seconds...");
  };

  const stopRecording = async () => {
    isRest.current = true;
    isRecording.current = false;
    countdown.current = 2000;
    startTime.current = Date.now();
    setMessage("Resting for 2 seconds...");

    try {
      // Gọi API predict
      console.log("predict:", coordinates.current);
      const response = await predict(coordinates.current);
      // const response = await test(coordinates.current);

      setMessage(`Detected: ${response.label}`); // Cập nhật giao diện với kết quả nhận diện
    } catch (error) {
      console.error("Prediction API error:", error);
      setMessage("Error in detection. Please try again.");
    } finally {
      coordinates.current = [];
    }
  };

  const onResults = async (results) => {
    const canvas = canvasRef.current;
    const canvasCtx = canvas.getContext("2d");

    canvasCtx.save();
    drawLandmarksOnCanvas(canvasCtx, results);

    if (isRest.current) {
      if (Date.now() - startTime.current >= countdown.current) {
        isRest.current = false;
        setMessage("Ready to detect again!");
      }
    } else {
      if (
        !isRecording.current &&
        (results.rightHandLandmarks || results.leftHandLandmarks)
      ) {
        startRecording();
      } else if (isRecording.current) {
        const normalizedLandmarks = makeLandmarkTimestep(results);

        coordinates.current.push(normalizedLandmarks);

        if (Date.now() - startTime.current >= countdown.current) {
          await stopRecording(); // Đảm bảo chờ xử lý xong trước khi tiếp tục
        }
      }
    }
  };

  useEffect(() => {
    if (isRecording.current && !isRest.current) {
      const totalDuration = countdown.current;
      const interval = setInterval(() => {
        const elapsedTime = Date.now() - startTime.current;
        const progressPercentage = Math.min(
          (elapsedTime / totalDuration) * 100,
          100
        );
        setProgress(progressPercentage);

        if (progressPercentage >= 100) {
          clearInterval(interval);
        }
      }, 100);

      return () => clearInterval(interval);
    } else {
      setProgress(0); // Reset khi không ghi hoặc nghỉ
    }
  }, [isRecording.current, isRest.current]);

  return (
    <div className="webcam-holistic" style={{ position: "relative" }}>
      <video
        ref={videoRef}
        className="input_video"
        style={{ display: "none" }}
      ></video>
      <canvas
        ref={canvasRef}
        className="output_canvas"
        style={{ width: "100%", height: "100vh" }}
      ></canvas>
      <div
        style={{
          position: "absolute",
          top: "20px",
          left: "50%",
          transform: "translateX(-50%)",
          backgroundColor: "rgba(0, 0, 0, 0.7)",
          color: "white",
          padding: "10px 20px",
          borderRadius: "10px",
          fontSize: "18px",
          textAlign: "center",
        }}
      >
        {message} {countdown > 0 && `(${countdown}s)`}
      </div>
      <div
        style={{
          position: "absolute",
          top: "20px", // Đặt cách phần trên cùng 20px
          right: "20px", // Đặt cách phần bên phải 20px
          width: "200px", // Đặt chiều rộng cụ thể cho thanh (tuỳ chỉnh)
          zIndex: 10, // Đảm bảo nó nằm trên các phần tử khác
        }}
      >
        <ProgressBar progress={progress} />
      </div>
    </div>
  );
};

export default WebcamHolistic;
