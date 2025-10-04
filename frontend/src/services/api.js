const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

class APIError extends Error {
  constructor(message, status, details) {
    super(message);
    this.name = 'APIError';
    this.status = status;
    this.details = details;
  }
}

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
  async scrapePromotions(store = 'metro') {
    return fetchAPI('/api/scrape', {
      method: 'POST',
      body: JSON.stringify({ store }),
    });
  },

  async generateRecipes(promotions, numRecipes = 5, preferences = {}) {
    return fetchAPI('/api/recipes/generate', {
      method: 'POST',
      body: JSON.stringify({
        promotions,
        num_recipes: numRecipes,
        preferences,
      }),
    });
  },

  async createShoppingList(recipeIds) {
    return fetchAPI('/api/shopping-list', {
      method: 'POST',
      body: JSON.stringify({
        recipe_ids: recipeIds,
      }),
    });
  },

  async healthCheck() {
    return fetchAPI('/health');
  },
};
