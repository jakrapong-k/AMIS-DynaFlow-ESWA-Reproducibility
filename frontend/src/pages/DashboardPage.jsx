import { useEffect, useState } from 'react';

const RUN_ID = 'run_20260520_052548';
const METRICS_ENDPOINT = `http://127.0.0.1:8000/api/v1/runs/${RUN_ID}/metrics`;
const ARTIFACTS_ENDPOINT = `http://127.0.0.1:8000/api/v1/runs/${RUN_ID}/artifacts`;

function getMetricValue(metrics, name) {
  return metrics.find((metric) => metric.name === name)?.value ?? 'N/A';
}

export default function DashboardPage() {
  const [kpis, setKpis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchDashboardSummary() {
      try {
        const [metricsRes, artifactsRes] = await Promise.all([
          fetch(METRICS_ENDPOINT),
          fetch(ARTIFACTS_ENDPOINT),
        ]);

        if (!metricsRes.ok || !artifactsRes.ok) {
          throw new Error('Failed to fetch dashboard data');
        }

        const [metricsData, artifactsData] = await Promise.all([
          metricsRes.json(),
          artifactsRes.json(),
        ]);
        const metrics = metricsData.metrics || [];
        const artifacts = artifactsData.artifacts || [];

        setKpis([
          { label: 'Run ID', value: RUN_ID },
          { label: 'MAE', value: getMetricValue(metrics, 'mae') },
          { label: 'Service Level', value: getMetricValue(metrics, 'service_level') },
          { label: 'Utilization', value: getMetricValue(metrics, 'utilization') },
          { label: 'Artifact Count', value: artifacts.length },
        ]);
      } catch (_err) {
        setError('Unable to reach backend dashboard APIs. Please ensure the backend is running.');
      } finally {
        setLoading(false);
      }
    }

    fetchDashboardSummary();
  }, []);

  return (
    <section>
      <h2>Dashboard</h2>
      {loading ? (
        <p>Loading dashboard summary...</p>
      ) : error ? (
        <p>{error}</p>
      ) : (
        <div className="grid">
          {kpis.map((kpi) => (
            <div className="card" key={kpi.label}>
              <strong>{kpi.label}</strong>
              <div>{String(kpi.value)}</div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
