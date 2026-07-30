import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
});

export const uploadFile = async (formData) => {
  const response = await api.post("/billing/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

export const getReport = () =>
  api.get("/report").then((res) => res.data);

export const getAnalytics = () =>
  api.get("/analytics").then((res) => res.data);

export const getNarrative = () =>
  api.get("/narrative").then((res) => res.data);