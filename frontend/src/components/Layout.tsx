import { Link } from 'react-router-dom';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  return (
    <div>
      <nav className="navbar">
        <div className="container nav-content">
          <Link to="/" className="nav-brand">
            🥊 UFC Analytics
          </Link>
          <ul className="nav-links">
            <li><Link to="/search">Search Fighters</Link></li>
            <li><Link to="/head-to-head">Head-to-Head</Link></li>
            <li><Link to="/premium"><span className="premium-badge">Go Premium</span></Link></li>
          </ul>
        </div>
      </nav>
      <main>
        {children}
      </main>
      <footer style={{ textAlign: 'center', padding: '2rem', color: '#666' }}>
        <p>UFC Analytics &copy; 2024 | AI-Powered Fight Predictions</p>
      </footer>
    </div>
  );
};

export default Layout;
