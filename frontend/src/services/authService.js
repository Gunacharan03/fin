import apiClient from "./apiClient";

export const authService = {
  async register(data) {
    const res = await apiClient.post("/api/auth/register", data);
    return res.data;
  },

  async login(data) {
    const res = await apiClient.post("/api/auth/login", data);
    return res.data;
  },

  async getProfile() {
    const res = await apiClient.get("/api/auth/me");
    return res.data;
  },

  async updateProfile(data) {
    const res = await apiClient.put("/api/auth/me", data);
    return res.data;
  },

  async changePassword(data) {
    const res = await apiClient.post("/api/auth/change-password", data);
    return res.data;
  },

  logout() {
    localStorage.removeItem("bt_access_token");
    localStorage.removeItem("bt_user");
  },

  saveSession(token, user) {
    localStorage.setItem("bt_access_token", token);
    localStorage.setItem("bt_user", JSON.stringify(user));
  },

  getStoredUser() {
    const raw = localStorage.getItem("bt_user");
    return raw ? JSON.parse(raw) : null;
  },

  isAuthenticated() {
    return !!localStorage.getItem("bt_access_token");
  },
};
