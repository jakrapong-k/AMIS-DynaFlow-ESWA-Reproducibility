import { useEffect, useState } from 'react';

const METRICS_ENDPOINT = 'http://127.0.0.1:8000/api/v1/runs/run_20260520_052548/metrics';

export default function MetricsPage() {
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchMetrics() {
      try {
        const res = await fetch(METRICS_ENDPOINT);
        if (!res.ok) {
          throw new Error(`Failed to fetch metrics (${res.status})`);
        }
        const data = await res.json();
        setMetrics(data.metrics || []);
      } catch (_err) {
        setError('Unable to reach backend metrics API. Please ensure the backend is running.');
      } finally {
        setLoading(false);
      }
    }

    fetchMetrics();
  }, []);

  return (
    <section>
      <h2>Metrics</h2>
      {loading ? (
        <p>Loading metrics...</p>
      ) : error ? (
        <p>{error}</p>
      ) : (
        <table className="table card">
          <thead>
            <tr>
              <th>Name</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            {metrics.map((metric) => (
              <tr key={metric.name}>
                <td>{metric.name}</td>
                <td>{metric.value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}
