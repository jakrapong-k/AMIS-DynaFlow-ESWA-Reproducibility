import { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function ArtifactsPage() {
  const [artifacts, setArtifacts] = useState([]);
  useEffect(() => { api.runArtifacts().then((d) => setArtifacts(d.artifacts || [])).catch(() => setArtifacts([])); }, []);

  return (
    <section>
      <h2>Artifacts</h2>
      <ul className="card">
        {artifacts.map((a) => <li key={a.path}>{a.type}: {a.path}</li>)}
      </ul>
    </section>
  );
}
