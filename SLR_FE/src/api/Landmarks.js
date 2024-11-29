import axiosInstance from "./AxiosInstance";

export const predict = async (lm_list) => {
  console.log("checkk::", lm_list);
  const response = await axiosInstance.post("/slr/predict", { lm_list });
  return response.data;
};
