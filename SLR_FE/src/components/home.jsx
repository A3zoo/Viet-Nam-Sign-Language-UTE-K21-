import React, { useEffect, useState } from "react";
import WebcamHolistic from "./WebcamHolistic"; // Giả sử bạn có một component webcam
import "../styles/Home.scss";
import Header from "./header";
import { Button } from "@mui/material";
import KeyboardVoiceIcon from "@mui/icons-material/KeyboardVoice";
import { sentenceBuilder } from "../api/SentenceBuider";
import { speakText } from "../utils/SpeakText";

const Home = () => {
  const [listWord, setListWord] = useState([]);
  const [sentence, setSentence] = useState("");
  const addWord = (detectedLabel) => {
    setListWord((prevList) => [...prevList, detectedLabel]);
  };

  useEffect(() => {
    console.log("list::: ", listWord);
  }, [listWord]);

  useEffect(() => {
    if (sentence) {
      speakText(sentence);
      //   setSentence("");
    }
  }, [sentence]);

  const onClickRead = () => {
    async function awaitReadSentence() {
      try {
        const { GoogleGenerativeAI } = require("@google/generative-ai");

        const genAI = new GoogleGenerativeAI(process.env.REACT_APP_GEMINI_KEY);
        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

        const prompt = `Tôi có các từ sau: ${listWord.join(
          ", "
        )}. Hãy ghép chúng thành một câu hoàn chỉnh.`;
        console.log(prompt);
        const result = await model.generateContent(prompt);
        console.log(result.response.text());

        setSentence(result.response.text());
        setListWord([]);
      } catch (error) {
        alert("Đã có lỗi xảy ra", error);
        console.log(error);
      }
    }
    awaitReadSentence();
  };

  return (
    <div className="container">
      {/* Header with data */}
      <Header />

      {/* Main Content */}
      <div className="main-content">
        <div className="webcamContainer">
          <WebcamHolistic addWord={addWord} />
        </div>
        <div className="textContainer">
          <div className="textBox">
            <div>
              <span>
                <strong>Từ:</strong>
                {listWord.length > 0 ? listWord.join(", ") : ""}
              </span>{" "}
            </div>
            <div>
              <span>
                <strong>Câu:</strong> {sentence}
              </span>{" "}
            </div>
            <Button
              variant="contained"
              startIcon={<KeyboardVoiceIcon />}
              onClick={onClickRead}
            >
              Đọc
            </Button>{" "}
            {/* Nút "Đọc" */}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
