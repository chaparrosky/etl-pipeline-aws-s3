"""
API endpoints for fight predictions and head-to-head analysis
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from database.config import get_db
from database.schema import Fighter, Fight
from models.schemas import (
    HeadToHeadRequest,
    HeadToHeadResponse,
    FighterStats,
    FightSummary,
    PredictionRequest,
    PredictionResponse,
    BettingValueResponse,
    BettingValue
)
from services.ml_predictor import MLPredictor

router = APIRouter(prefix="/predictions", tags=["predictions"])

# Initialize ML predictor (will be loaded once)
predictor = MLPredictor()


@router.post("/head-to-head", response_model=HeadToHeadResponse)
def compare_fighters(
    request: HeadToHeadRequest,
    db: Session = Depends(get_db)
):
    """
    Head-to-head comparison of two fighters
    Free tier: Basic comparison
    Premium tier: Includes prediction
    """
    # Get both fighters
    fighter1 = db.query(Fighter).filter(
        func.lower(Fighter.name) == func.lower(request.fighter1_name)
    ).first()

    fighter2 = db.query(Fighter).filter(
        func.lower(Fighter.name) == func.lower(request.fighter2_name)
    ).first()

    if not fighter1:
        raise HTTPException(status_code=404, detail=f"Fighter '{request.fighter1_name}' not found")
    if not fighter2:
        raise HTTPException(status_code=404, detail=f"Fighter '{request.fighter2_name}' not found")

    # Check if they've fought before
    previous_matchups = db.query(Fight).filter(
        ((Fight.red_fighter_id == fighter1.id) & (Fight.blue_fighter_id == fighter2.id)) |
        ((Fight.red_fighter_id == fighter2.id) & (Fight.blue_fighter_id == fighter1.id))
    ).order_by(Fight.date.desc()).all()

    # Convert to FightSummary
    matchup_summaries = []
    for fight in previous_matchups:
        matchup_summaries.append(FightSummary(
            id=fight.id,
            date=fight.date,
            red_fighter_name=fight.red_fighter.name,
            blue_fighter_name=fight.blue_fighter.name,
            winner=fight.winner,
            finish_method=fight.finish_method,
            finish_round=fight.finish_round,
            location=fight.location
        ))

    # Analyze advantages
    fighter1_advantages = []
    fighter2_advantages = []

    if fighter1.win_percentage > fighter2.win_percentage:
        diff = fighter1.win_percentage - fighter2.win_percentage
        fighter1_advantages.append(f"Higher win percentage (+{diff:.1f}%)")
    else:
        diff = fighter2.win_percentage - fighter1.win_percentage
        fighter2_advantages.append(f"Higher win percentage (+{diff:.1f}%)")

    if fighter1.ko_tko_wins > fighter2.ko_tko_wins:
        fighter1_advantages.append(f"More knockout power ({fighter1.ko_tko_wins} KO/TKO wins)")
    elif fighter2.ko_tko_wins > fighter1.ko_tko_wins:
        fighter2_advantages.append(f"More knockout power ({fighter2.ko_tko_wins} KO/TKO wins)")

    if fighter1.submission_wins > fighter2.submission_wins:
        fighter1_advantages.append(f"Superior grappling ({fighter1.submission_wins} submission wins)")
    elif fighter2.submission_wins > fighter1.submission_wins:
        fighter2_advantages.append(f"Superior grappling ({fighter2.submission_wins} submission wins)")

    if fighter1.total_fights > fighter2.total_fights:
        fighter1_advantages.append(f"More experience ({fighter1.total_fights} fights)")
    elif fighter2.total_fights > fighter1.total_fights:
        fighter2_advantages.append(f"More experience ({fighter2.total_fights} fights)")

    # Generate prediction (Premium feature - simplified here)
    prediction = predictor.predict_fight(fighter1, fighter2, db)

    return HeadToHeadResponse(
        fighter1=FighterStats.from_orm(fighter1),
        fighter2=FighterStats.from_orm(fighter2),
        previous_matchups=matchup_summaries,
        fighter1_advantages=fighter1_advantages,
        fighter2_advantages=fighter2_advantages,
        prediction=prediction
    )


@router.post("/predict", response_model=PredictionResponse)
def predict_fight(
    request: PredictionRequest,
    db: Session = Depends(get_db)
):
    """
    Predict fight outcome using ML model
    Premium feature
    """
    # Get both fighters
    red_fighter = db.query(Fighter).filter(
        func.lower(Fighter.name) == func.lower(request.red_fighter_name)
    ).first()

    blue_fighter = db.query(Fighter).filter(
        func.lower(Fighter.name) == func.lower(request.blue_fighter_name)
    ).first()

    if not red_fighter:
        raise HTTPException(status_code=404, detail=f"Fighter '{request.red_fighter_name}' not found")
    if not blue_fighter:
        raise HTTPException(status_code=404, detail=f"Fighter '{request.blue_fighter_name}' not found")

    # Generate prediction using ML model
    prediction = predictor.predict_fight(red_fighter, blue_fighter, db)

    return prediction


@router.get("/betting-value", response_model=BettingValueResponse)
def find_betting_value(
    min_value_percentage: float = 5.0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Find upcoming fights with betting value
    Premium feature - shows where ML predictions differ from betting odds
    """
    # Get upcoming fights (fights without winner yet, or recent fights)
    # For demo, we'll analyze recent fights where we have odds
    fights = db.query(Fight).filter(
        Fight.red_odds.isnot(None),
        Fight.blue_odds.isnot(None)
    ).order_by(Fight.date.desc()).limit(50).all()

    opportunities = []

    for fight in fights:
        # Get fighters
        red_fighter = db.query(Fighter).filter(Fighter.id == fight.red_fighter_id).first()
        blue_fighter = db.query(Fighter).filter(Fighter.blue_fighter_id == fight.blue_fighter_id).first()

        if not red_fighter or not blue_fighter:
            continue

        # Get prediction
        prediction = predictor.predict_fight(red_fighter, blue_fighter, db)

        # Calculate implied probability from odds
        red_implied_prob = predictor.odds_to_probability(fight.red_odds)
        blue_implied_prob = predictor.odds_to_probability(fight.blue_odds)

        # Find value bets
        red_value = prediction.red_win_probability - red_implied_prob
        blue_value = prediction.blue_win_probability - blue_implied_prob

        # If our model predicts higher probability than odds suggest, it's value
        if red_value * 100 >= min_value_percentage:
            opportunities.append(BettingValue(
                fight_id=fight.id,
                red_fighter_name=red_fighter.name,
                blue_fighter_name=blue_fighter.name,
                date=fight.date,
                recommended_bet='Red',
                expected_value=red_value * 100,
                current_odds=fight.red_odds,
                predicted_probability=prediction.red_win_probability,
                value_percentage=red_value * 100
            ))
        elif blue_value * 100 >= min_value_percentage:
            opportunities.append(BettingValue(
                fight_id=fight.id,
                red_fighter_name=red_fighter.name,
                blue_fighter_name=blue_fighter.name,
                date=fight.date,
                recommended_bet='Blue',
                expected_value=blue_value * 100,
                current_odds=fight.blue_odds,
                predicted_probability=prediction.blue_win_probability,
                value_percentage=blue_value * 100
            ))

    # Sort by value percentage
    opportunities.sort(key=lambda x: x.value_percentage, reverse=True)
    opportunities = opportunities[:limit]

    return BettingValueResponse(
        opportunities=opportunities,
        total_found=len(opportunities)
    )


@router.get("/fight-card/{event_name}")
def analyze_fight_card(
    event_name: str,
    db: Session = Depends(get_db)
):
    """
    Analyze all fights on a UFC event card
    Premium feature
    """
    # Search for fights matching the event name
    fights = db.query(Fight).filter(
        Fight.event_name.ilike(f"%{event_name}%")
    ).order_by(Fight.date.desc()).all()

    if not fights:
        raise HTTPException(status_code=404, detail=f"No fights found for event '{event_name}'")

    card_analysis = []

    for fight in fights:
        red_fighter = fight.red_fighter
        blue_fighter = fight.blue_fighter

        # Get prediction
        prediction = predictor.predict_fight(red_fighter, blue_fighter, db)

        card_analysis.append({
            'fight_id': fight.id,
            'red_fighter': red_fighter.name,
            'blue_fighter': blue_fighter.name,
            'red_record': f"{red_fighter.wins}-{red_fighter.losses}-{red_fighter.draws}",
            'blue_record': f"{blue_fighter.wins}-{blue_fighter.losses}-{blue_fighter.draws}",
            'prediction': {
                'winner': prediction.predicted_winner,
                'confidence': prediction.confidence_score,
                'method': prediction.predicted_method,
                'red_probability': prediction.red_win_probability,
                'blue_probability': prediction.blue_win_probability
            },
            'odds': {
                'red_odds': fight.red_odds,
                'blue_odds': fight.blue_odds
            }
        })

    return {
        'event_name': event_name,
        'total_fights': len(card_analysis),
        'fights': card_analysis
    }
