"""
Script to remove duplicate fight records from the database
"""
from database.config import SessionLocal
from database.schema import Fight, Fighter
from sqlalchemy import func

def find_and_remove_duplicates():
    db = SessionLocal()

    print("Finding duplicate fights...")

    # Get all fights
    all_fights = db.query(Fight).all()
    print(f"Total fight records: {len(all_fights)}")

    # Track unique fights and duplicates
    seen_fights = {}
    duplicate_ids = []

    for fight in all_fights:
        # Create unique key: sorted fighter IDs + date
        fighter_ids = tuple(sorted([fight.red_fighter_id, fight.blue_fighter_id]))
        fight_key = (fighter_ids, fight.date)

        if fight_key in seen_fights:
            # This is a duplicate, mark for deletion
            duplicate_ids.append(fight.id)
        else:
            # First occurrence, keep it
            seen_fights[fight_key] = fight.id

    print(f"Unique fights: {len(seen_fights)}")
    print(f"Duplicate records to delete: {len(duplicate_ids)}")

    if duplicate_ids:
        print("\nDeleting duplicates...")
        deleted_count = 0
        for fight_id in duplicate_ids:
            fight = db.query(Fight).filter(Fight.id == fight_id).first()
            if fight:
                db.delete(fight)
                deleted_count += 1
                if deleted_count % 100 == 0:
                    print(f"  Deleted {deleted_count} duplicates...")

        db.commit()
        print(f"Successfully deleted {deleted_count} duplicate fights")

    db.close()


def recalculate_fighter_stats():
    """Recalculate stats for all fighters after cleanup"""
    print("\nRecalculating fighter statistics...")
    db = SessionLocal()

    fighters = db.query(Fighter).all()

    for idx, fighter in enumerate(fighters):
        # Get all fights for this fighter
        red_fights = db.query(Fight).filter(Fight.red_fighter_id == fighter.id).all()
        blue_fights = db.query(Fight).filter(Fight.blue_fighter_id == fighter.id).all()

        total_fights = len(red_fights) + len(blue_fights)
        wins = 0
        losses = 0
        draws = 0
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
            elif fight.winner == 'Blue':
                losses += 1
            elif fight.winner and 'Draw' in fight.winner:
                draws += 1

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
            elif fight.winner == 'Red':
                losses += 1
            elif fight.winner and 'Draw' in fight.winner:
                draws += 1

            if fight.total_fight_duration_secs:
                total_duration += fight.total_fight_duration_secs

        # Update fighter stats
        fighter.total_fights = total_fights
        fighter.wins = wins
        fighter.losses = losses
        fighter.draws = draws
        fighter.win_percentage = (wins / total_fights * 100) if total_fights > 0 else 0
        fighter.ko_tko_wins = ko_wins
        fighter.submission_wins = sub_wins
        fighter.decision_wins = dec_wins
        fighter.avg_fight_duration_secs = total_duration / total_fights if total_fights > 0 else 0

        if (idx + 1) % 100 == 0:
            print(f"  Processed {idx + 1}/{len(fighters)} fighters...")

    db.commit()
    print(f"Updated stats for {len(fighters)} fighters")

    db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("CLEANING DUPLICATE FIGHT RECORDS")
    print("=" * 60)

    # Remove duplicates
    find_and_remove_duplicates()

    # Recalculate stats
    recalculate_fighter_stats()

    print("\n" + "=" * 60)
    print("CLEANUP COMPLETE!")
    print("=" * 60)

    # Verify Jon Jones as example
    db = SessionLocal()
    jj = db.query(Fighter).filter(Fighter.name == 'Jon Jones').first()
    if jj:
        print(f"\nJon Jones updated stats: {jj.wins}W-{jj.losses}L-{jj.draws}D ({jj.total_fights} total fights)")
    db.close()
