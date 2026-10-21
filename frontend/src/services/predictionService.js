import api from "./api.js";

export const predictionService = {
  predict: (features) => api.post("/predictions", features).then(({ data }) => data),
  batch: (payload) => api.post("/predictions/batch", payload).then(({ data }) => data),
};
