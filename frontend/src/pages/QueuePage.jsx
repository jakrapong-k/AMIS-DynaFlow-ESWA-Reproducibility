import { useEffect, useState } from 'react';
import { api } from '../services/api';

function valueOrFallback(value) {
  return value === null || value === undefined || value === '' ? 'N/A' : String(value);
}

function getWaitingCount(item) {
  return item.waiting_count ?? item.waitingCount ?? item.queue_length ?? item.queueLength;
}

export default function QueuePage() {
  const [runs, setRuns] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchQueueStatus() {
      try {
        const data = await api.listRuns();
        const items = data.items || [];
        setRuns(items);
        setTotal(data.total ?? items.length);
      } catch (_err) {
        setError('Unable to reach backend queue/status API. Please ensure the backend is running.');
      } finally {
        setLoading(false);
      }
    }

    fetchQueueStatus();
  }, []);

  return (
    <section>
      <h2>Queue / Status</h2>
      {loading ? (
        <p>Loading queue status...</p>
      ) : error ? (
        <p>{error}</p>
      ) : runs.length === 0 ? (
        <div className="card">
          <strong>Queue Summary</strong>
          <p>No queued or active runs were returned by the backend.</p>
          <p>Total items: {total}</p>
        </div>
      ) : (
        <table className="table card">
          <thead>
            <tr>
              <th>Run ID</th>
              <th>Queue</th>
              <th>Station</th>
              <th>Status</th>
              <th>Waiting Count</th>
              <th>Created At</th>
            </tr>
          </thead>
          <tbody>
            {runs.map((item, index) => (
              <tr key={item.run_id || item.id || `${item.queue || 'queue'}-${index}`}>
                <td>{valueOrFallback(item.run_id || item.id)}</td>
                <td>{valueOrFallback(item.queue || item.queue_name || item.run_type)}</td>
                <td>{valueOrFallback(item.station || item.station_name)}</td>
                <td>{valueOrFallback(item.status)}</td>
                <td>{valueOrFallback(getWaitingCount(item))}</td>
                <td>{valueOrFallback(item.created_at)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}
