import { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function ArtifactsPage() {
  const [artifacts, setArtifacts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchArtifacts() {
      try {
        const data = await api.runArtifacts();
        setArtifacts(data.artifacts || []);
      } catch (_err) {
        setError('Unable to reach backend artifacts API. Please ensure the backend is running.');
      } finally {
        setLoading(false);
      }
    }

    fetchArtifacts();
  }, []);

  return (
    <section>
      <h2>Artifacts</h2>
      {loading ? (
        <p>Loading artifacts...</p>
      ) : error ? (
        <p>{error}</p>
      ) : artifacts.length === 0 ? (
        <p>No artifacts were returned for this run.</p>
      ) : (
        <table className="table card">
          <thead>
            <tr>
              <th>Type</th>
              <th>Path</th>
              <th>Checksum</th>
            </tr>
          </thead>
          <tbody>
            {artifacts.map((artifact) => (
              <tr key={`${artifact.type}-${artifact.path}`}>
                <td>{artifact.type || 'N/A'}</td>
                <td>{artifact.path || 'N/A'}</td>
                <td>{artifact.checksum || 'N/A'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}
