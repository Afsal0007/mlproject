import api from "./api.js";

export const analyticsService = {
  summary: (params = {}) => api.get("/analytics/summary", { params }).then(({ data }) => data),
  reports: (params = {}) => api.get("/analytics/reports", { params }).then(({ data }) => data),
};
