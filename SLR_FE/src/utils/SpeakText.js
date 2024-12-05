export const speakText = (text) => {
  if ("speechSynthesis" in window) {
    const utterance = new SpeechSynthesisUtterance(text);

    utterance.lang = "vi-VN"; // Ngôn ngữ tiếng Việt
    utterance.rate = 0.6; // Tốc độ nói (1 là tốc độ bình thường)
    utterance.pitch = 1; // Cao độ (1 là bình thường)

    window.speechSynthesis.speak(utterance);
  } else {
    console.log("Speech Synthesis không được hỗ trợ trên trình duyệt này");
  }
};
