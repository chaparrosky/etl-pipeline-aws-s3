import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Fighter {
  id: number;
  name: string;
  total_fights: number;
  wins: number;
  losses: number;
  draws: number;
  win_percentage: number;
  ko_tko_wins: number;
  submission_wins: number;
  decision_wins: number;
  avg_fight_duration_secs: number;
}

export interface FightSummary {
  id: number;
  date: string;
  red_fighter_name: string;
  blue_fighter_name: string;
  winner: string | null;
  finish_method: string | null;
  finish_round: number | null;
  location: string | null;
}

export interface FighterProfile extends Fighter {
  recent_fights: FightSummary[];
}

export interface Prediction {
  red_fighter_name: string;
  blue_fighter_name: string;
  predicted_winner: string;
  red_win_probability: number;
  blue_win_probability: number;
  confidence_score: number;
  predicted_method: string;
  key_factors: string[];
  betting_recommendation: string | null;
}

export interface HeadToHeadResponse {
  fighter1: Fighter;
  fighter2: Fighter;
  previous_matchups: FightSummary[];
  fighter1_advantages: string[];
  fighter2_advantages: string[];
  prediction: Prediction | null;
}

// Fighter API calls
export const searchFighters = async (query: string): Promise<{ fighters: Fighter[]; total: number }> => {
  const response = await api.get('/fighters/search', {
    params: { query, limit: 10 }
  });
  return response.data;
};

export const getFighterById = async (id: number): Promise<FighterProfile> => {
  const response = await api.get(`/fighters/${id}`);
  return response.data;
};

export const getFighterByName = async (name: string): Promise<FighterProfile> => {
  const response = await api.get(`/fighters/name/${encodeURIComponent(name)}`);
  return response.data;
};

export const listTopFighters = async (limit: number = 20): Promise<Fighter[]> => {
  const response = await api.get('/fighters/', {
    params: { limit, sort_by: 'wins' }
  });
  return response.data;
};

// Prediction API calls
export const compareFighters = async (fighter1_name: string, fighter2_name: string): Promise<HeadToHeadResponse> => {
  const response = await api.post('/predictions/head-to-head', {
    fighter1_name,
    fighter2_name
  });
  return response.data;
};

export const predictFight = async (red_fighter_name: string, blue_fighter_name: string): Promise<Prediction> => {
  const response = await api.post('/predictions/predict', {
    red_fighter_name,
    blue_fighter_name
  });
  return response.data;
};

// Stats
export const getApiStats = async () => {
  const response = await api.get('/stats');
  return response.data;
};

export default api;
