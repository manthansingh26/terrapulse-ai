# TerraPulse AI Frontend

React + TypeScript frontend for the TerraPulse AI environmental intelligence platform.

## Pages

- `Login` and `Register`
- `Dashboard`
- `Map`
- `Analytics`
- `Model Lab`
- `Profile`

## Model Lab Features

The Model Lab is the ML operations workspace:

- Model health cards
- Data freshness status
- Time-based validation status
- Training data quality panel
- Animated training pipeline
- Run history
- Run comparison
- Prediction quality chart
- Feature importance chart
- Prediction explanations
- 24-hour city forecasts
- ML alert checks
- Retraining action

## Visual Polish

- Branded opening animation
- Staggered health-card reveal
- Animated ML training pipeline
- Animated explanation cards
- Responsive dashboard layout
- Reduced-motion support for users who prefer less animation

## Requirements

- Node.js 18+
- npm
- Backend running at `http://127.0.0.1:8000`

## Start Development Server

```powershell
cd frontend
npm install
npm run dev -- --host 127.0.0.1
```

Open:

```text
http://127.0.0.1:3000/
```

Login:

```text
username: demo
password: demo123
```

## Verification

```powershell
npm run lint
npm run type-check
npm run build
```

## API Integration

The frontend API client is in:

```text
frontend/src/services/api.ts
```

Main backend API base:

```text
http://localhost:8000/api
```

Key frontend ML calls:

- `getMLMetrics`
- `getMLRunHistory`
- `getMLDataQuality`
- `getFeatureImportance`
- `getEvaluationSamples`
- `getAllForecasts`
- `getTopForecastExplanations`
- `trainAQIModel`
- `checkAllMLForecastAlerts`

## Project Structure

```text
frontend/src/
  components/
    AppIntro.tsx
    Layout.tsx
    ProtectedRoute.tsx
  context/
    AuthContext.tsx
  hooks/
    useAuth.ts
    useWebSocket.ts
  pages/
    Analytics.tsx
    Dashboard.tsx
    Login.tsx
    Map.tsx
    ModelLab.tsx
    Profile.tsx
    Register.tsx
  services/
    api.ts
  styles/
    global.css
```

## Known Improvement

The production build currently warns that the JS bundle is larger than 500 kB. This is non-blocking. The next frontend optimization should be route-level lazy loading with `React.lazy`.

