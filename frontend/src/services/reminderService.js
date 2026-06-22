import apiClient from "./apiClient";

export const reminderService = {
  async create(data) {
    const res = await apiClient.post("/api/reminders", data);
    return res.data;
  },

  async list(filters = {}) {
    const res = await apiClient.get("/api/reminders", { params: filters });
    return res.data;
  },

  async getOne(id) {
    const res = await apiClient.get(`/api/reminders/${id}`);
    return res.data;
  },

  async update(id, data) {
    const res = await apiClient.put(`/api/reminders/${id}`, data);
    return res.data;
  },

  async markPaid(id) {
    const res = await apiClient.post(`/api/reminders/${id}/mark-paid`);
    return res.data;
  },

  async remove(id) {
    const res = await apiClient.delete(`/api/reminders/${id}`);
    return res.data;
  },
};
