/**
 * AppRoutes — top-level route definitions.
 * Phase 1: only the health-check dev page is wired.
 * Remaining routes will be added in Phase 2+.
 */
import { Routes, Route, Navigate } from "react-router-dom";
import HealthPage from "../pages/HealthPage.jsx";

export default function AppRoutes() {
  return (
    <Routes>
      {/* Temporary Phase-1 health check page */}
      <Route path="/health" element={<HealthPage />} />

      {/* Default: redirect to health check for now */}
      <Route path="*" element={<Navigate to="/health" replace />} />
    </Routes>
  );
}
