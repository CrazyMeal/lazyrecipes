import { mockRecipes, mockShoppingList } from './mockData';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';
const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK_DATA === 'true';

class APIError extends Error {
  constructor(message, status, details) {
    super(message);
    this.name = 'APIError';
    this.status = status;
    this.details = details;
  }
}

// Helper to simulate API delay
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function fetchAPI(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    const data = await response.json();

    if (!response.ok) {
      throw new APIError(
        data.error || 'API request failed',
        response.status,
        data.details
      );
    }

    return data;
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    throw new APIError('Network error', 0, error.message);
  }
}

export const api = {
  async getRecipes(numRecipes = 5, preferences = {}) {
    if (USE_MOCK_DATA) {
      await delay(150); // Minimal delay for smooth UI transitions
      return mockRecipes;
    }
    // Backend will handle promotion scraping internally
    return fetchAPI('/api/recipes', {
      method: 'GET',
      // Query params for customization
    });
  },

  async createShoppingList(recipeIds) {
    if (USE_MOCK_DATA) {
      await delay(100); // Minimal delay for smooth UI transitions
      return mockShoppingList(recipeIds);
    }
    return fetchAPI('/api/shopping-list', {
      method: 'POST',
      body: JSON.stringify({
        recipe_ids: recipeIds,
      }),
    });
  },

  async healthCheck() {
    if (USE_MOCK_DATA) {
      await delay(200);
      return { status: 'healthy (mock)', timestamp: new Date().toISOString() };
    }
    return fetchAPI('/health');
  },
};
