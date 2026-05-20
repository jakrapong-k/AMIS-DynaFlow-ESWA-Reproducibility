import { NavLink, Outlet } from 'react-router-dom';

const links = [
  ['/', 'Dashboard'],
  ['/login', 'Login'],
  ['/queue', 'Queue/Status'],
  ['/metrics', 'Metrics'],
  ['/artifacts', 'Artifacts'],
];

export default function Layout() {
  return (
    <div className="layout">
      <aside className="sidebar">
        <h3>AMIS DynaFlow</h3>
        {links.map(([to, label]) => (
          <NavLink key={to} to={to} end>{label}</NavLink>
        ))}
      </aside>
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
