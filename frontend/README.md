# UFC Analytics Frontend

React + TypeScript + Vite frontend for the UFC Analytics platform.

## Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

The app will be available at http://localhost:3000

**IMPORTANT**: Make sure the backend API is running at http://localhost:8000 before starting the frontend.

## Features

- **Fighter Search** - Search for any UFC fighter
- **Fighter Profiles** - Detailed stats and recent fight history
- **Head-to-Head** - AI-powered fighter comparisons
- **Fight Predictions** - ML predictions with win probabilities
- **Responsive Design** - Works on mobile and desktop

## Project Structure

```
src/
├── components/
│   └── Layout.tsx          # Navigation and footer
├── pages/
│   ├── Home.tsx            # Landing page
│   ├── FighterSearch.tsx   # Fighter search
│   ├── FighterProfile.tsx  # Fighter details
│   └── HeadToHead.tsx      # Fighter comparison
├── services/
│   └── api.ts              # API client
├── App.tsx                 # Main app with routing
├── main.tsx                # Entry point
└── index.css               # Global styles
```

## Development

```bash
# Run dev server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Connecting to Backend

The frontend is configured to proxy API requests to the backend.

Vite proxy configuration in `vite.config.ts`:
```typescript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
  }
}
```

Make sure your backend is running before starting the frontend!

## Technologies

- React 19
- TypeScript
- Vite
- React Router
- Axios (API calls)
- Recharts (future visualizations)

## Next Steps

- [ ] Add visualizations with Recharts
- [ ] Implement authentication
- [ ] Add premium features
- [ ] Mobile optimization
- [ ] SEO improvements
