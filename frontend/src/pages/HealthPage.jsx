/**
 * HealthPage — Temporary Phase-1 diagnostic page.
 *
 * Calls GET /api/health and renders the raw JSON response.
 * This page will be removed once the real dashboard is built in Phase 2+.
 */
import { useEffect, useState } from "react";
import api from "../services/api.js";

export default function HealthPage() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get("/health")
      .then((res) => setData(res.data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <main className="min-h-screen bg-surface flex items-center justify-center px-space-lg">
      <div className="w-full max-w-lg bg-surface-container-lowest rounded-xl shadow-sm p-space-lg">
        {/* Header */}
        <div className="flex items-center gap-space-sm mb-space-lg">
          <span className="material-symbols-outlined text-[28px] text-secondary">
            monitor_heart
          </span>
          <div>
            <h1 className="font-headline-md text-headline-md text-primary">
              API Health Check
            </h1>
            <p className="font-body-sm text-body-sm text-on-surface-variant">
              Phase 1 scaffold — calls <code className="font-label-sm text-label-sm bg-surface-container px-1 rounded">GET /api/health</code>
            </p>
          </div>
        </div>

        {/* Status */}
        {loading && (
          <div className="flex items-center gap-space-sm text-on-surface-variant">
            <span className="w-2 h-2 rounded-full bg-secondary animate-pulse" />
            <span className="font-body-sm text-body-sm">Contacting backend…</span>
          </div>
        )}

        {error && (
          <div className="rounded-lg bg-error-container p-space-md">
            <p className="font-label-sm text-label-sm text-on-error-container font-semibold mb-1">
              Connection Failed
            </p>
            <p className="font-body-sm text-body-sm text-on-error-container">{error}</p>
            <p className="font-body-sm text-body-sm text-on-error-container mt-2 opacity-75">
              Make sure the Flask backend is running on <code>http://127.0.0.1:5000</code>
            </p>
          </div>
        )}

        {data && (
          <>
            <div className="flex items-center gap-space-xs mb-space-md">
              <span className="w-2 h-2 rounded-full bg-secondary" />
              <span className="font-label-sm text-label-sm text-secondary font-semibold uppercase tracking-wider">
                Backend Reachable
              </span>
            </div>
            <pre className="bg-surface-container rounded-lg p-space-md font-label-md text-label-md text-on-surface overflow-auto tabular-nums">
              {JSON.stringify(data, null, 2)}
            </pre>
          </>
        )}
      </div>
    </main>
  );
}
