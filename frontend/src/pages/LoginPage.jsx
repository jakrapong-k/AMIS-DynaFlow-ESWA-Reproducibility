import { useState } from 'react';
import { api } from '../services/api';

export default function LoginPage() {
  const [email, setEmail] = useState('operator@example.com');
  const [password, setPassword] = useState('password');
  const [token, setToken] = useState('');

  const onSubmit = async (e) => {
    e.preventDefault();
    const result = await api.login(email, password);
    setToken(result.access_token);
  };

  return (
    <section>
      <h2>Mock Login</h2>
      <form className="card" onSubmit={onSubmit}>
        <div><input aria-label="email" value={email} onChange={(e) => setEmail(e.target.value)} /></div>
        <div><input aria-label="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} /></div>
        <button type="submit">Sign In</button>
      </form>
      {token && <p>Token: {token}</p>}
    </section>
  );
}
