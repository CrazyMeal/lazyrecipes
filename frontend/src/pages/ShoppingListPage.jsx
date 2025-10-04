import { useLocation, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import ShoppingList from '../components/ShoppingList';

export default function ShoppingListPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const shoppingListData = location.state?.shoppingList;

  // Generate a unique key for this shopping list session
  const shoppingListKey = 'lazyrecipes-current-shopping-list';

  // Initialize state from sessionStorage or location state
  const getInitialState = () => {
    // Try to load from sessionStorage first
    const saved = sessionStorage.getItem(shoppingListKey);
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch (e) {
        console.error('Failed to parse saved shopping list', e);
      }
    }
    // Fallback to location state
    return {
      shopping_list: shoppingListData?.shopping_list || [],
      total_cost: shoppingListData?.total_cost || 0,
      estimated_savings: shoppingListData?.estimated_savings || 0
    };
  };

  const [currentShoppingList, setCurrentShoppingList] = useState(() =>
    getInitialState().shopping_list
  );
  const [currentTotalCost, setCurrentTotalCost] = useState(() =>
    getInitialState().total_cost
  );
  const [currentSavings, setCurrentSavings] = useState(() =>
    getInitialState().estimated_savings
  );

  // Save to sessionStorage whenever state changes
  useEffect(() => {
    const dataToSave = {
      shopping_list: currentShoppingList,
      total_cost: currentTotalCost,
      estimated_savings: currentSavings
    };
    sessionStorage.setItem(shoppingListKey, JSON.stringify(dataToSave));
  }, [currentShoppingList, currentTotalCost, currentSavings]);

  // Redirect to recipes if no shopping list data
  useEffect(() => {
    if (!shoppingListData && currentShoppingList.length === 0) {
      navigate('/recipes', { replace: true });
    }
  }, [shoppingListData, currentShoppingList.length, navigate]);

  // Function to remove an item and recalculate costs
  function handleRemoveItem(itemId) {
    // Find the item by ID instead of index
    const indexToRemove = currentShoppingList.findIndex(item => {
      const id = item.id || `item-${currentShoppingList.indexOf(item)}`;
      return id === itemId;
    });

    if (indexToRemove === -1) {
      console.error('Item not found:', itemId);
      return;
    }

    const removedItem = currentShoppingList[indexToRemove];
    const newShoppingList = currentShoppingList.filter((_, index) => index !== indexToRemove);

    // Recalculate total cost
    const newTotalCost = Math.max(0, currentTotalCost - (removedItem.price || 0));

    // Recalculate savings based on actual promotional savings
    let itemSavings = 0;
    if (removedItem.is_promotion && removedItem.original_price && removedItem.price_per_unit) {
      // Use actual savings: (original - sale) * quantity
      const savingsPerUnit = removedItem.original_price - removedItem.price_per_unit;
      itemSavings = savingsPerUnit * (removedItem.recipes_using || 1);
    }
    const newSavings = Math.max(0, currentSavings - itemSavings);

    setCurrentShoppingList(newShoppingList);
    setCurrentTotalCost(newTotalCost);
    setCurrentSavings(newSavings);
  }

  // Function to handle reordering of items
  function handleReorder(newOrderedList) {
    setCurrentShoppingList(newOrderedList);
  }

  if (!shoppingListData) {
    return null;
  }

  function handleBackToRecipes() {
    navigate('/recipes');
  }

  function handleStartNewSearch() {
    // Clear saved shopping list when starting over
    sessionStorage.removeItem(shoppingListKey);
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
            shoppingList={currentShoppingList}
            totalCost={currentTotalCost}
            estimatedSavings={currentSavings}
            onRemoveItem={handleRemoveItem}
            onReorder={handleReorder}
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
