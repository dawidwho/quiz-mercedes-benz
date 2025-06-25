# Star Wars Frontend Application

A React-based frontend application for exploring Star Wars data with AI-powered insights.

## Features

### Core Features

- **People Management**: View, search, sort, and manage Star Wars characters
- **Planets Management**: View, search, sort, and manage Star Wars planets
- **Pagination**: Navigate through large datasets with 15 items per page
- **Search**: Case-insensitive partial matching for names
- **Sorting**: Sort by name and creation date in ascending/descending order

### AI Insights Features (New!)

- **People AI Insights**: Generate AI-powered analysis for Star Wars characters
- **Planets AI Insights**: Generate AI-powered analysis for Star Wars planets
- **Insight Storage**: Save and manage generated insights locally
- **Confidence Scoring**: View confidence levels for each AI-generated insight
- **Real-time Generation**: Get instant AI insights with loading states

## Navigation

The application includes the following main sections:

- **People**: Browse and manage Star Wars characters
- **People Insights**: Generate AI insights for characters
- **Planets**: Browse and manage Star Wars planets
- **Planets Insights**: Generate AI insights for planets

## AI Insights Usage

1. Navigate to either "People Insights" or "Planets Insights"
2. Enter the name of a character or planet
3. Click "Generate Insight" to get AI-powered analysis
4. View the generated insight with confidence score
5. Save insights for later reference
6. Remove individual insights or clear all saved insights

## Technology Stack

- **React 19**: Modern React with latest features
- **React Router 7**: Client-side routing
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Vite**: Fast build tool and dev server

## Development

### Prerequisites

- Node.js 18+
- npm or yarn

### Setup

1. Install dependencies:

   ```bash
   npm install
   ```

2. Start development server:

   ```bash
   npm run dev
   ```

3. Build for production:

   ```bash
   npm run build
   ```

4. Type checking:
   ```bash
   npm run typecheck
   ```

## API Integration

The frontend integrates with the Star Wars API backend:

- **Base URL**: `http://localhost:8000/api`
- **People Endpoints**: `/people/` for CRUD operations
- **Planets Endpoints**: `/planets/` for CRUD operations
- **AI Insights Endpoint**: `/simulate-ai-insight/` for AI analysis

## Project Structure

```
app/
├── components/          # Reusable UI components
│   ├── Navigation.tsx   # Main navigation
│   ├── InsightsCard.tsx # AI insights component
│   └── ...
├── pages/              # Page components
│   ├── people.tsx      # People list page
│   ├── people-insights.tsx # People AI insights
│   ├── planets.tsx     # Planets list page
│   ├── planets-insights.tsx # Planets AI insights
│   └── ...
├── services/           # API clients
│   ├── apiClientStarWars.ts # Star Wars API client
│   └── apiClientInsights.ts # AI insights API client
├── models/             # TypeScript interfaces
│   ├── people.ts       # People data models
│   ├── planets.ts      # Planets data models
│   └── insights.ts     # AI insights models
└── ...
```
