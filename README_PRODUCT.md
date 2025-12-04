# UFC Analytics Platform

Transform your UFC data pipeline into a revenue-generating analytics platform.

## Product Overview

A freemium web application providing UFC fight statistics, ML-powered predictions, and betting value analysis.

### Revenue Model

- **Free Tier**: Basic fighter stats, limited searches (10/day), with ads
- **Premium Tier ($14.99/month)**:
  - Unlimited searches
  - ML fight predictions
  - Betting value finder
  - Historical ROI tracking
  - No ads
  - Email alerts

## Tech Stack

### Backend
- FastAPI (Python)
- PostgreSQL
- SQLAlchemy ORM
- Scikit-learn (ML predictions)

### Frontend (To Be Built)
- Next.js (React)
- TailwindCSS
- Recharts/D3.js (visualizations)
- NextAuth.js (authentication)

### Infrastructure
- Backend: Railway or Render
- Frontend: Vercel
- Database: Railway PostgreSQL or Supabase
- Payments: Stripe

## Quick Start

### 1. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your database credentials

# Create database
createdb ufc_analytics

# Migrate CSV data to PostgreSQL
python database/migrate_csv_to_db.py

# Run the API server
python main.py
```

API will be available at http://localhost:8000
API docs at http://localhost:8000/docs

### 2. Test the API

```bash
# Search fighters
curl http://localhost:8000/api/v1/fighters/search?query=mcgregor

# Get fighter profile
curl http://localhost:8000/api/v1/fighters/name/conor mcgregor

# Head-to-head comparison
curl -X POST http://localhost:8000/api/v1/predictions/head-to-head \
  -H "Content-Type: application/json" \
  -d '{"fighter1_name": "Conor McGregor", "fighter2_name": "Khabib Nurmagomedov"}'

# Get betting value opportunities
curl http://localhost:8000/api/v1/predictions/betting-value
```

## Core Features Implemented

### 1. Fighter Database API ✅
- **Endpoint**: `/api/v1/fighters/search`
- Search fighters by name
- Get detailed fighter profiles
- View career statistics and recent fights
- Timeline of fighter performance

### 2. Head-to-Head Comparison ✅
- **Endpoint**: `/api/v1/predictions/head-to-head`
- Compare any two fighters
- Shows advantages for each fighter
- Previous matchup history
- ML prediction for hypothetical fight

### 3. Fight Prediction Model ✅
- **Endpoint**: `/api/v1/predictions/predict`
- Rule-based prediction system (can be enhanced with trained ML)
- Win probability calculations
- Predicted finish method
- Key factors analysis
- Betting recommendations

### 4. Betting Value Finder ✅
- **Endpoint**: `/api/v1/predictions/betting-value`
- Identifies fights where odds don't match predictions
- Expected value calculations
- Ranked by value percentage
- Historical analysis

### 5. Fight Card Analysis ✅
- **Endpoint**: `/api/v1/predictions/fight-card/{event_name}`
- Analyze entire UFC event cards
- Predictions for all fights
- Odds comparison
- Value opportunities

## Database Schema

### Tables
1. **fighters** - Fighter profiles and career stats
2. **fights** - Individual fight records with stats
3. **predictions** - ML predictions storage
4. **users** - User accounts and subscriptions

See `backend/database/schema.py` for full schema.

## Next Steps

### Phase 1: MVP Launch (2-4 weeks)
- [ ] Build Next.js frontend
- [ ] Implement authentication with NextAuth
- [ ] Integrate Stripe payments
- [ ] Deploy to production
- [ ] Create landing page

### Phase 2: Enhanced Features
- [ ] Train actual ML model on historical data
- [ ] Add more detailed fight statistics
- [ ] Implement email alerts
- [ ] Add betting ROI tracker
- [ ] Build mobile-responsive design

### Phase 3: Growth
- [ ] SEO optimization for fighter pages
- [ ] Content marketing (blog with predictions)
- [ ] Social media integration
- [ ] Affiliate partnerships with betting sites
- [ ] API tier for developers

## ML Model Enhancement

Current: Rule-based prediction system
Future: Train with XGBoost/Random Forest on features:
- Win percentage
- Recent form (last 5 fights)
- Finishing rates (KO, submission, decision)
- Strike accuracy
- Takedown accuracy
- Experience level
- Betting odds (as feature)

## Monetization Strategy

### Month 1-2: Launch & Validation
- Goal: 100 free users
- Focus: Product validation, collect feedback
- Revenue: $0 (free tier only)

### Month 3-4: Conversion Optimization
- Goal: 5% conversion rate (5 paying users)
- Revenue: ~$75/month
- Focus: Improve predictions, add premium features

### Month 6: Growth Phase
- Goal: 500 free users, 25 premium (5% conversion)
- Revenue: ~$375/month
- Focus: SEO, content marketing, partnerships

### Year 1: Scale
- Goal: 2,000 free users, 100 premium
- Revenue: ~$1,500/month
- Consider: API tier, affiliate revenue, ads on free tier

## Marketing Channels

1. **Reddit**: r/MMA, r/ufc, r/sportsbook
2. **SEO**: Fighter name pages, fight predictions
3. **Content**: Weekly fight predictions blog
4. **Twitter/X**: Live fight analysis and predictions
5. **YouTube**: Data-driven fight breakdowns

## Development Environment

```bash
# Backend development
cd backend
python main.py

# Watch for changes
uvicorn main:app --reload

# Run tests (TODO)
pytest

# Database migrations
alembic upgrade head
```

## Contributing

This is a personal project being transformed into a digital product.
See roadmap above for planned features.

## License

MIT License - See LICENSE file
