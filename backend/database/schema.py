from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Fighter(Base):
    """Fighter profile and career statistics"""
    __tablename__ = "fighters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)

    # Career statistics (aggregated from fights)
    total_fights = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    draws = Column(Integer, default=0)
    win_percentage = Column(Float, default=0.0)

    # Win methods
    ko_tko_wins = Column(Integer, default=0)
    submission_wins = Column(Integer, default=0)
    decision_wins = Column(Integer, default=0)

    # Average stats
    avg_fight_duration_secs = Column(Float, default=0.0)
    avg_significant_strikes = Column(Float, default=0.0)
    avg_takedowns = Column(Float, default=0.0)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    red_corner_fights = relationship("Fight", back_populates="red_fighter", foreign_keys="Fight.red_fighter_id")
    blue_corner_fights = relationship("Fight", back_populates="blue_fighter", foreign_keys="Fight.blue_fighter_id")


class Fight(Base):
    """Individual fight records with all statistics"""
    __tablename__ = "fights"

    id = Column(Integer, primary_key=True, index=True)

    # Fighter references
    red_fighter_id = Column(Integer, ForeignKey("fighters.id"), nullable=False)
    blue_fighter_id = Column(Integer, ForeignKey("fighters.id"), nullable=False)

    # Fight details
    date = Column(DateTime, index=True, nullable=False)
    location = Column(String(255))
    country = Column(String(100))
    event_name = Column(String(255))

    # Betting odds
    red_odds = Column(Float)
    blue_odds = Column(Float)
    red_expected_value = Column(Float)
    blue_expected_value = Column(Float)

    # Method odds
    red_ko_odds = Column(Float)
    blue_ko_odds = Column(Float)
    red_sub_odds = Column(Float)
    blue_sub_odds = Column(Float)
    red_dec_odds = Column(Float)
    blue_dec_odds = Column(Float)

    # Fight outcome
    winner = Column(String(10))  # 'Red', 'Blue', 'Draw'
    finish_method = Column(String(100))
    finish_details = Column(Text)
    finish_round = Column(Integer)
    finish_round_time = Column(String(10))
    total_fight_duration_secs = Column(Float)

    # Red fighter stats
    red_sig_strikes = Column(Integer)
    red_sig_strikes_attempted = Column(Integer)
    red_sig_strike_accuracy = Column(Float)
    red_total_strikes = Column(Integer)
    red_takedowns = Column(Integer)
    red_takedown_attempts = Column(Integer)
    red_takedown_accuracy = Column(Float)
    red_submission_attempts = Column(Integer)
    red_knockdowns = Column(Integer)
    red_control_time_secs = Column(Float)

    # Blue fighter stats
    blue_sig_strikes = Column(Integer)
    blue_sig_strikes_attempted = Column(Integer)
    blue_sig_strike_accuracy = Column(Float)
    blue_total_strikes = Column(Integer)
    blue_takedowns = Column(Integer)
    blue_takedown_attempts = Column(Integer)
    blue_takedown_accuracy = Column(Float)
    blue_submission_attempts = Column(Integer)
    blue_knockdowns = Column(Integer)
    blue_control_time_secs = Column(Float)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    red_fighter = relationship("Fighter", back_populates="red_corner_fights", foreign_keys=[red_fighter_id])
    blue_fighter = relationship("Fighter", back_populates="blue_corner_fights", foreign_keys=[blue_fighter_id])

    # Indexes for common queries
    __table_args__ = (
        Index('idx_fight_date', 'date'),
        Index('idx_fight_fighters', 'red_fighter_id', 'blue_fighter_id'),
    )


class Prediction(Base):
    """ML predictions for fights"""
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    fight_id = Column(Integer, ForeignKey("fights.id"), nullable=False)

    # Prediction results
    predicted_winner = Column(String(10))  # 'Red', 'Blue'
    red_win_probability = Column(Float)
    blue_win_probability = Column(Float)
    confidence_score = Column(Float)

    # Betting value
    predicted_method = Column(String(50))  # 'KO/TKO', 'Submission', 'Decision'
    betting_value_detected = Column(Boolean, default=False)
    recommended_bet = Column(String(50))

    # Model info
    model_version = Column(String(50))
    features_used = Column(Text)  # JSON string

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    fight = relationship("Fight")


class User(Base):
    """User accounts for premium features"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # Subscription
    is_premium = Column(Boolean, default=False)
    stripe_customer_id = Column(String(255))
    stripe_subscription_id = Column(String(255))
    subscription_start_date = Column(DateTime)
    subscription_end_date = Column(DateTime)

    # Usage tracking (for free tier limits)
    daily_searches = Column(Integer, default=0)
    last_search_reset = Column(DateTime, default=datetime.utcnow)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
