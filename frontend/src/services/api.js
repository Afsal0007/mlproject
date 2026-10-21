/**
 * api.js — Axios client for PlacementAI Flask backend.
 *
 * All components MUST use this module for data fetching.
 * supabase-js is used ONLY for auth (sign-in / sign-out / session).
 * The access token is attached here automatically.
 */
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api",
  headers: { "Content-Type": "application/json" },
  withCredentials: false,
});

// Attach Supabase JWT on every outgoing request.
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("sb-access-token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Global 401 handler: clear session and redirect to login.
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("sb-access-token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default api;
