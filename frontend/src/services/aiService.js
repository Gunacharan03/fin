import apiClient from "./apiClient";

export const aiService = {
  async getExpenseAnalysis() {
    const res = await apiClient.get("/api/ai/expense-analysis");
    return res.data;
  },

  async getSavingsRecommendation() {
    const res = await apiClient.get("/api/ai/savings-recommendation");
    return res.data;
  },

  async getGoalPrediction() {
    const res = await apiClient.get("/api/ai/goal-prediction");
    return res.data;
  },

  async getReminderAlert() {
    const res = await apiClient.get("/api/ai/reminder-alert");
    return res.data;
  },

  async getFinancialHealthScore() {
    const res = await apiClient.get("/api/ai/financial-health-score");
    return res.data;
  },

  async getMonthlyReport() {
    const res = await apiClient.get("/api/ai/monthly-report");
    return res.data;
  },

  async sendChatMessage(message) {
    const res = await apiClient.post("/api/ai/chat", { message });
    return res.data;
  },

  async getFullReport() {
    const res = await apiClient.get("/api/ai/full-report");
    return res.data;
  },

  async getHistory(limit = 20) {
    const res = await apiClient.get("/api/ai/history", { params: { limit } });
    return res.data;
  },
};

export const analyticsService = {
  async getSummary(params = {}) {
    const res = await apiClient.get("/api/analytics/summary", { params });
    return res.data;
  },

  async getCategoryBreakdown(type = "expense") {
    const res = await apiClient.get("/api/analytics/category-breakdown", { params: { type } });
    return res.data;
  },

  async getMonthlyTrend(months = 6) {
    const res = await apiClient.get("/api/analytics/monthly-trend", { params: { months } });
    return res.data;
  },

  async getDashboard() {
    const res = await apiClient.get("/api/analytics/dashboard");
    return res.data;
  },
};
