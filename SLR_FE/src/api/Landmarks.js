import axiosInstance from "./AxiosInstance";

export const predict = async (lm_list) => {
  console.log("checkk::", lm_list);
  const response = await axiosInstance.post("http://127.0.0.1:8000/api/v1/slr/predict", { lm_list });
  return response.data;
};
