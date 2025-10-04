import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import RecipeCard from '../components/RecipeCard';
import ShoppingList from '../components/ShoppingList';
import { useScrapePromotions } from '../hooks/usePromotions';
import { useGenerateRecipes } from '../hooks/useRecipes';
import { useCreateShoppingList } from '../hooks/useShoppingList';

export default function Recipes() {
  const navigate = useNavigate();
  const [step, setStep] = useState('initial');
  const [selectedRecipes, setSelectedRecipes] = useState(new Set());

  const scrapeMutation = useScrapePromotions();
  const generateMutation = useGenerateRecipes();
  const shoppingListMutation = useCreateShoppingList();

  useEffect(() => {
    startScraping();
  }, []);

  async function startScraping() {
    setStep('promotions');

    try {
      const scrapeData = await scrapeMutation.mutateAsync('metro');
      const recipesData = await generateMutation.mutateAsync({
        promotions: scrapeData.promotions,
        numRecipes: 5,
      });
      setStep('recipes');
    } catch (err) {
      setStep('initial');
    }
  }

  async function createShoppingList() {
    if (selectedRecipes.size === 0) {
      return;
    }

    const recipeIds = Array.from(selectedRecipes);
    await shoppingListMutation.mutateAsync(recipeIds);
    setStep('shopping-list');
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
    setSelectedRecipes(new Set());
    scrapeMutation.reset();
    generateMutation.reset();
    shoppingListMutation.reset();
    startScraping();
  }

  const isLoading = scrapeMutation.isPending || generateMutation.isPending || shoppingListMutation.isPending;
  const error = scrapeMutation.error || generateMutation.error || shoppingListMutation.error;

  const promotions = scrapeMutation.data?.promotions || [];
  const store = scrapeMutation.data?.store || 'Metro';
  const recipes = generateMutation.data?.recipes || [];
  const shoppingList = shoppingListMutation.data;

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
              <span className="font-medium">{error.message || 'An error occurred'}</span>
            </div>
          </div>
        )}

        {isLoading && (
          <div className="flex flex-col items-center justify-center py-16">
            <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-primary-600 mb-4"></div>
            <p className="text-lg text-gray-600">
              {scrapeMutation.isPending && 'Scanning grocery stores for promotions...'}
              {generateMutation.isPending && 'Generating delicious recipes...'}
              {shoppingListMutation.isPending && 'Creating your shopping list...'}
            </p>
          </div>
        )}

        {!isLoading && step === 'recipes' && (
          <div>
            <h2 className="text-3xl font-bold text-gray-900 mb-6">
              Recipe Suggestions
            </h2>

            <div className="flex gap-6">
              {/* Left Column - Recipes */}
              <div className="flex-1">
                <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
                  {recipes.map(recipe => (
                    <RecipeCard
                      key={recipe.id}
                      recipe={recipe}
                      onSelect={toggleRecipeSelection}
                      isSelected={selectedRecipes.has(recipe.id)}
                    />
                  ))}
                </div>
              </div>

              {/* Right Column - Shopping Cart */}
              <div className="w-80 flex-shrink-0">
                <div className="sticky top-6 bg-white rounded-lg shadow-lg border border-gray-200 p-6">
                  <h3 className="text-xl font-bold text-gray-900 mb-4">
                    Shopping Cart
                  </h3>

                  {selectedRecipes.size === 0 ? (
                    <div className="text-center py-8">
                      <div className="text-5xl mb-3">🛒</div>
                      <p className="text-gray-500 text-sm">
                        Select recipes to add them to your cart
                      </p>
                    </div>
                  ) : (
                    <>
                      <div className="mb-4">
                        <div className="text-sm text-gray-600 mb-3">
                          {selectedRecipes.size} recipe{selectedRecipes.size !== 1 ? 's' : ''} selected
                        </div>
                        <div className="space-y-2 max-h-96 overflow-y-auto">
                          {recipes
                            .filter(recipe => selectedRecipes.has(recipe.id))
                            .map(recipe => (
                              <div
                                key={recipe.id}
                                className="flex items-start justify-between gap-2 p-3 bg-gray-50 rounded-lg border border-gray-200"
                              >
                                <div className="flex-1 min-w-0">
                                  <div className="font-medium text-gray-900 text-sm truncate">
                                    {recipe.name}
                                  </div>
                                  <div className="text-xs text-gray-500 mt-1">
                                    {recipe.servings} servings • {recipe.cooking_time}
                                  </div>
                                </div>
                                <button
                                  onClick={() => toggleRecipeSelection(recipe.id)}
                                  className="text-gray-400 hover:text-red-600 transition-colors flex-shrink-0"
                                  title="Remove"
                                >
                                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                  </svg>
                                </button>
                              </div>
                            ))}
                        </div>
                      </div>

                      <button
                        onClick={createShoppingList}
                        className="btn-primary w-full py-3 shadow-lg hover:shadow-xl transition-shadow"
                      >
                        Create Shopping List
                      </button>
                    </>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {!isLoading && step === 'shopping-list' && shoppingList && (
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
