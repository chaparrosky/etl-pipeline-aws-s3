import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { compareFighters, HeadToHeadResponse } from '../services/api';

const HeadToHead = () => {
  const location = useLocation();
  const [fighter1Name, setFighter1Name] = useState('');
  const [fighter2Name, setFighter2Name] = useState('');
  const [comparison, setComparison] = useState<HeadToHeadResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (location.state?.fighter1) {
      setFighter1Name(location.state.fighter1);
    }
  }, [location]);

  const handleCompare = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!fighter1Name.trim() || !fighter2Name.trim()) return;

    setLoading(true);
    setError(null);
    setComparison(null);

    try {
      const result = await compareFighters(fighter1Name, fighter2Name);
      setComparison(result);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error comparing fighters');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '3rem 0', minHeight: 'calc(100vh - 200px)' }}>
      <div className="container">
        <h1 style={{ textAlign: 'center', marginBottom: '2rem' }}>
          Head-to-Head Comparison
        </h1>

        {/* Input Form */}
        <form onSubmit={handleCompare} style={{ maxWidth: '800px', margin: '0 auto 3rem' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr auto 1fr', gap: '1rem', alignItems: 'end' }}>
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', color: '#888' }}>
                Fighter 1
              </label>
              <input
                type="text"
                className="search-input"
                placeholder="e.g., Jon Jones"
                value={fighter1Name}
                onChange={(e) => setFighter1Name(e.target.value)}
              />
            </div>
            <div style={{ fontSize: '2rem', color: '#d32f2f', paddingBottom: '1rem' }}>
              VS
            </div>
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', color: '#888' }}>
                Fighter 2
              </label>
              <input
                type="text"
                className="search-input"
                placeholder="e.g., Daniel Cormier"
                value={fighter2Name}
                onChange={(e) => setFighter2Name(e.target.value)}
              />
            </div>
          </div>
          <button
            type="submit"
            className="btn btn-primary"
            style={{ width: '100%', marginTop: '1rem' }}
            disabled={loading}
          >
            {loading ? 'Comparing...' : 'Compare Fighters'}
          </button>
        </form>

        {/* Loading */}
        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Analyzing matchup...</p>
          </div>
        )}

        {/* Error */}
        {error && (
          <div style={{ textAlign: 'center', color: '#f44336', padding: '2rem' }}>
            <p style={{ fontSize: '1.25rem' }}>{error}</p>
          </div>
        )}

        {/* Comparison Results */}
        {comparison && !loading && (
          <div>
            {/* Fighter Cards */}
            <div className="comparison">
              {/* Fighter 1 */}
              <div className="card" style={{ height: '100%' }}>
                <h2 style={{ fontSize: '2rem', marginBottom: '1rem', color: '#d32f2f' }}>
                  {comparison.fighter1.name}
                </h2>
                <div style={{ fontSize: '1.5rem', marginBottom: '1.5rem', color: '#4caf50' }}>
                  {comparison.fighter1.wins}-{comparison.fighter1.losses}-{comparison.fighter1.draws}
                </div>
                <div className="fighter-stats">
                  <div className="stat">
                    <div className="stat-value">{comparison.fighter1.win_percentage.toFixed(1)}%</div>
                    <div className="stat-label">Win Rate</div>
                  </div>
                  <div className="stat">
                    <div className="stat-value">{comparison.fighter1.total_fights}</div>
                    <div className="stat-label">Fights</div>
                  </div>
                </div>
                <div style={{ marginTop: '2rem' }}>
                  <div style={{ marginBottom: '0.5rem' }}>
                    <strong>KO/TKO Wins:</strong> {comparison.fighter1.ko_tko_wins}
                  </div>
                  <div style={{ marginBottom: '0.5rem' }}>
                    <strong>Submission Wins:</strong> {comparison.fighter1.submission_wins}
                  </div>
                  <div>
                    <strong>Decision Wins:</strong> {comparison.fighter1.decision_wins}
                  </div>
                </div>
              </div>

              <div className="vs-divider">VS</div>

              {/* Fighter 2 */}
              <div className="card" style={{ height: '100%' }}>
                <h2 style={{ fontSize: '2rem', marginBottom: '1rem', color: '#d32f2f' }}>
                  {comparison.fighter2.name}
                </h2>
                <div style={{ fontSize: '1.5rem', marginBottom: '1.5rem', color: '#4caf50' }}>
                  {comparison.fighter2.wins}-{comparison.fighter2.losses}-{comparison.fighter2.draws}
                </div>
                <div className="fighter-stats">
                  <div className="stat">
                    <div className="stat-value">{comparison.fighter2.win_percentage.toFixed(1)}%</div>
                    <div className="stat-label">Win Rate</div>
                  </div>
                  <div className="stat">
                    <div className="stat-value">{comparison.fighter2.total_fights}</div>
                    <div className="stat-label">Fights</div>
                  </div>
                </div>
                <div style={{ marginTop: '2rem' }}>
                  <div style={{ marginBottom: '0.5rem' }}>
                    <strong>KO/TKO Wins:</strong> {comparison.fighter2.ko_tko_wins}
                  </div>
                  <div style={{ marginBottom: '0.5rem' }}>
                    <strong>Submission Wins:</strong> {comparison.fighter2.submission_wins}
                  </div>
                  <div>
                    <strong>Decision Wins:</strong> {comparison.fighter2.decision_wins}
                  </div>
                </div>
              </div>
            </div>

            {/* Advantages */}
            {(comparison.fighter1_advantages.length > 0 || comparison.fighter2_advantages.length > 0) && (
              <div className="grid grid-2" style={{ marginTop: '2rem' }}>
                <div className="card">
                  <h3 style={{ marginBottom: '1rem', color: '#4caf50' }}>
                    {comparison.fighter1.name} Advantages
                  </h3>
                  {comparison.fighter1_advantages.length > 0 ? (
                    <ul style={{ listStyle: 'none', padding: 0 }}>
                      {comparison.fighter1_advantages.map((adv, idx) => (
                        <li key={idx} style={{ marginBottom: '0.5rem', paddingLeft: '1.5rem', position: 'relative' }}>
                          <span style={{ position: 'absolute', left: 0 }}>✓</span>
                          {adv}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p style={{ color: '#888' }}>No significant advantages</p>
                  )}
                </div>
                <div className="card">
                  <h3 style={{ marginBottom: '1rem', color: '#4caf50' }}>
                    {comparison.fighter2.name} Advantages
                  </h3>
                  {comparison.fighter2_advantages.length > 0 ? (
                    <ul style={{ listStyle: 'none', padding: 0 }}>
                      {comparison.fighter2_advantages.map((adv, idx) => (
                        <li key={idx} style={{ marginBottom: '0.5rem', paddingLeft: '1.5rem', position: 'relative' }}>
                          <span style={{ position: 'absolute', left: 0 }}>✓</span>
                          {adv}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p style={{ color: '#888' }}>No significant advantages</p>
                  )}
                </div>
              </div>
            )}

            {/* Prediction */}
            {comparison.prediction && (
              <div className="prediction-card" style={{ marginTop: '2rem' }}>
                <h2 style={{ marginBottom: '1.5rem', textAlign: 'center' }}>
                  AI Prediction
                </h2>
                <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                  <div style={{ fontSize: '2.5rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>
                    {comparison.prediction.predicted_winner === 'Red'
                      ? comparison.prediction.red_fighter_name
                      : comparison.prediction.blue_fighter_name}
                  </div>
                  <div style={{ color: '#888' }}>
                    Predicted Winner • {comparison.prediction.confidence_score.toFixed(1)}% Confidence
                  </div>
                </div>

                {/* Probability Bars */}
                <div style={{ marginBottom: '2rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                    <span>{comparison.prediction.red_fighter_name}</span>
                    <span>{(comparison.prediction.red_win_probability * 100).toFixed(1)}%</span>
                  </div>
                  <div className="probability-bar">
                    <div
                      className="probability-fill"
                      style={{ width: `${comparison.prediction.red_win_probability * 100}%` }}
                    ></div>
                  </div>

                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem', marginTop: '1rem' }}>
                    <span>{comparison.prediction.blue_fighter_name}</span>
                    <span>{(comparison.prediction.blue_win_probability * 100).toFixed(1)}%</span>
                  </div>
                  <div className="probability-bar">
                    <div
                      className="probability-fill"
                      style={{ width: `${comparison.prediction.blue_win_probability * 100}%` }}
                    ></div>
                  </div>
                </div>

                {/* Key Factors */}
                {comparison.prediction.key_factors.length > 0 && (
                  <div>
                    <h3 style={{ marginBottom: '1rem' }}>Key Factors</h3>
                    <ul style={{ listStyle: 'none', padding: 0 }}>
                      {comparison.prediction.key_factors.map((factor, idx) => (
                        <li key={idx} style={{ marginBottom: '0.5rem', paddingLeft: '1.5rem', position: 'relative' }}>
                          <span style={{ position: 'absolute', left: 0 }}>•</span>
                          {factor}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Betting Recommendation */}
                {comparison.prediction.betting_recommendation && (
                  <div style={{ marginTop: '2rem', padding: '1rem', background: 'rgba(211, 47, 47, 0.1)', borderRadius: '8px' }}>
                    <strong>Betting Recommendation:</strong> {comparison.prediction.betting_recommendation}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default HeadToHead;
