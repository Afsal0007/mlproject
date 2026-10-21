import api from "./api.js";

export const studentsService = {
  list: (params = {}) => api.get("/students", { params }).then(({ data }) => data),
  get: (id) => api.get(`/students/${id}`).then(({ data }) => data),
  create: (student) => api.post("/students", student).then(({ data }) => data),
  update: (id, changes) => api.put(`/students/${id}`, changes).then(({ data }) => data),
  remove: (id) => api.delete(`/students/${id}`),
  addSkills: (id, assessment) => api.post(`/students/${id}/skills`, assessment).then(({ data }) => data),
  template: () => api.get("/students/template.csv", { responseType: "blob" }),
  import: (file, options = {}) => {
    const form = new FormData();
    form.append("file", file);
    return api.post("/students/import", form, { params: options }).then(({ data }) => data);
  },
  export: (params = {}) => api.get("/students/export.csv", { params, responseType: "blob" }),
};
