import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getFighterById, FighterProfile as FighterProfileType } from '../services/api';

const FighterProfile = () => {
  const { id } = useParams<{ id: string }>();
  const [fighter, setFighter] = useState<FighterProfileType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadFighter = async () => {
      if (!id) return;

      try {
        const data = await getFighterById(parseInt(id));
        setFighter(data);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Fighter not found');
      } finally {
        setLoading(false);
      }
    };

    loadFighter();
  }, [id]);

  if (loading) {
    return (
      <div className="loading" style={{ minHeight: 'calc(100vh - 200px)' }}>
        <div className="spinner"></div>
        <p>Loading fighter...</p>
      </div>
    );
  }

  if (error || !fighter) {
    return (
      <div className="container" style={{ padding: '3rem 0', textAlign: 'center' }}>
        <h2 style={{ color: '#f44336' }}>Fighter Not Found</h2>
        <p style={{ color: '#888', marginTop: '1rem' }}>{error}</p>
        <Link to="/search" className="btn btn-primary" style={{ marginTop: '2rem' }}>
          Back to Search
        </Link>
      </div>
    );
  }

  const finishRate = fighter.total_fights > 0
    ? ((fighter.ko_tko_wins + fighter.submission_wins) / fighter.total_fights * 100).toFixed(1)
    : '0';

  return (
    <div style={{ padding: '3rem 0' }}>
      <div className="container">
        {/* Header */}
        <div style={{ marginBottom: '3rem' }}>
          <h1 style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>
            {fighter.name}
          </h1>
          <div style={{ fontSize: '1.5rem', color: '#888' }}>
            <span style={{ color: '#4caf50', fontWeight: 'bold' }}>{fighter.wins}W</span>
            {' - '}
            <span style={{ color: '#f44336', fontWeight: 'bold' }}>{fighter.losses}L</span>
            {fighter.draws > 0 && <> - <span>{fighter.draws}D</span></>}
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-3" style={{ marginBottom: '3rem' }}>
          <div className="card">
            <div className="stat">
              <div className="stat-value">{fighter.win_percentage.toFixed(1)}%</div>
              <div className="stat-label">Win Rate</div>
            </div>
          </div>
          <div className="card">
            <div className="stat">
              <div className="stat-value">{fighter.total_fights}</div>
              <div className="stat-label">Total Fights</div>
            </div>
          </div>
          <div className="card">
            <div className="stat">
              <div className="stat-value">{finishRate}%</div>
              <div className="stat-label">Finish Rate</div>
            </div>
          </div>
        </div>

        {/* Win Methods */}
        <div className="card" style={{ marginBottom: '3rem' }}>
          <h2 style={{ marginBottom: '1.5rem' }}>Win Methods</h2>
          <div className="grid grid-3">
            <div className="stat">
              <div className="stat-value">{fighter.ko_tko_wins}</div>
              <div className="stat-label">KO/TKO Wins</div>
            </div>
            <div className="stat">
              <div className="stat-value">{fighter.submission_wins}</div>
              <div className="stat-label">Submission Wins</div>
            </div>
            <div className="stat">
              <div className="stat-value">{fighter.decision_wins}</div>
              <div className="stat-label">Decision Wins</div>
            </div>
          </div>
        </div>

        {/* Recent Fights */}
        {fighter.recent_fights && fighter.recent_fights.length > 0 && (
          <div className="card">
            <h2 style={{ marginBottom: '1.5rem' }}>Recent Fights</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {fighter.recent_fights.map((fight) => {
                const isFighterRed = fight.red_fighter_name === fighter.name;
                const opponent = isFighterRed ? fight.blue_fighter_name : fight.red_fighter_name;
                const won = (isFighterRed && fight.winner === 'Red') || (!isFighterRed && fight.winner === 'Blue');

                return (
                  <div
                    key={fight.id}
                    style={{
                      padding: '1rem',
                      background: '#111',
                      borderRadius: '8px',
                      borderLeft: `4px solid ${won ? '#4caf50' : '#f44336'}`
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <div>
                        <div style={{ fontSize: '1.125rem', fontWeight: 'bold', marginBottom: '0.25rem' }}>
                          {won ? 'Win' : 'Loss'} vs {opponent}
                        </div>
                        <div style={{ color: '#888', fontSize: '0.875rem' }}>
                          {fight.finish_method && fight.finish_round
                            ? `${fight.finish_method} • Round ${fight.finish_round}`
                            : fight.finish_method || 'Decision'}
                        </div>
                      </div>
                      <div style={{ textAlign: 'right', color: '#888', fontSize: '0.875rem' }}>
                        {new Date(fight.date).toLocaleDateString()}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Actions */}
        <div style={{ marginTop: '3rem', display: 'flex', gap: '1rem', justifyContent: 'center' }}>
          <Link to="/search" className="btn btn-secondary">
            ← Back to Search
          </Link>
          <Link to="/head-to-head" state={{ fighter1: fighter.name }} className="btn btn-primary">
            Compare with Another Fighter
          </Link>
        </div>
      </div>
    </div>
  );
};

export default FighterProfile;
