# LazyRecipes Frontend

React frontend for the LazyRecipes hackathon PoC application.

## Setup

```bash
npm install
```

## Development

```bash
npm run dev
```

The application will run on http://localhost:3000

## Configuration

Create a `.env` file (or copy from `.env.example`):

```env
VITE_API_URL=http://localhost:5000
```

## Project Structure

```
src/
├── components/         # Reusable UI components
│   ├── RecipeCard.jsx
│   ├── PromotionsList.jsx
│   └── ShoppingList.jsx
├── pages/             # Page components
│   ├── Home.jsx
│   └── Recipes.jsx
├── services/          # API service layer
│   └── api.js
├── App.jsx           # Main app component with routing
├── main.jsx          # Application entry point
└── index.css         # Global styles with Tailwind

```

## Features

- **Smart Shopping**: Automatically finds promotions from grocery stores
- **AI-Powered Recipes**: Generates recipes using OpenAI based on sale items
- **Shopping List**: Creates consolidated shopping list with cost tracking
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- React 18
- Vite (build tool)
- Tailwind CSS (styling)
- React Router (navigation)

## Backend Integration

The frontend connects to the Flask backend API (default: http://localhost:5000). Ensure the backend is running before starting the frontend.

API endpoints:
- `POST /api/scrape` - Scrape promotions
- `POST /api/recipes/generate` - Generate recipes
- `POST /api/shopping-list` - Create shopping list

See `backend/api_spec.yaml` for complete API documentation.
