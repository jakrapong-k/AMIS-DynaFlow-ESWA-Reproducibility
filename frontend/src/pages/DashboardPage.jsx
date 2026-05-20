import { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function DashboardPage() {
  const [summary, setSummary] = useState(null);
  useEffect(() => { api.dashboardSummary().then(setSummary).catch(() => setSummary({})); }, []);

  return <section><h2>Dashboard</h2><div className="grid">{summary && Object.entries(summary).map(([k,v]) => <div className="card" key={k}><strong>{k}</strong><div>{String(v)}</div></div>)}</div></section>;
}
