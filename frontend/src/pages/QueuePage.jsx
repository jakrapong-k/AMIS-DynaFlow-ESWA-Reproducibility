import { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function QueuePage() {
  const [runs, setRuns] = useState([]);
  useEffect(() => { api.listRuns().then((d) => setRuns(d.items || [])).catch(() => setRuns([])); }, []);

  return (
    <section>
      <h2>Queue / Status</h2>
      <div className="card">
        <p>Showing mock run queue from backend stub.</p>
        <p>Total items: {runs.length}</p>
      </div>
    </section>
  );
}
