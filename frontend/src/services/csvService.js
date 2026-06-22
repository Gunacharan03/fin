import apiClient from "./apiClient";

export const csvService = {
  async preview(file) {
    const formData = new FormData();
    formData.append("file", file);
    const res = await apiClient.post("/api/csv/preview", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return res.data;
  },

  async confirm(file) {
    const formData = new FormData();
    formData.append("file", file);
    const res = await apiClient.post("/api/csv/confirm", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return res.data;
  },
};
