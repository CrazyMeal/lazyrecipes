export default function ShoppingList({
  shoppingList,
  totalCost,
  estimatedSavings,
  onRemoveItem
}) {
  if (!shoppingList || shoppingList.length === 0) {
    return (
      <div className="card text-center py-8">
        <p className="text-gray-500 text-lg">
          No items in your shopping list
        </p>
      </div>
    );
  }

  return (
    <div className="card">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">
        Your Shopping List
      </h2>

      <div className="space-y-3 mb-6">
        {shoppingList.map((item, index) => (
          <div
            key={index}
            className="flex justify-between items-center p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <div className="flex items-center gap-3 flex-1">
              {item.on_sale && (
                <span className="text-green-500 text-xl">💰</span>
              )}
              <div className="flex-1">
                <div className="font-medium text-gray-900">
                  {item.amount} {item.item}
                </div>
                {item.unit_price && (
                  <div className="text-sm text-gray-600">
                    ${item.unit_price.toFixed(2)} per unit
                  </div>
                )}
              </div>
            </div>
            <div className="flex items-center gap-3">
              {item.price && (
                <div className={`font-semibold ${
                  item.on_sale ? 'text-primary-700' : 'text-gray-900'
                }`}>
                  ${item.price.toFixed(2)}
                </div>
              )}
              {onRemoveItem && (
                <button
                  onClick={() => onRemoveItem(index)}
                  className="text-red-500 hover:text-red-700 hover:bg-red-50 p-2 rounded-lg transition-colors"
                  title="Remove item (already have it at home)"
                  aria-label={`Remove ${item.item} from shopping list`}
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-5 w-5"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                      clipRule="evenodd"
                    />
                  </svg>
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="border-t pt-4 space-y-2">
        <div className="flex justify-between text-lg">
          <span className="text-gray-700">Total Cost:</span>
          <span className="font-bold text-gray-900">${totalCost.toFixed(2)}</span>
        </div>
        {estimatedSavings > 0 && (
          <div className="flex justify-between text-lg">
            <span className="text-green-600">Estimated Savings:</span>
            <span className="font-bold text-green-600">
              ${estimatedSavings.toFixed(2)}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
