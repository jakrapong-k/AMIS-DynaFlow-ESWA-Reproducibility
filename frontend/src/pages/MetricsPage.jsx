import { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function MetricsPage() {
  const [metrics, setMetrics] = useState([]);
  useEffect(() => { api.runMetrics().then((d) => setMetrics(d.metrics || [])).catch(() => setMetrics([])); }, []);

  return (
    <section>
      <h2>Metrics</h2>
      <table className="table card"><thead><tr><th>Name</th><th>Value</th></tr></thead><tbody>{metrics.map((m) => <tr key={m.name}><td>{m.name}</td><td>{m.value}</td></tr>)}</tbody></table>
    </section>
  );
}
