import apiClient from "./apiClient";

export const transactionService = {
  async create(data) {
    const res = await apiClient.post("/api/transactions", data);
    return res.data;
  },

  async list(filters = {}) {
    const res = await apiClient.get("/api/transactions", { params: filters });
    return res.data;
  },

  async getOne(id) {
    const res = await apiClient.get(`/api/transactions/${id}`);
    return res.data;
  },

  async update(id, data) {
    const res = await apiClient.put(`/api/transactions/${id}`, data);
    return res.data;
  },

  async remove(id) {
    const res = await apiClient.delete(`/api/transactions/${id}`);
    return res.data;
  },
};
