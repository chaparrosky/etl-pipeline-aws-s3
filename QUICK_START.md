# Quick Start Guide - UFC Analytics Platform

## What We've Built

You now have a complete FastAPI backend with 5 core features:

1. **Fighter Search & Profiles** - Search any UFC fighter and view their career stats
2. **Head-to-Head Comparison** - Compare two fighters with AI analysis
3. **Fight Predictions** - ML-powered fight outcome predictions
4. **Betting Value Finder** - Discover value bets where odds don't match predictions
5. **Fight Card Analysis** - Analyze entire UFC event cards

## Setup Instructions

### Step 1: Install PostgreSQL

**Windows:**
1. Download from https://www.postgresql.org/download/windows/
2. Install with default settings
3. Remember the password you set for postgres user

**Or use Docker:**
```bash
docker run --name ufc-postgres -e POSTGRES_PASSWORD=yourpassword -p 5432:5432 -d postgres
```

### Step 2: Create Database

```bash
# Using psql command line
psql -U postgres
CREATE DATABASE ufc_analytics;
\q
```

Or using pgAdmin (GUI tool that comes with PostgreSQL)

### Step 3: Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env with your database info
# DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/ufc_analytics
```

### Step 4: Migrate Data to Database

```bash
# Make sure you're in the backend directory
cd backend

# Run migration script
python database/migrate_csv_to_db.py
```

This will:
- Create all database tables
- Load your UFC data from the CSV
- Calculate fighter statistics
- Takes about 30-60 seconds

### Step 5: Start the API

```bash
# Still in backend directory
python main.py
```

API will start at: http://localhost:8000
API Documentation: http://localhost:8000/docs (interactive!)

## Testing the API

### Option 1: Use the Interactive Docs

Go to http://localhost:8000/docs and try:

1. **GET /api/v1/fighters/search** - Search for "mcgregor"
2. **GET /api/v1/fighters/{id}** - Get fighter profile
3. **POST /api/v1/predictions/head-to-head** - Compare two fighters
4. **GET /api/v1/predictions/betting-value** - Find value bets

### Option 2: Use cURL (Command Line)

```bash
# Search for a fighter
curl "http://localhost:8000/api/v1/fighters/search?query=silva"

# Get API stats
curl http://localhost:8000/api/v1/stats

# Head-to-head comparison
curl -X POST http://localhost:8000/api/v1/predictions/head-to-head \
  -H "Content-Type: application/json" \
  -d "{\"fighter1_name\": \"Jon Jones\", \"fighter2_name\": \"Daniel Cormier\"}"

# Find betting value
curl http://localhost:8000/api/v1/predictions/betting-value?min_value_percentage=5
```

### Option 3: Python Script

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Search fighters
response = requests.get(f"{BASE_URL}/fighters/search", params={"query": "silva"})
print(response.json())

# Head-to-head
response = requests.post(
    f"{BASE_URL}/predictions/head-to-head",
    json={
        "fighter1_name": "Jon Jones",
        "fighter2_name": "Daniel Cormier"
    }
)
print(response.json())
```

## API Endpoints Reference

### Fighter Endpoints

| Endpoint | Method | Description | Free Tier |
|----------|--------|-------------|-----------|
| `/api/v1/fighters/search` | GET | Search fighters by name | ✅ Yes |
| `/api/v1/fighters/{id}` | GET | Get fighter profile | ✅ Yes |
| `/api/v1/fighters/name/{name}` | GET | Get fighter by exact name | ✅ Yes |
| `/api/v1/fighters/` | GET | List top fighters | ✅ Yes |
| `/api/v1/fighters/{id}/stats/timeline` | GET | Fighter performance timeline | 💎 Premium |

### Prediction Endpoints

| Endpoint | Method | Description | Free Tier |
|----------|--------|-------------|-----------|
| `/api/v1/predictions/head-to-head` | POST | Compare two fighters | ✅ Limited |
| `/api/v1/predictions/predict` | POST | Predict fight outcome | 💎 Premium |
| `/api/v1/predictions/betting-value` | GET | Find betting opportunities | 💎 Premium |
| `/api/v1/predictions/fight-card/{event}` | GET | Analyze event card | 💎 Premium |

## Next Steps

### Option A: Build the Frontend (Recommended)

Create a Next.js app to visualize this data:

```bash
# In project root
npx create-next-app@latest frontend
cd frontend
npm install recharts axios @tanstack/react-query
```

### Option B: Test More Features

Try analyzing real UFC data:
- Search for your favorite fighters
- Compare historic matchups
- Find betting value in past fights
- Analyze fight cards

### Option C: Improve the ML Model

Train a real ML model:

```bash
cd backend
python ml/train_model.py  # (You'll need to create this)
```

## Troubleshooting

### Database Connection Error
- Check PostgreSQL is running: `pg_isready`
- Verify DATABASE_URL in .env is correct
- Make sure database exists: `psql -U postgres -l`

### Migration Fails
- Check CSV file path in migrate_csv_to_db.py (line 184)
- Ensure ufc-master-transformed.csv exists
- Try with smaller batch size

### API Won't Start
- Check port 8000 is available
- Activate virtual environment: `venv\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`

### No Fighters Found
- Run migration script again
- Check database has data: `psql -U postgres -d ufc_analytics -c "SELECT COUNT(*) FROM fighters;"`

## Project Structure

```
etl-pipeline-aws-s3/
├── backend/
│   ├── api/
│   │   ├── fighters.py       # Fighter endpoints
│   │   └── predictions.py    # Prediction endpoints
│   ├── database/
│   │   ├── schema.py         # Database models
│   │   ├── config.py         # DB connection
│   │   └── migrate_csv_to_db.py  # Migration script
│   ├── models/
│   │   └── schemas.py        # API response models
│   ├── services/
│   │   └── ml_predictor.py   # Prediction logic
│   ├── main.py               # FastAPI app
│   └── requirements.txt      # Dependencies
├── ufc-master-transformed.csv # Your UFC data
└── README_PRODUCT.md         # Product documentation
```

## What's Been Implemented

✅ Database schema with fighters, fights, predictions
✅ Fighter search and profiles
✅ Head-to-head comparisons with analysis
✅ ML prediction model (rule-based, ready for ML)
✅ Betting value detection
✅ Fight card analysis
✅ API documentation

## What's Next

🔲 Frontend (Next.js + React)
🔲 Authentication & user accounts
🔲 Stripe payment integration
🔲 Deployment
🔲 Marketing & launch

Ready to continue? Choose:
1. Build the frontend
2. Add authentication
3. Train better ML model
4. Deploy to production

Let me know which you'd like to tackle next!
