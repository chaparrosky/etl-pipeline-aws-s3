"""
API endpoints for fighter operations
"""
from __future__ import annotations

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import List, Optional

from database.config import get_db
from database.schema import Fighter, Fight
from models.schemas import (
    FighterStats,
    FighterProfile,
    FighterSearchRequest,
    FighterSearchResponse,
    FightSummary
)

router = APIRouter(prefix="/fighters", tags=["fighters"])


@router.get("/search", response_model=FighterSearchResponse)
def search_fighters(
    query: str = Query(..., min_length=2),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Search fighters by name (case-insensitive)
    Free tier: Available to all users
    """
    fighters = db.query(Fighter).filter(
        Fighter.name.ilike(f"%{query}%")
    ).order_by(
        Fighter.total_fights.desc()
    ).limit(limit).all()

    return FighterSearchResponse(
        fighters=fighters,
        total=len(fighters)
    )


@router.get("/{fighter_id}", response_model=FighterProfile)
def get_fighter_profile(
    fighter_id: int,
    include_recent_fights: bool = Query(True),
    db: Session = Depends(get_db)
):
    """
    Get detailed fighter profile with statistics
    Free tier: Available to all users
    """
    fighter = db.query(Fighter).filter(Fighter.id == fighter_id).first()

    if not fighter:
        raise HTTPException(status_code=404, detail="Fighter not found")

    profile_data = FighterStats.from_orm(fighter).dict()

    if include_recent_fights:
        # Get all fights for this fighter (both red and blue corner)
        red_fights = db.query(Fight).filter(
            Fight.red_fighter_id == fighter_id
        ).order_by(Fight.date.desc()).all()

        blue_fights = db.query(Fight).filter(
            Fight.blue_fighter_id == fighter_id
        ).order_by(Fight.date.desc()).all()

        # Combine and sort by date
        all_fights = red_fights + blue_fights
        all_fights.sort(key=lambda x: x.date if x.date else datetime.min, reverse=True)

        # Convert to FightSummary and deduplicate by fight key (fighters + date)
        seen_fights = set()
        fight_summaries = []
        for fight in all_fights:
            # Create unique key: sorted fighter names + date
            fighters = tuple(sorted([fight.red_fighter.name, fight.blue_fighter.name]))
            fight_key = (fighters, fight.date)

            if fight_key not in seen_fights:
                seen_fights.add(fight_key)
                fight_summaries.append(FightSummary(
                    id=fight.id,
                    date=fight.date,
                    red_fighter_name=fight.red_fighter.name,
                    blue_fighter_name=fight.blue_fighter.name,
                    winner=fight.winner,
                    finish_method=fight.finish_method,
                    finish_round=fight.finish_round,
                    location=fight.location
                ))

                # Stop after collecting 5 unique fights
                if len(fight_summaries) >= 5:
                    break

        profile_data['recent_fights'] = fight_summaries

    return FighterProfile(**profile_data)


@router.get("/name/{fighter_name}", response_model=FighterProfile)
def get_fighter_by_name(
    fighter_name: str,
    db: Session = Depends(get_db)
):
    """
    Get fighter profile by exact name
    """
    fighter = db.query(Fighter).filter(
        func.lower(Fighter.name) == func.lower(fighter_name)
    ).first()

    if not fighter:
        raise HTTPException(status_code=404, detail=f"Fighter '{fighter_name}' not found")

    return get_fighter_profile(fighter.id, db=db)


@router.get("/", response_model=List[FighterStats])
def list_fighters(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = Query("wins", regex="^(wins|win_percentage|total_fights)$"),
    db: Session = Depends(get_db)
):
    """
    List fighters with pagination and sorting
    Free tier: Available to all users
    """
    # Sort by the specified column
    sort_column = getattr(Fighter, sort_by)

    fighters = db.query(Fighter).filter(
        Fighter.total_fights > 0
    ).order_by(
        sort_column.desc()
    ).offset(skip).limit(limit).all()

    return fighters


@router.get("/{fighter_id}/stats/timeline")
def get_fighter_timeline(
    fighter_id: int,
    db: Session = Depends(get_db)
):
    """
    Get fighter's performance timeline (win/loss record over time)
    Premium feature for visualization
    """
    fighter = db.query(Fighter).filter(Fighter.id == fighter_id).first()

    if not fighter:
        raise HTTPException(status_code=404, detail="Fighter not found")

    # Get all fights chronologically
    red_fights = db.query(Fight).filter(
        Fight.red_fighter_id == fighter_id
    ).order_by(Fight.date.asc()).all()

    blue_fights = db.query(Fight).filter(
        Fight.blue_fighter_id == fighter_id
    ).order_by(Fight.date.asc()).all()

    # Combine and sort
    all_fights = []
    for fight in red_fights:
        all_fights.append({
            'date': fight.date.isoformat(),
            'opponent': fight.blue_fighter.name,
            'won': fight.winner == 'Red',
            'method': fight.finish_method,
            'round': fight.finish_round,
            'location': fight.location
        })

    for fight in blue_fights:
        all_fights.append({
            'date': fight.date.isoformat(),
            'opponent': fight.red_fighter.name,
            'won': fight.winner == 'Blue',
            'method': fight.finish_method,
            'round': fight.finish_round,
            'location': fight.location
        })

    all_fights.sort(key=lambda x: x['date'])

    # Calculate running win percentage
    wins = 0
    total = 0
    timeline = []

    for fight in all_fights:
        total += 1
        if fight['won']:
            wins += 1

        timeline.append({
            **fight,
            'fight_number': total,
            'career_wins': wins,
            'career_losses': total - wins,
            'win_percentage': (wins / total) * 100
        })

    return {
        'fighter_id': fighter_id,
        'fighter_name': fighter.name,
        'timeline': timeline
    }
