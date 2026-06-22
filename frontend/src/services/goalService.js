import apiClient from "./apiClient";

export const goalService = {
  async create(data) {
    const res = await apiClient.post("/api/goals", data);
    return res.data;
  },

  async list() {
    const res = await apiClient.get("/api/goals");
    return res.data;
  },

  async getOne(id) {
    const res = await apiClient.get(`/api/goals/${id}`);
    return res.data;
  },

  async update(id, data) {
    const res = await apiClient.put(`/api/goals/${id}`, data);
    return res.data;
  },

  async contribute(id, amount) {
    const res = await apiClient.post(`/api/goals/${id}/contribute`, { amount });
    return res.data;
  },

  async remove(id) {
    const res = await apiClient.delete(`/api/goals/${id}`);
    return res.data;
  },
};
