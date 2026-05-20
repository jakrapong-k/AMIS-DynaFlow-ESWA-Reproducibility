import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Layout from './components/Layout';
import DashboardPage from './pages/DashboardPage';
import LoginPage from './pages/LoginPage';
import QueuePage from './pages/QueuePage';
import MetricsPage from './pages/MetricsPage';
import ArtifactsPage from './pages/ArtifactsPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<DashboardPage />} />
          <Route path="login" element={<LoginPage />} />
          <Route path="queue" element={<QueuePage />} />
          <Route path="metrics" element={<MetricsPage />} />
          <Route path="artifacts" element={<ArtifactsPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
