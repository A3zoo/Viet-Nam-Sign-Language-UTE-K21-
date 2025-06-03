import React, { useEffect, useState } from "react";
import WebcamHolistic from "./WebcamHolistic"; // Giả sử bạn có một component webcam
import "../styles/Home.scss";
import Header from "./header";
import { Button } from "@mui/material";
import KeyboardVoiceIcon from "@mui/icons-material/KeyboardVoice";
import DeleteIcon from "@mui/icons-material/Delete";
import { speakText } from "../utils/SpeakText";
import SpellcheckIcon from "@mui/icons-material/Spellcheck";
import Alert from "@mui/material/Alert";
import Snackbar from "@mui/material/Snackbar";

const Home = () => {
  const [listWord, setListWord] = useState([]);
  const [sentence, setSentence] = useState("");
  const [openAlert, setOpenAlert] = useState(false);

  const addWord = (detectedLabel) => {
    setListWord((prevList) => [...prevList, detectedLabel]);
  };

  useEffect(() => {
    console.log("list::: ", listWord);
  }, [listWord]);

  async function awaitMergeSentence() {
    try {
      const { GoogleGenerativeAI } = require("@google/generative-ai");

      const genAI = new GoogleGenerativeAI(process.env.REACT_APP_GEMINI_KEY);
      const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

      const prompt = `Tôi có các từ sau: ${listWord.join(
        ", "
      )}. Hãy ghép chúng thành một câu hoàn chỉnh, càng đơn giản càng tốt.`;
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
  const onClickMerge = () => {
    awaitMergeSentence();
  };

  const onClickRead = () => {
    if (sentence) {
      speakText(sentence);
    } else {
      setOpenAlert(true);
    }
  };

  const handleCloseAlert = () => {
    setOpenAlert(false);
  };

  const onClickDelete = () => {
    setListWord([]);
    setSentence("");
  };
  return (
    <div className="container">
      {/* Header with data */}
      <Header />

      {/* Main Content */}
      <div className="main-content">
        <div className="webcamContainer">
          <WebcamHolistic
            addWord={addWord}
            awaitReadSentence={awaitMergeSentence}
          />
        </div>
        <div
          className="textContainer"
          style={{ display: "flex", gap: "20px", minWidth: "40%" }}
        >
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
            <div style={{ display: "flex", gap: "10px" }}>
              <Button
                variant="contained"
                startIcon={<SpellcheckIcon />}
                onClick={onClickMerge}
              >
                Ghép từ
              </Button>
              <Button
                variant="contained"
                startIcon={<KeyboardVoiceIcon />}
                onClick={onClickRead}
                color="success"
              >
                Đọc
              </Button>
              <Button
                variant="contained"
                color="error"
                startIcon={<DeleteIcon />}
                onClick={onClickDelete}
              >
                Xóa toàn bộ
              </Button>
            </div>
          </div>

          <div className="textBox">
            <div>
              <span>
                <strong>Nhóm sinh viên thực hiện: </strong>
              </span>{" "}
            </div>
            <div className="listStudent">
              <span>Lê Đình Đạt - 21110416</span>{" "}
              <span>Lê Nam Hưng - 21110484</span>{" "}
              <span>Đào Quang Duy - 21110398</span>{" "}
            </div>
          </div>
        </div>
      </div>
      <Snackbar
        open={openAlert}
        autoHideDuration={3000}
        onClose={handleCloseAlert}
        anchorOrigin={{ vertical: "top", horizontal: "right" }}
      >
        <Alert severity="warning" color="warning" onClose={handleCloseAlert}>
          Chưa có câu nào được ghép.
        </Alert>
      </Snackbar>
    </div>
  );
};

export default Home;
