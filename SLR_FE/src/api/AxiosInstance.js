import axios from "axios";

const axiosInstance = axios.create({
  baseURL: process.env.SLA_API_URL || "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export default axiosInstance;
