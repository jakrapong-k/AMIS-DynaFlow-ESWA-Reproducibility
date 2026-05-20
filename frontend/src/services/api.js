const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });
  if (!res.ok) {
    throw new Error(`API error ${res.status}`);
  }
  return res.json();
}

export const api = {
  login: (email, password) => request('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }),
  dashboardSummary: () => request('/dashboard/summary'),
  listRuns: () => request('/runs'),
  runMetrics: (runId = 'run_mock_001') => request(`/runs/${runId}/metrics`),
  runArtifacts: (runId = 'run_mock_001') => request(`/runs/${runId}/artifacts`),
};
