import axiosInstance from "./AxiosInstance";

export const test = async (lm_list) => {
  console.log("checkk::", lm_list);
  const response = await axiosInstance.post("/test", {
    name: "dat",
    age: 1,
  });
  return response.data;
};
