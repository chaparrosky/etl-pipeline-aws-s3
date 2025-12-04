from database.config import SessionLocal
from database.schema import Fighter, Fight

db = SessionLocal()
jj = db.query(Fighter).filter(Fighter.name == 'Jon Jones').first()

print(f'Current DB Stats: {jj.total_fights} fights, {jj.wins}W-{jj.losses}L')
print('\nRed corner fights (wins when Winner=Red):')
red_fights = db.query(Fight).filter(Fight.red_fighter_id == jj.id).all()
red_wins = sum(1 for f in red_fights if f.winner == 'Red')
print(f'  Total: {len(red_fights)}, Wins: {red_wins}')

print('\nBlue corner fights (wins when Winner=Blue):')
blue_fights = db.query(Fight).filter(Fight.blue_fighter_id == jj.id).all()
blue_wins = sum(1 for f in blue_fights if f.winner == 'Blue')
print(f'  Total: {len(blue_fights)}, Wins: {blue_wins}')

print(f'\nCalculated record: {red_wins + blue_wins}W-{len(red_fights) + len(blue_fights) - red_wins - blue_wins}L')

# Check for duplicates
print('\nChecking for duplicate fights...')
all_fights = []
for f in red_fights:
    all_fights.append((f.date, f.blue_fighter.name, 'Red'))
for f in blue_fights:
    all_fights.append((f.date, f.red_fighter.name, 'Blue'))

unique_fights = set(all_fights)
print(f'Total fight records: {len(all_fights)}')
print(f'Unique fights: {len(unique_fights)}')
print(f'Duplicates: {len(all_fights) - len(unique_fights)}')

db.close()
