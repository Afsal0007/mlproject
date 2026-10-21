/**
 * api.js — Axios client for PlacementAI Flask backend.
 *
 * All components MUST use this module for data fetching.
 * supabase-js is used ONLY for auth (sign-in / sign-out / session).
 * The access token is attached here automatically.
 */
import axios from "axios";
import { supabase } from "../lib/supabase.js";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api",
  headers: { "Content-Type": "application/json" },
  withCredentials: false,
});

// Attach the latest Supabase JWT to every Flask request.
api.interceptors.request.use(async (config) => {
  if (import.meta.env.VITE_DEV_BYPASS_AUTH !== "true" && supabase) {
    const { data } = await supabase.auth.getSession();
    const token = data.session?.access_token;
    if (token) config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

function normalizeError(error) {
  const payload = error.response?.data?.error;
  error.apiError = {
    code: payload?.code || (error.response ? `http_${error.response.status}` : "network_error"),
    message: payload?.message || error.message || "Request failed",
    details: payload?.details ?? null,
  };
  return error;
}

// Retry a single expired access token after refreshing the persisted session.
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && supabase && original && !original._sessionRetry) {
      original._sessionRetry = true;
      const { data, error: refreshError } = await supabase.auth.refreshSession();
      if (!refreshError && data.session?.access_token) {
        original.headers = original.headers || {};
        original.headers.Authorization = `Bearer ${data.session.access_token}`;
        return api(original);
      }
      await supabase.auth.signOut();
      if (window.location.pathname !== "/login") window.location.assign("/login");
    }
    return Promise.reject(normalizeError(error));
  }
);

export default api;
export { normalizeError };
