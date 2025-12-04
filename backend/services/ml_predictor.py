"""
Machine Learning predictor for UFC fight outcomes
"""
import numpy as np
from sqlalchemy.orm import Session
from typing import Tuple
import pickle
from pathlib import Path

from database.schema import Fighter, Fight
from models.schemas import PredictionResponse


class MLPredictor:
    """
    ML model for predicting UFC fight outcomes
    Start with a rule-based system, then enhance with trained ML model
    """

    def __init__(self):
        self.model = None
        self.model_path = Path(__file__).parent.parent / "ml" / "model.pkl"

        # Try to load pre-trained model
        if self.model_path.exists():
            try:
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
            except Exception as e:
                print(f"Could not load model: {e}")
                self.model = None

    def predict_fight(self, red_fighter: Fighter, blue_fighter: Fighter, db: Session) -> PredictionResponse:
        """
        Predict fight outcome between two fighters
        Uses rule-based system for now, can be replaced with trained ML model
        """

        # Feature extraction
        features = self._extract_features(red_fighter, blue_fighter, db)

        if self.model:
            # Use trained ML model
            prediction = self._predict_with_model(features)
        else:
            # Use rule-based prediction
            prediction = self._predict_rule_based(features, red_fighter, blue_fighter)

        return prediction

    def _extract_features(self, red_fighter: Fighter, blue_fighter: Fighter, db: Session) -> dict:
        """Extract features for prediction"""

        # Get recent fight statistics
        red_recent_fights = db.query(Fight).filter(
            (Fight.red_fighter_id == red_fighter.id) | (Fight.blue_fighter_id == red_fighter.id)
        ).order_by(Fight.date.desc()).limit(5).all()

        blue_recent_fights = db.query(Fight).filter(
            (Fight.red_fighter_id == blue_fighter.id) | (Fight.blue_fighter_id == blue_fighter.id)
        ).order_by(Fight.date.desc()).limit(5).all()

        # Calculate recent form (last 5 fights)
        red_recent_wins = sum(1 for f in red_recent_fights
                              if (f.red_fighter_id == red_fighter.id and f.winner == 'Red') or
                              (f.blue_fighter_id == red_fighter.id and f.winner == 'Blue'))

        blue_recent_wins = sum(1 for f in blue_recent_fights
                               if (f.red_fighter_id == blue_fighter.id and f.winner == 'Red') or
                               (f.blue_fighter_id == blue_fighter.id and f.winner == 'Blue'))

        features = {
            # Red fighter features
            'red_win_percentage': red_fighter.win_percentage,
            'red_total_fights': red_fighter.total_fights,
            'red_ko_rate': (red_fighter.ko_tko_wins / red_fighter.total_fights * 100) if red_fighter.total_fights > 0 else 0,
            'red_sub_rate': (red_fighter.submission_wins / red_fighter.total_fights * 100) if red_fighter.total_fights > 0 else 0,
            'red_recent_form': red_recent_wins / min(5, len(red_recent_fights)) if red_recent_fights else 0,

            # Blue fighter features
            'blue_win_percentage': blue_fighter.win_percentage,
            'blue_total_fights': blue_fighter.total_fights,
            'blue_ko_rate': (blue_fighter.ko_tko_wins / blue_fighter.total_fights * 100) if blue_fighter.total_fights > 0 else 0,
            'blue_sub_rate': (blue_fighter.submission_wins / blue_fighter.total_fights * 100) if blue_fighter.total_fights > 0 else 0,
            'blue_recent_form': blue_recent_wins / min(5, len(blue_recent_fights)) if blue_recent_fights else 0,

            # Differential features
            'win_percentage_diff': red_fighter.win_percentage - blue_fighter.win_percentage,
            'experience_diff': red_fighter.total_fights - blue_fighter.total_fights,
            'ko_rate_diff': features['red_ko_rate'] - features['blue_ko_rate'] if 'red_ko_rate' in features else 0,
        }

        return features

    def _predict_rule_based(self, features: dict, red_fighter: Fighter, blue_fighter: Fighter) -> PredictionResponse:
        """
        Rule-based prediction system
        This is a simple heuristic approach that can be replaced with ML
        """

        # Score system
        red_score = 50.0  # Start neutral
        blue_score = 50.0

        # Win percentage impact (±15 points max)
        win_perc_impact = (features['win_percentage_diff'] / 100) * 15
        red_score += win_perc_impact
        blue_score -= win_perc_impact

        # Recent form impact (±10 points max)
        form_diff = features['red_recent_form'] - features['blue_recent_form']
        form_impact = form_diff * 10
        red_score += form_impact
        blue_score -= form_impact

        # Experience impact (±5 points max)
        exp_diff = min(max(features['experience_diff'], -10), 10)
        exp_impact = (exp_diff / 10) * 5
        red_score += exp_impact
        blue_score -= exp_impact

        # Finishing ability (±8 points max)
        red_finish_rate = features['red_ko_rate'] + features['red_sub_rate']
        blue_finish_rate = features['blue_ko_rate'] + features['blue_sub_rate']
        finish_impact = ((red_finish_rate - blue_finish_rate) / 100) * 8
        red_score += finish_impact
        blue_score -= finish_impact

        # Normalize to probabilities
        total = red_score + blue_score
        red_prob = red_score / total
        blue_prob = blue_score / total

        # Determine predicted method based on fighter styles
        if red_fighter.ko_tko_wins > red_fighter.submission_wins and red_fighter.ko_tko_wins > red_fighter.decision_wins:
            predicted_method = "KO/TKO"
        elif red_fighter.submission_wins > red_fighter.decision_wins:
            predicted_method = "Submission"
        else:
            predicted_method = "Decision"

        # Calculate confidence (0-100)
        confidence = abs(red_prob - blue_prob) * 100

        # Key factors
        key_factors = []
        if abs(features['win_percentage_diff']) > 10:
            if features['win_percentage_diff'] > 0:
                key_factors.append(f"{red_fighter.name} has superior win rate (+{features['win_percentage_diff']:.1f}%)")
            else:
                key_factors.append(f"{blue_fighter.name} has superior win rate (+{abs(features['win_percentage_diff']):.1f}%)")

        if abs(form_diff) > 0.2:
            if form_diff > 0:
                key_factors.append(f"{red_fighter.name} in better recent form")
            else:
                key_factors.append(f"{blue_fighter.name} in better recent form")

        if abs(features['experience_diff']) > 5:
            if features['experience_diff'] > 0:
                key_factors.append(f"{red_fighter.name} has more experience")
            else:
                key_factors.append(f"{blue_fighter.name} has more experience")

        if red_finish_rate > 50 or blue_finish_rate > 50:
            if red_finish_rate > blue_finish_rate:
                key_factors.append(f"{red_fighter.name} has higher finish rate ({red_finish_rate:.1f}%)")
            else:
                key_factors.append(f"{blue_fighter.name} has higher finish rate ({blue_finish_rate:.1f}%)")

        return PredictionResponse(
            red_fighter_name=red_fighter.name,
            blue_fighter_name=blue_fighter.name,
            predicted_winner='Red' if red_prob > blue_prob else 'Blue',
            red_win_probability=round(red_prob, 3),
            blue_win_probability=round(blue_prob, 3),
            confidence_score=round(confidence, 2),
            predicted_method=predicted_method,
            key_factors=key_factors,
            betting_recommendation=self._get_betting_recommendation(red_prob, blue_prob, confidence)
        )

    def _predict_with_model(self, features: dict) -> dict:
        """Use trained ML model for prediction (placeholder for future implementation)"""
        # TODO: Implement once model is trained
        pass

    def _get_betting_recommendation(self, red_prob: float, blue_prob: float, confidence: float) -> str:
        """Generate betting recommendation based on prediction confidence"""
        if confidence < 10:
            return "Too close to call - avoid betting"
        elif confidence < 20:
            return "Low confidence - small bet only"
        elif confidence < 30:
            return "Moderate confidence - reasonable bet"
        else:
            winner = "Red" if red_prob > blue_prob else "Blue"
            return f"High confidence - strong bet on {winner}"

    @staticmethod
    def odds_to_probability(odds: float) -> float:
        """
        Convert American odds to implied probability
        """
        if odds > 0:
            # Underdog odds
            return 100 / (odds + 100)
        else:
            # Favorite odds
            return abs(odds) / (abs(odds) + 100)

    @staticmethod
    def probability_to_odds(probability: float) -> float:
        """
        Convert probability to American odds
        """
        if probability >= 0.5:
            # Favorite
            return -(probability / (1 - probability)) * 100
        else:
            # Underdog
            return ((1 - probability) / probability) * 100
