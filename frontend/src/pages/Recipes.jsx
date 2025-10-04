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
