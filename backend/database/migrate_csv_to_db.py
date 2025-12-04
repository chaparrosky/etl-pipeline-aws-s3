"""
Script to migrate UFC CSV data to PostgreSQL database
Run this after setting up your database
"""
import pandas as pd
import sys
from pathlib import Path
from sqlalchemy.orm import Session
from datetime import datetime

# Add parent directory to path to import schema
sys.path.append(str(Path(__file__).parent.parent))

from database.schema import Base, Fighter, Fight
from database.config import engine, SessionLocal


def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")


def get_or_create_fighter(db: Session, fighter_name: str) -> Fighter:
    """Get existing fighter or create new one"""
    fighter = db.query(Fighter).filter(Fighter.name == fighter_name).first()
    if not fighter:
        fighter = Fighter(name=fighter_name)
        db.add(fighter)
        db.flush()  # Get the ID without committing
    return fighter


def update_fighter_stats(db: Session):
    """Update aggregated stats for all fighters"""
    print("Updating fighter statistics...")

    fighters = db.query(Fighter).all()

    for fighter in fighters:
        # Get all fights for this fighter
        red_fights = db.query(Fight).filter(Fight.red_fighter_id == fighter.id).all()
        blue_fights = db.query(Fight).filter(Fight.blue_fighter_id == fighter.id).all()

        total_fights = len(red_fights) + len(blue_fights)
        wins = 0
        ko_wins = 0
        sub_wins = 0
        dec_wins = 0
        total_duration = 0

        # Count wins from red corner
        for fight in red_fights:
            if fight.winner == 'Red':
                wins += 1
                if fight.finish_method:
                    method_upper = fight.finish_method.upper()
                    if 'KO' in method_upper or 'TKO' in method_upper:
                        ko_wins += 1
                    elif 'SUB' in method_upper:
                        sub_wins += 1
                    elif 'DEC' in method_upper:
                        dec_wins += 1

            if fight.total_fight_duration_secs:
                total_duration += fight.total_fight_duration_secs

        # Count wins from blue corner
        for fight in blue_fights:
            if fight.winner == 'Blue':
                wins += 1
                if fight.finish_method:
                    method_upper = fight.finish_method.upper()
                    if 'KO' in method_upper or 'TKO' in method_upper:
                        ko_wins += 1
                    elif 'SUB' in method_upper:
                        sub_wins += 1
                    elif 'DEC' in method_upper:
                        dec_wins += 1

            if fight.total_fight_duration_secs:
                total_duration += fight.total_fight_duration_secs

        # Update fighter stats
        fighter.total_fights = total_fights
        fighter.wins = wins
        fighter.losses = total_fights - wins
        fighter.win_percentage = (wins / total_fights * 100) if total_fights > 0 else 0
        fighter.ko_tko_wins = ko_wins
        fighter.submission_wins = sub_wins
        fighter.decision_wins = dec_wins
        fighter.avg_fight_duration_secs = total_duration / total_fights if total_fights > 0 else 0

    db.commit()
    print(f"Updated stats for {len(fighters)} fighters")


def migrate_csv_data(csv_path: str):
    """Migrate data from transformed CSV to database"""
    print(f"Loading data from {csv_path}...")

    # Read the transformed CSV
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} fight records")

    db = SessionLocal()

    try:
        # Track fighters and fights
        fighters_created = 0
        fights_created = 0

        print("Migrating data to database...")

        for idx, row in df.iterrows():
            # Get or create fighters
            red_fighter = get_or_create_fighter(db, row['RedFighter'])
            blue_fighter = get_or_create_fighter(db, row['BlueFighter'])

            # Create fight record
            fight = Fight(
                red_fighter_id=red_fighter.id,
                blue_fighter_id=blue_fighter.id,
                date=pd.to_datetime(row['Date']) if pd.notna(row['Date']) else None,
                location=row['Location'] if pd.notna(row['Location']) else None,
                country=row['Country'] if pd.notna(row['Country']) else None,
                winner=row['Winner'] if pd.notna(row['Winner']) else None,

                # Betting odds
                red_odds=float(row['RedOdds']) if pd.notna(row['RedOdds']) else None,
                blue_odds=float(row['BlueOdds']) if pd.notna(row['BlueOdds']) else None,
                red_expected_value=float(row['RedExpectedValue']) if pd.notna(row['RedExpectedValue']) else None,
                blue_expected_value=float(row['BlueExpectedValue']) if pd.notna(row['BlueExpectedValue']) else None,

                # Method odds
                red_ko_odds=float(row['RKOOdds']) if pd.notna(row['RKOOdds']) else None,
                blue_ko_odds=float(row['BKOOdds']) if pd.notna(row['BKOOdds']) else None,
                red_sub_odds=float(row['RSubOdds']) if pd.notna(row['RSubOdds']) else None,
                blue_sub_odds=float(row['BSubOdds']) if pd.notna(row['BSubOdds']) else None,
                red_dec_odds=float(row['RedDecOdds']) if pd.notna(row['RedDecOdds']) else None,
                blue_dec_odds=float(row['BlueDecOdds']) if pd.notna(row['BlueDecOdds']) else None,

                # Fight outcome
                finish_method=row['Finish'] if pd.notna(row['Finish']) else None,
                finish_details=row['FinishDetails'] if pd.notna(row['FinishDetails']) else None,
                finish_round=int(row['FinishRound']) if pd.notna(row['FinishRound']) else None,
                finish_round_time=row['FinishRoundTime'] if pd.notna(row['FinishRoundTime']) else None,
                total_fight_duration_secs=float(row['TotalFightDurationSecs']) if pd.notna(row['TotalFightDurationSecs']) else None,
            )

            # Add optional stats columns if they exist
            stat_columns = {
                'red_sig_strikes': 'RSigStrikes',
                'blue_sig_strikes': 'BSigStrikes',
                'red_total_strikes': 'RTotalStrikes',
                'blue_total_strikes': 'BTotalStrikes',
                'red_takedowns': 'RTakedowns',
                'blue_takedowns': 'BTakedowns',
            }

            for db_col, csv_col in stat_columns.items():
                if csv_col in df.columns and pd.notna(row[csv_col]):
                    setattr(fight, db_col, int(row[csv_col]))

            db.add(fight)
            fights_created += 1

            # Commit in batches of 100
            if (idx + 1) % 100 == 0:
                db.commit()
                print(f"Processed {idx + 1} fights...")

        # Final commit
        db.commit()

        print(f"\nMigration complete!")
        print(f"Fights created: {fights_created}")

        # Count unique fighters
        fighters_count = db.query(Fighter).count()
        print(f"Fighters in database: {fighters_count}")

        # Update fighter statistics
        update_fighter_stats(db)

    except Exception as e:
        print(f"Error during migration: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    # Create tables
    create_tables()

    # Migrate data from transformed CSV
    csv_path = "../ufc-master-transformed.csv"

    if Path(csv_path).exists():
        migrate_csv_data(csv_path)
    else:
        print(f"CSV file not found at {csv_path}")
        print("Please provide the correct path to your UFC data CSV file")
