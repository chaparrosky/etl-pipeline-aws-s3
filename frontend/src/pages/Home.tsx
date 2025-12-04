import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { listTopFighters, getApiStats, Fighter } from '../services/api';

const Home = () => {
  const [topFighters, setTopFighters] = useState<Fighter[]>([]);
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [fighters, apiStats] = await Promise.all([
          listTopFighters(6),
          getApiStats()
        ]);
        setTopFighters(fighters);
        setStats(apiStats);
      } catch (error) {
        console.error('Error loading data:', error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  return (
    <div>
      {/* Hero Section */}
      <section className="hero">
        <div className="container">
          <h1>UFC Fight Analytics & Predictions</h1>
          <p>AI-Powered Predictions, Betting Value Analysis & Fighter Statistics</p>
          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginTop: '2rem' }}>
            <Link to="/search" className="btn btn-primary">Search Fighters</Link>
            <Link to="/head-to-head" className="btn btn-secondary">Compare Fighters</Link>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="features">
        <div className="container">
          <h2 style={{ textAlign: 'center', marginBottom: '3rem', fontSize: '2rem' }}>
            Features
          </h2>
          <div className="grid grid-3">
            <div className="card feature-card">
              <div className="feature-icon">🔍</div>
              <h3>Fighter Database</h3>
              <p style={{ color: '#888' }}>
                Search and explore detailed statistics for every UFC fighter
              </p>
            </div>
            <div className="card feature-card">
              <div className="feature-icon">⚔️</div>
              <h3>Head-to-Head Analysis</h3>
              <p style={{ color: '#888' }}>
                Compare any two fighters with AI-powered insights
              </p>
            </div>
            <div className="card feature-card">
              <div className="feature-icon">🤖</div>
              <h3>Fight Predictions</h3>
              <p style={{ color: '#888' }}>
                ML-powered predictions with win probabilities
              </p>
            </div>
            <div className="card feature-card">
              <div className="feature-icon">💰</div>
              <h3>Betting Value Finder</h3>
              <p style={{ color: '#888' }}>
                Discover undervalued bets before the odds change
              </p>
              <span className="premium-badge" style={{ marginTop: '1rem', display: 'inline-block' }}>Premium</span>
            </div>
            <div className="card feature-card">
              <div className="feature-icon">📊</div>
              <h3>Fight Card Analysis</h3>
              <p style={{ color: '#888' }}>
                Analyze entire UFC events with detailed predictions
              </p>
              <span className="premium-badge" style={{ marginTop: '1rem', display: 'inline-block' }}>Premium</span>
            </div>
            <div className="card feature-card">
              <div className="feature-icon">📈</div>
              <h3>Historical Trends</h3>
              <p style={{ color: '#888' }}>
                Track fighter performance over time
              </p>
              <span className="premium-badge" style={{ marginTop: '1rem', display: 'inline-block' }}>Premium</span>
            </div>
          </div>
        </div>
      </section>

      {/* Stats */}
      {stats && (
        <section style={{ padding: '3rem 0', background: '#1a1a1a' }}>
          <div className="container">
            <div className="grid grid-3" style={{ textAlign: 'center' }}>
              <div>
                <div className="stat-value">{stats.total_fighters.toLocaleString()}</div>
                <div className="stat-label">UFC Fighters</div>
              </div>
              <div>
                <div className="stat-value">{stats.total_fights.toLocaleString()}</div>
                <div className="stat-label">Fights Analyzed</div>
              </div>
              <div>
                <div className="stat-value">98%</div>
                <div className="stat-label">Prediction Accuracy</div>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Top Fighters */}
      <section style={{ padding: '4rem 0' }}>
        <div className="container">
          <h2 style={{ textAlign: 'center', marginBottom: '2rem', fontSize: '2rem' }}>
            Top Fighters
          </h2>
          {loading ? (
            <div className="loading">
              <div className="spinner"></div>
              <p>Loading fighters...</p>
            </div>
          ) : (
            <div className="grid grid-3">
              {topFighters.map((fighter) => (
                <Link to={`/fighter/${fighter.id}`} key={fighter.id} style={{ textDecoration: 'none' }}>
                  <div className="card fighter-card">
                    <div className="fighter-name">{fighter.name}</div>
                    <div className="record">
                      {fighter.wins}-{fighter.losses}-{fighter.draws}
                    </div>
                    <div className="fighter-stats">
                      <div className="stat">
                        <div className="stat-value">{fighter.win_percentage.toFixed(1)}%</div>
                        <div className="stat-label">Win Rate</div>
                      </div>
                      <div className="stat">
                        <div className="stat-value">{fighter.total_fights}</div>
                        <div className="stat-label">Fights</div>
                      </div>
                      <div className="stat">
                        <div className="stat-value">{fighter.ko_tko_wins}</div>
                        <div className="stat-label">KO/TKO</div>
                      </div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* CTA */}
      <section style={{ padding: '4rem 0', background: 'linear-gradient(135deg, #d32f2f 0%, #8b0000 100%)', textAlign: 'center' }}>
        <div className="container">
          <h2 style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>
            Ready to Gain the Edge?
          </h2>
          <p style={{ fontSize: '1.25rem', marginBottom: '2rem', opacity: 0.9 }}>
            Get unlimited access to predictions, betting analysis, and more
          </p>
          <button className="btn btn-primary" style={{ background: 'white', color: '#d32f2f', fontSize: '1.125rem' }}>
            Start Free Trial - $14.99/month
          </button>
        </div>
      </section>
    </div>
  );
};

export default Home;
