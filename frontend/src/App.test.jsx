import { render, screen } from '@testing-library/react';
import App from './App';

describe('App shell', () => {
  it('renders sidebar navigation', () => {
    render(<App />);
    expect(screen.getByText('AMIS DynaFlow')).toBeInTheDocument();
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Metrics')).toBeInTheDocument();
  });
});
