export default function ShoppingList({ shoppingList, totalCost, estimatedSavings }) {
  if (!shoppingList || shoppingList.length === 0) {
    return null;
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
            className="flex justify-between items-center p-3 bg-gray-50 rounded-lg"
          >
            <div className="flex items-center gap-3">
              {item.on_sale && (
                <span className="text-green-500 text-xl">💰</span>
              )}
              <div>
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
            {item.price && (
              <div className={`font-semibold ${
                item.on_sale ? 'text-primary-700' : 'text-gray-900'
              }`}>
                ${item.price.toFixed(2)}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="border-t pt-4 space-y-2">
        <div className="flex justify-between text-lg">
          <span className="font-medium text-gray-900">Total Cost:</span>
          <span className="font-bold text-gray-900">
            ${totalCost ? totalCost.toFixed(2) : '0.00'}
          </span>
        </div>
        {estimatedSavings > 0 && (
          <div className="flex justify-between text-lg">
            <span className="font-medium text-green-700">You Save:</span>
            <span className="font-bold text-green-700">
              ${estimatedSavings.toFixed(2)}
            </span>
          </div>
        )}
      </div>

      <button
        onClick={() => window.print()}
        className="btn-secondary w-full mt-4"
      >
        Print Shopping List
      </button>
    </div>
  );
}
