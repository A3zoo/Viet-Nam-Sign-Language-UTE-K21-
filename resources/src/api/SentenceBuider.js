import axiosInstance from "./AxiosInstance";

export const sentenceBuilder = async (listWord) => {
  const prompt = `Tôi có các từ sau: ${listWord.join(
    ", "
  )}. Hãy ghép chúng thành một câu hoàn chỉnh.`;

  try {
    const response = await axiosInstance.post(
      "https://api.openai.com/v1/chat/completions",
      {
        model: "gpt-3.5-turbo", 
        messages: [
          { role: "system", content: "Bạn là một trợ lý AI" },
          { role: "user", content: prompt },
        ],
        max_tokens: 60,
        temperature: 0.7,
      },
      {
        headers: {
          Authorization: `Bearer ${process.env.REACT_APP_OPENAI_API_KEY}`, // Sử dụng biến môi trường
          "Content-Type": "application/json",
        },
      }
    );
    const generatedText = response.data.choices[0].message.content.trim();
    return generatedText;
  } catch (error) {
    console.error("Error generating sentence:", error);
    return "Có lỗi xảy ra!";
  }
};
