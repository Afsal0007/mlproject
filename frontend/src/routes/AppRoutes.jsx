import { Navigate, Route, Routes } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import AppLayout from "../layouts/AppLayout.jsx";
import AdminPage from "../pages/AdminPage.jsx";
import AnalyticsPage from "../pages/AnalyticsPage.jsx";
import DashboardPage from "../pages/DashboardPage.jsx";
import LoginPage from "../pages/LoginPage.jsx";
import NotFoundPage from "../pages/NotFoundPage.jsx";
import PredictionPage from "../pages/PredictionPage.jsx";
import SkillsPage from "../pages/SkillsPage.jsx";
import StudentsPage from "../pages/StudentsPage.jsx";
import ProtectedRoute from "./ProtectedRoute.jsx";

function RootRedirect() {
  const { session, profile, loading } = useAuth();
  if (loading) return null;
  return <Navigate to={session && profile ? "/" : "/login"} replace />;
}

export default function AppRoutes() {
  return <Routes>
    <Route path="/login" element={<LoginPage />} />
    <Route element={<ProtectedRoute />}>
      <Route element={<AppLayout />}>
        <Route index element={<DashboardPage />} />
        <Route path="students" element={<StudentsPage />} />
        <Route path="prediction" element={<PredictionPage />} />
        <Route path="analytics" element={<AnalyticsPage />} />
        <Route path="skills" element={<SkillsPage />} />
        <Route element={<ProtectedRoute allowedRoles={["super_admin"]} />}>
          <Route path="admin" element={<AdminPage />} />
        </Route>
        <Route path="404" element={<NotFoundPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Route>
    <Route path="*" element={<RootRedirect />} />
  </Routes>;
}
