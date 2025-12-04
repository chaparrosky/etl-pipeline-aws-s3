# How to Run Your UFC Analytics Platform

Follow these steps to see your product live!

## Step 1: Start the Backend API

Open a terminal and run:

```bash
cd backend

# Activate virtual environment (if not already activated)
# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

# Start the FastAPI server
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**API is now running at http://localhost:8000**

Test it by visiting http://localhost:8000/docs in your browser - you'll see the interactive API documentation!

## Step 2: Start the Frontend

Open a **NEW** terminal (keep the backend running) and run:

```bash
cd frontend

# Start the React app
npm run dev
```

You should see:
```
  VITE v7.x.x  ready in XXX ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

**Frontend is now running at http://localhost:3000**

## Step 3: Use Your Product!

Open your browser and go to **http://localhost:3000**

You should see your UFC Analytics platform!

### Things to Try:

1. **Home Page** - View top fighters and stats
2. **Search** - Click "Search Fighters" and search for "silva" or "jones"
3. **Fighter Profile** - Click on any fighter to see their detailed profile
4. **Head-to-Head** - Click "Head-to-Head" and compare "Jon Jones" vs "Daniel Cormier"

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Find and kill the process
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

**Database not set up:**
- Run the migration script first: `python backend/database/migrate_csv_to_db.py`

### Frontend Issues

**Port 3000 already in use:**
- Vite will automatically use the next available port (3001, 3002, etc.)
- Or kill the process using port 3000

**API errors / CORS issues:**
- Make sure the backend is running BEFORE starting the frontend
- Check that both are on localhost

**Module not found:**
```bash
cd frontend
npm install
```

## Development Workflow

### Making Changes - See Them Live!

**Backend changes:**
- FastAPI automatically reloads when you save Python files
- No need to restart the server

**Frontend changes:**
- Vite hot-reloads automatically
- Changes appear instantly in the browser
- No need to refresh (most of the time)

### Recommended Terminal Setup

Have 2 terminals open:
1. **Terminal 1**: Backend (running `python main.py`)
2. **Terminal 2**: Frontend (running `npm run dev`)

## What You're Seeing

When you run both servers, you have a FULL STACK application:

```
Browser (localhost:3000)
    ↓
React Frontend
    ↓
API Calls (axios)
    ↓
FastAPI Backend (localhost:8000)
    ↓
PostgreSQL Database
    ↓
Your UFC Data!
```

## Quick Commands Reference

### Backend
```bash
cd backend
venv\Scripts\activate          # Activate virtual env
python main.py                 # Start server
python database/migrate_csv_to_db.py  # Migrate data
```

### Frontend
```bash
cd frontend
npm install                    # Install dependencies
npm run dev                    # Start dev server
npm run build                  # Build for production
```

## Next Steps

Now that you can see your app live:

1. **Try the features** - Search fighters, compare them, see predictions
2. **Make changes** - Edit files and watch them update live
3. **Add features** - Build new pages, add visualizations
4. **Deploy** - When ready, deploy to production

Enjoy your UFC Analytics platform! 🥊
