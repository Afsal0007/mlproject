import api from "./api.js";

export const adminService = {
  settings: () => api.get("/settings").then(({ data }) => data),
  updateSettings: (settings) => api.put("/settings", settings).then(({ data }) => data),
  users: () => api.get("/admin/users").then(({ data }) => data),
  audit: (params = {}) => api.get("/admin/audit", { params }).then(({ data }) => data),
};
