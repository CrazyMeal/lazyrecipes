import { useLocation, useNavigate } from 'react-router-dom';
import { useEffect } from 'react';
import ShoppingList from '../components/ShoppingList';

export default function ShoppingListPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const shoppingListData = location.state?.shoppingList;

  // Redirect to recipes if no shopping list data
  useEffect(() => {
    if (!shoppingListData) {
      navigate('/recipes', { replace: true });
    }
  }, [shoppingListData, navigate]);

  if (!shoppingListData) {
    return null;
  }

  function handleBackToRecipes() {
    navigate('/recipes');
  }

  function handleStartNewSearch() {
    navigate('/recipes', { state: { resetFlow: true } });
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
          <button onClick={handleStartNewSearch} className="btn-secondary">
            Start Over
          </button>
        </div>
      </nav>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          <ShoppingList
            shoppingList={shoppingListData.shopping_list}
            totalCost={shoppingListData.total_cost}
            estimatedSavings={shoppingListData.estimated_savings}
          />

          <div className="mt-6 flex gap-4">
            <button
              onClick={handleBackToRecipes}
              className="btn-secondary flex-1"
            >
              Back to Recipes
            </button>
            <button
              onClick={handleStartNewSearch}
              className="btn-primary flex-1"
            >
              Start New Search
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
