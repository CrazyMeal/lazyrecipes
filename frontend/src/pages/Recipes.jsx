import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import RecipeCard from '../components/RecipeCard';
import PromotionsList from '../components/PromotionsList';
import ShoppingList from '../components/ShoppingList';

export default function Recipes() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [step, setStep] = useState('initial'); // initial, promotions, recipes, shopping-list

  const [promotions, setPromotions] = useState([]);
  const [store, setStore] = useState('Metro');
  const [recipes, setRecipes] = useState([]);
  const [selectedRecipes, setSelectedRecipes] = useState(new Set());
  const [shoppingList, setShoppingList] = useState(null);

  useEffect(() => {
    startScraping();
  }, []);

  async function startScraping() {
    setLoading(true);
    setError(null);
    setStep('promotions');

    try {
      const data = await api.scrapePromotions('metro');
      setPromotions(data.promotions);
      setStore(data.store);

      await generateRecipes(data.promotions);
    } catch (err) {
      setError(err.message || 'Failed to scrape promotions');
      setStep('initial');
    } finally {
      setLoading(false);
    }
  }

  async function generateRecipes(promos) {
    setLoading(true);
    setError(null);

    try {
      const data = await api.generateRecipes(promos, 5);
      setRecipes(data.recipes);
      setStep('recipes');
    } catch (err) {
      setError(err.message || 'Failed to generate recipes');
    } finally {
      setLoading(false);
    }
  }

  async function createShoppingList() {
    if (selectedRecipes.size === 0) {
      setError('Please select at least one recipe');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const recipeIds = Array.from(selectedRecipes);
      const data = await api.createShoppingList(recipeIds);
      setShoppingList(data);
      setStep('shopping-list');
    } catch (err) {
      setError(err.message || 'Failed to create shopping list');
    } finally {
      setLoading(false);
    }
  }

  function toggleRecipeSelection(recipeId) {
    setSelectedRecipes(prev => {
      const newSet = new Set(prev);
      if (newSet.has(recipeId)) {
        newSet.delete(recipeId);
      } else {
        newSet.add(recipeId);
      }
      return newSet;
    });
  }

  function resetFlow() {
    setStep('initial');
    setPromotions([]);
    setRecipes([]);
    setSelectedRecipes(new Set());
    setShoppingList(null);
    setError(null);
    startScraping();
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <button
            onClick={() => navigate('/')}
            className="text-2xl font-bold text-primary-600 hover:text-primary-700"
          >
            LazyRecipes
          </button>
          {step !== 'initial' && (
            <button onClick={resetFlow} className="btn-secondary">
              Start Over
            </button>
          )}
        </div>
      </nav>

      <div className="container mx-auto px-4 py-8">
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center gap-2 text-red-800">
              <span className="text-xl">⚠️</span>
              <span className="font-medium">{error}</span>
            </div>
          </div>
        )}

        {loading && (
          <div className="flex flex-col items-center justify-center py-16">
            <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-primary-600 mb-4"></div>
            <p className="text-lg text-gray-600">
              {step === 'promotions' && 'Scanning grocery stores for promotions...'}
              {step === 'recipes' && 'Generating delicious recipes...'}
              {step === 'shopping-list' && 'Creating your shopping list...'}
            </p>
          </div>
        )}

        {!loading && step === 'recipes' && (
          <>
            <div className="mb-8">
              <PromotionsList promotions={promotions} store={store} />
            </div>

            <div className="mb-8">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-3xl font-bold text-gray-900">
                  Recipe Suggestions
                </h2>
                <div className="text-gray-600">
                  {selectedRecipes.size} recipe{selectedRecipes.size !== 1 ? 's' : ''} selected
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                {recipes.map(recipe => (
                  <RecipeCard
                    key={recipe.id}
                    recipe={recipe}
                    onSelect={toggleRecipeSelection}
                    isSelected={selectedRecipes.has(recipe.id)}
                  />
                ))}
              </div>

              <div className="mt-8 flex justify-center">
                <button
                  onClick={createShoppingList}
                  disabled={selectedRecipes.size === 0}
                  className="btn-primary text-lg px-8 py-4 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Create Shopping List ({selectedRecipes.size} recipe{selectedRecipes.size !== 1 ? 's' : ''})
                </button>
              </div>
            </div>
          </>
        )}

        {!loading && step === 'shopping-list' && shoppingList && (
          <div className="max-w-2xl mx-auto">
            <ShoppingList
              shoppingList={shoppingList.shopping_list}
              totalCost={shoppingList.total_cost}
              estimatedSavings={shoppingList.estimated_savings}
            />

            <div className="mt-6 flex gap-4">
              <button
                onClick={() => setStep('recipes')}
                className="btn-secondary flex-1"
              >
                Back to Recipes
              </button>
              <button
                onClick={resetFlow}
                className="btn-primary flex-1"
              >
                Start New Search
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
