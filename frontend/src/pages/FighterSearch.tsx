import { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { searchFighters, Fighter } from '../services/api';

const FighterSearch = () => {
  const [query, setQuery] = useState('');
  const [fighters, setFighters] = useState<Fighter[]>([]);
  const [suggestions, setSuggestions] = useState<Fighter[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [popularSearches] = useState([
    'Conor McGregor',
    'Jon Jones',
    'Israel Adesanya',
    'Khabib Nurmagomedov',
    'Anderson Silva',
    'Georges St-Pierre'
  ]);

  const debounceTimer = useRef<NodeJS.Timeout | null>(null);
  const searchRef = useRef<HTMLDivElement>(null);

  // Close suggestions when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Live search with debouncing
  useEffect(() => {
    if (debounceTimer.current) {
      clearTimeout(debounceTimer.current);
    }

    if (query.trim().length >= 2) {
      debounceTimer.current = setTimeout(async () => {
        try {
          setLoading(true);
          const result = await searchFighters(query);
          setSuggestions(result.fighters.slice(0, 5));
          setShowSuggestions(true);
        } catch (error) {
          console.error('Search error:', error);
        } finally {
          setLoading(false);
        }
      }, 300); // 300ms debounce
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
    }

    return () => {
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current);
      }
    };
  }, [query]);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim().length < 2) return;

    setLoading(true);
    setSearched(true);
    setShowSuggestions(false);

    try {
      const result = await searchFighters(query);
      setFighters(result.fighters);
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePopularSearch = (fighterName: string) => {
    setQuery(fighterName);
    setShowSuggestions(false);
    // Trigger search
    setTimeout(() => {
      const form = document.querySelector('form');
      if (form) {
        form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
      }
    }, 100);
  };

  const handleSuggestionClick = (fighter: Fighter) => {
    setQuery(fighter.name);
    setShowSuggestions(false);
    setFighters([fighter]);
    setSearched(true);
  };

  return (
    <div style={{ padding: '3rem 0', minHeight: 'calc(100vh - 200px)' }}>
      <div className="container">
        <h1 style={{ textAlign: 'center', marginBottom: '1rem', fontSize: '2.5rem' }}>
          Search UFC Fighters
        </h1>
        <p style={{ textAlign: 'center', color: '#888', marginBottom: '3rem' }}>
          Search from thousands of fighters to view detailed stats and analysis
        </p>

        {/* Search Form */}
        <form onSubmit={handleSearch} className="search-container" ref={searchRef}>
          <div style={{ position: 'relative' }}>
            <input
              type="text"
              className="search-input"
              placeholder="Search for a fighter (e.g., Conor McGregor, Jon Jones)..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onFocus={() => {
                if (suggestions.length > 0) {
                  setShowSuggestions(true);
                }
              }}
              autoComplete="off"
            />

            {/* Live search indicator */}
            {loading && query.length >= 2 && (
              <div style={{
                position: 'absolute',
                right: '1rem',
                top: '50%',
                transform: 'translateY(-50%)',
                fontSize: '0.875rem',
                color: '#888'
              }}>
                Searching...
              </div>
            )}

            {/* Auto-suggestions dropdown */}
            {showSuggestions && suggestions.length > 0 && (
              <div style={{
                position: 'absolute',
                top: '100%',
                left: 0,
                right: 0,
                background: '#1a1a1a',
                border: '2px solid #d32f2f',
                borderTop: 'none',
                borderRadius: '0 0 10px 10px',
                marginTop: '-10px',
                paddingTop: '10px',
                zIndex: 1000,
                maxHeight: '300px',
                overflowY: 'auto'
              }}>
                {suggestions.map((fighter) => (
                  <div
                    key={fighter.id}
                    onClick={() => handleSuggestionClick(fighter)}
                    style={{
                      padding: '1rem',
                      cursor: 'pointer',
                      borderBottom: '1px solid #333',
                      transition: 'background 0.2s'
                    }}
                    onMouseEnter={(e) => e.currentTarget.style.background = '#252525'}
                    onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
                  >
                    <div style={{ fontWeight: 'bold', marginBottom: '0.25rem' }}>
                      {fighter.name}
                    </div>
                    <div style={{ fontSize: '0.875rem', color: '#888' }}>
                      {fighter.wins}-{fighter.losses}-{fighter.draws} • {fighter.win_percentage.toFixed(1)}% Win Rate
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </form>

        {/* Popular Searches */}
        {!searched && (
          <div style={{ marginTop: '3rem' }}>
            <h3 style={{ marginBottom: '1rem', color: '#888', textAlign: 'center' }}>
              Popular Searches
            </h3>
            <div style={{
              display: 'flex',
              flexWrap: 'wrap',
              gap: '0.75rem',
              justifyContent: 'center',
              maxWidth: '600px',
              margin: '0 auto'
            }}>
              {popularSearches.map((name) => (
                <button
                  key={name}
                  onClick={() => handlePopularSearch(name)}
                  style={{
                    padding: '0.5rem 1rem',
                    background: '#1a1a1a',
                    border: '1px solid #333',
                    borderRadius: '20px',
                    color: 'white',
                    cursor: 'pointer',
                    transition: 'all 0.3s',
                    fontSize: '0.875rem'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.borderColor = '#d32f2f';
                    e.currentTarget.style.background = '#252525';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.borderColor = '#333';
                    e.currentTarget.style.background = '#1a1a1a';
                  }}
                >
                  {name}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Loading State */}
        {loading && searched && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Searching fighters...</p>
          </div>
        )}

        {/* No Results */}
        {!loading && searched && fighters.length === 0 && (
          <div style={{
            textAlign: 'center',
            padding: '4rem 2rem',
            background: '#1a1a1a',
            borderRadius: '12px',
            marginTop: '2rem'
          }}>
            <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>🔍</div>
            <h2 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>
              No fighters found
            </h2>
            <p style={{ color: '#888', marginBottom: '1.5rem' }}>
              No fighters match "{query}"
            </p>
            <p style={{ color: '#666', fontSize: '0.875rem' }}>
              Try searching with a different name or check the spelling
            </p>
          </div>
        )}

        {/* Search Results */}
        {!loading && fighters.length > 0 && (
          <div style={{ marginTop: '2rem' }}>
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: '1.5rem'
            }}>
              <p style={{ color: '#888' }}>
                Found <span style={{ color: '#d32f2f', fontWeight: 'bold' }}>{fighters.length}</span> fighter{fighters.length !== 1 ? 's' : ''}
              </p>
              <button
                onClick={() => {
                  setQuery('');
                  setFighters([]);
                  setSearched(false);
                }}
                style={{
                  padding: '0.5rem 1rem',
                  background: 'transparent',
                  border: '1px solid #333',
                  borderRadius: '8px',
                  color: '#888',
                  cursor: 'pointer',
                  fontSize: '0.875rem',
                  transition: 'all 0.3s'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.borderColor = '#d32f2f';
                  e.currentTarget.style.color = '#d32f2f';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = '#333';
                  e.currentTarget.style.color = '#888';
                }}
              >
                Clear Search
              </button>
            </div>

            <div className="grid grid-2">
              {fighters.map((fighter, index) => (
                <Link
                  to={`/fighter/${fighter.id}`}
                  key={fighter.id}
                  style={{
                    textDecoration: 'none',
                    animation: `fadeInUp 0.5s ease ${index * 0.1}s both`
                  }}
                >
                  <div className="card fighter-card">
                    <div className="fighter-name">{fighter.name}</div>
                    <div className="record" style={{ marginBottom: '1rem' }}>
                      <span style={{ color: '#4caf50' }}>{fighter.wins}W</span>
                      {' - '}
                      <span style={{ color: '#f44336' }}>{fighter.losses}L</span>
                      {fighter.draws > 0 && <> - <span>{fighter.draws}D</span></>}
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
                      <div className="stat">
                        <div className="stat-value">{fighter.submission_wins}</div>
                        <div className="stat-label">Subs</div>
                      </div>
                    </div>

                    {/* View Profile Button */}
                    <div style={{
                      marginTop: '1rem',
                      padding: '0.75rem',
                      background: 'linear-gradient(135deg, #d32f2f 0%, #8b0000 100%)',
                      borderRadius: '8px',
                      textAlign: 'center',
                      fontWeight: 'bold',
                      opacity: 0,
                      transition: 'opacity 0.3s'
                    }}
                    className="view-profile-btn">
                      View Full Profile →
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}

        {/* Helpful Tips */}
        {!searched && (
          <div style={{
            marginTop: '4rem',
            padding: '2rem',
            background: 'linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%)',
            borderRadius: '12px',
            border: '1px solid #333'
          }}>
            <h3 style={{ marginBottom: '1rem', color: '#d32f2f' }}>
              Search Tips
            </h3>
            <ul style={{ color: '#888', lineHeight: 1.8, paddingLeft: '1.5rem' }}>
              <li>Search by first name, last name, or full name</li>
              <li>Live results appear as you type</li>
              <li>Click on suggestions for instant results</li>
              <li>Try popular fighters like "Silva", "Jones", or "McGregor"</li>
            </ul>
          </div>
        )}
      </div>

      {/* Add fade-in animation */}
      <style>{`
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .fighter-card:hover .view-profile-btn {
          opacity: 1 !important;
        }
      `}</style>
    </div>
  );
};

export default FighterSearch;
