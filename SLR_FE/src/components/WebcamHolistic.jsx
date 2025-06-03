import React, { useRef, useEffect, useState } from "react";
import { Camera } from "@mediapipe/camera_utils";
import { Holistic } from "@mediapipe/holistic";
import ProgressBar from "./ProgressBar";
import { drawLandmarksOnCanvas } from "../utils/drawLandmarks";
import { makeLandmarkTimestep } from "../utils/makeLandmarkTimestep";
import { predict } from "../api/Landmarks";

const WebcamHolistic = ({
  addWord,
  awaitMergeSentence,
  onClickMerge,
  listWord,
  setListWord,
}) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [holistic, setHolistic] = useState(null);
  const [message, setMessage] = useState("Hãy thực hiện ký hiệu"); // Thông báo hiển thị
  const isRecording = useRef(false);
  const isRest = useRef(false);
  const startTime = useRef(null);
  const countdown = useRef(null);
  const cameraRef = useRef(null);
  const [progress, setProgress] = useState(0);
  const coordinates = useRef([]); // Lưu tọa độ các landmarks
  const [detectedLabel, setDetectedLabel] = useState(null);
  const box = useRef({ x: 0.17, y: 0, width: 0.06, height: 0.08 });
  const isSpeak = useRef(false);
  const handInBoxTimer = useRef(null);
  const handInBoxStartTime = useRef(null);
  const currentListWord = useRef(listWord);

  // Cập nhật currentListWord khi listWord thay đổi
  useEffect(() => {
    currentListWord.current = listWord;
    console.log("listWord updated in ref:", currentListWord.current);
  }, [listWord]);

  useEffect(() => {
    if (detectedLabel) {
      console.log("New detected label:", detectedLabel);
      setListWord((prevList) => [...prevList, detectedLabel]);
    }
  }, [detectedLabel]);

  useEffect(() => {
    const holisticInstance = new Holistic({
      locateFile: (file) =>
        `https://cdn.jsdelivr.net/npm/@mediapipe/holistic/${file}`,
    });

    holisticInstance.setOptions({
      selfieMode: true,
      upperBodyOnly: true,
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
        width: 1920,
        height: 1080,
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
    setMessage("Bắt đầu nhận diện");
  };

  const stopRecording = async () => {
    isRest.current = true;
    isRecording.current = false;
    countdown.current = 2000;
    startTime.current = Date.now();
    setMessage("Thời gian nghỉ 2s");

    async function awaitPredict() {
      try {
        // console.log("predict:", coordinates.current);
        const response = await predict(coordinates.current); // Gọi API
        setDetectedLabel(response.label); // Cập nhật nhãn phát hiện
      } catch (error) {
        console.error("Prediction API error:", error);
        setMessage("Có lỗi xảy ra. Hãy thử lại.");
      } finally {
        coordinates.current = []; // Reset tọa độ sau khi gọi API
      }
    }

    awaitPredict();
  };

  // const checkHand = (canvasCtx, results) => {
  //   // Biến để theo dõi thời gian chờ (ngăn không cho gọi lại trong 2s)
  //   let canRead = true;

  //   if (results.rightHandLandmarks) {
  //     const x = results.rightHandLandmarks[8].x * canvasCtx.canvas.width;
  //     const y = results.rightHandLandmarks[8].y * canvasCtx.canvas.height;

  //     // Kiểm tra xem ngón tay có nằm trong khu vực quy định không
  //     if (x < 65 && x > 20 && y < 45 && y > 30 && canRead) {
  //       isSpeak.current = true;
  //       console.log("read");

  //       const read = async () => {
  //         if (isSpeak.current) {
  //           await awaitMergeSentence();
  //         }
  //       };

  //       read();

  //       canRead = false;
  //       setTimeout(() => {
  //         canRead = true;
  //       }, 2000);
  //     }
  //   }
  // };

  useEffect(() => {
    if (isSpeak.current) {
      console.log("doc");
      // awaitReadSentence();
      // isSpeak.current = false;
    } else {
      console.log("not true");
    }
  }, [isSpeak.current]);

  const onResults = async (results) => {
    const canvas = canvasRef.current;
    const canvasCtx = canvas.getContext("2d");

    // Lấy kích thước của video và canvas
    const videoWidth = videoRef.current.videoWidth;
    const videoHeight = videoRef.current.videoHeight;

    canvasCtx.save();
    drawLandmarksOnCanvas(canvasCtx, results);

    // Vẽ ô vuông bên trái
    const boxSize = 40;
    const boxX = 20;
    const boxY = canvas.height / 2 - boxSize / 2;

    canvasCtx.strokeStyle = "#00FF00";
    canvasCtx.lineWidth = 2;
    canvasCtx.strokeRect(boxX, boxY, boxSize, boxSize);

    // Kiểm tra nếu tay phải có landmarks
    if (results?.rightHandLandmarks?.[8]) {
      const indexFinger = results.rightHandLandmarks[8]; // Ngón trỏ
      const fingerX = indexFinger.x * canvas.width;
      const fingerY = indexFinger.y * canvas.height;

      // Kiểm tra xem ngón trỏ có nằm trong ô vuông không
      if (
        fingerX >= 50 &&
        fingerX <= 65 &&
        fingerY >= 90 &&
        fingerY <= 120 &&
        !isRecording.current
      ) {
        // Nếu chưa có timer, bắt đầu đếm thời gian
        if (!handInBoxStartTime.current) {
          handInBoxStartTime.current = Date.now();
        }

        // Kiểm tra nếu đã ở trong ô đủ 1 giây
        if (Date.now() - handInBoxStartTime.current >= 1000) {
          console.log("Current listWord from ref:", currentListWord.current);

          awaitMergeSentence(currentListWord.current);

          handInBoxStartTime.current = null; // Reset timer
        }
      } else {
        // Nếu tay ra khỏi ô, reset timer
        handInBoxStartTime.current = null;
      }
    } else {
      // Nếu không phát hiện tay, reset timer
      handInBoxStartTime.current = null;
    }

    if (isRest.current) {
      if (Date.now() - startTime.current >= countdown.current) {
        isRest.current = false;
        setMessage("Sẵn sàng nhận diện!");
      }
    } else {
      if (!isRecording.current && results.leftHandLandmarks) {
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
    <div
      className="webcam-holistic"
      style={{
        position: "relative",
        border: "3px solid #000",
        borderRadius: "10px",
      }}
    >
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
          top: "4%",
          left: "60%",
          // transform: "translateX(-50%)",
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
          top: "4%",
          left: "5%",
          width: "200px",
          zIndex: 10,
        }}
      >
        <ProgressBar progress={progress} />
      </div>
      <div
        style={{
          position: "absolute",
          bottom: "15%", // Đặt ở cuối màn hình
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
        {detectedLabel ? `Dự đoán: ${detectedLabel}` : "Chưa có hành động"}
      </div>
    </div>
  );
};

export default WebcamHolistic;
