"""
Pydantic models for API request/response validation
"""
from __future__ import annotations

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class FighterBase(BaseModel):
    name: str


class FighterStats(BaseModel):
    """Fighter statistics response"""
    id: int
    name: str
    total_fights: int
    wins: int
    losses: int
    draws: int
    win_percentage: float
    ko_tko_wins: int
    submission_wins: int
    decision_wins: int
    avg_fight_duration_secs: float

    class Config:
        from_attributes = True


class FightSummary(BaseModel):
    """Summary of a fight"""
    id: int
    date: datetime
    red_fighter_name: str
    blue_fighter_name: str
    winner: Optional[str]
    finish_method: Optional[str]
    finish_round: Optional[int]
    location: Optional[str]

    class Config:
        from_attributes = True


class FighterProfile(FighterStats):
    """Extended fighter profile with recent fights"""
    recent_fights: List[FightSummary] = []


class FightDetail(BaseModel):
    """Detailed fight information"""
    id: int
    date: datetime
    location: Optional[str]
    country: Optional[str]

    # Fighters
    red_fighter_id: int
    blue_fighter_id: int
    red_fighter_name: str
    blue_fighter_name: str

    # Odds
    red_odds: Optional[float]
    blue_odds: Optional[float]
    red_expected_value: Optional[float]
    blue_expected_value: Optional[float]

    # Outcome
    winner: Optional[str]
    finish_method: Optional[str]
    finish_details: Optional[str]
    finish_round: Optional[int]
    finish_round_time: Optional[str]
    total_fight_duration_secs: Optional[float]

    # Stats
    red_sig_strikes: Optional[int]
    blue_sig_strikes: Optional[int]
    red_takedowns: Optional[int]
    blue_takedowns: Optional[int]

    class Config:
        from_attributes = True


class HeadToHeadRequest(BaseModel):
    """Request for head-to-head comparison"""
    fighter1_name: str
    fighter2_name: str


class HeadToHeadResponse(BaseModel):
    """Head-to-head comparison response"""
    fighter1: FighterStats
    fighter2: FighterStats
    previous_matchups: List[FightSummary] = []
    fighter1_advantages: List[str] = []
    fighter2_advantages: List[str] = []
    prediction: Optional['PredictionResponse'] = None


class PredictionRequest(BaseModel):
    """Request for fight prediction"""
    red_fighter_name: str
    blue_fighter_name: str


class PredictionResponse(BaseModel):
    """Fight prediction response"""
    red_fighter_name: str
    blue_fighter_name: str
    predicted_winner: str
    red_win_probability: float
    blue_win_probability: float
    confidence_score: float
    predicted_method: str
    key_factors: List[str] = []
    betting_recommendation: Optional[str] = None

    class Config:
        from_attributes = True


class BettingValue(BaseModel):
    """Betting value opportunity"""
    fight_id: int
    red_fighter_name: str
    blue_fighter_name: str
    date: datetime
    recommended_bet: str  # 'Red', 'Blue', or 'Pass'
    expected_value: float
    current_odds: float
    predicted_probability: float
    value_percentage: float  # How much value in the bet


class BettingValueResponse(BaseModel):
    """Response with betting opportunities"""
    opportunities: List[BettingValue]
    total_found: int


class FighterSearchRequest(BaseModel):
    """Search fighters by name"""
    query: str
    limit: int = 10


class FighterSearchResponse(BaseModel):
    """Search results"""
    fighters: List[FighterStats]
    total: int


class UserCreate(BaseModel):
    """User registration"""
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """User login"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str


class UserProfile(BaseModel):
    """User profile information"""
    id: int
    email: str
    is_premium: bool
    subscription_end_date: Optional[datetime]
    daily_searches: int

    class Config:
        from_attributes = True
