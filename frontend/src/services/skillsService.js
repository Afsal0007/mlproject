import api from "./api.js";

export const skillsService = {
  assess: (studentId, assessment) => api.post(`/students/${studentId}/skills`, assessment).then(({ data }) => data),
  summary: (params = {}) => api.get("/skills/summary", { params }).then(({ data }) => data),
};
