export default function RecipeCard({ recipe, onSelect, isSelected }) {
  return (
    <div className={`card hover:shadow-lg transition-shadow duration-200 ${
      isSelected ? 'ring-2 ring-primary-500' : ''
    }`}>
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-bold text-gray-900 mb-2">
            {recipe.name}
          </h3>
          <p className="text-gray-600 text-sm mb-3">{recipe.description}</p>
        </div>
        <input
          type="checkbox"
          checked={isSelected}
          onChange={() => onSelect(recipe.id)}
          className="ml-4 h-5 w-5 text-primary-600 rounded focus:ring-primary-500"
        />
      </div>

      <div className="flex gap-4 mb-4 text-sm text-gray-600">
        <div className="flex items-center gap-1">
          <span>⏱️</span>
          <span>{recipe.cooking_time}</span>
        </div>
        <div className="flex items-center gap-1">
          <span>👥</span>
          <span>{recipe.servings} servings</span>
        </div>
      </div>

      <div className="mb-4">
        <h4 className="font-semibold text-gray-900 mb-3">Ingredients:</h4>
        <ul className="space-y-2">
          {recipe.ingredients.map((ingredient, index) => (
            <li
              key={index}
              className={`text-sm flex items-center justify-between gap-3 px-3 py-2 rounded-lg transition-colors ${
                ingredient.on_sale
                  ? 'bg-green-50 border border-green-200'
                  : 'bg-gray-50'
              }`}
            >
              <span className={`flex-1 ${ingredient.on_sale ? 'text-gray-900 font-medium' : 'text-gray-700'}`}>
                {ingredient.amount} {ingredient.item}
              </span>
              {ingredient.on_sale && (
                <span className="flex items-center gap-1 text-xs font-semibold text-green-700 bg-green-100 px-2 py-1 rounded-full">
                  <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z" />
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clipRule="evenodd" />
                  </svg>
                  On Sale
                </span>
              )}
            </li>
          ))}
        </ul>
      </div>

      <div className="border-t pt-4">
        <h4 className="font-semibold text-gray-900 mb-3">Instructions:</h4>
        <ol className="space-y-3">
          {recipe.instructions.map((instruction, index) => (
            <li key={index} className="flex gap-3 text-sm text-gray-700">
              <span className="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 text-primary-700 font-semibold flex items-center justify-center text-xs">
                {index + 1}
              </span>
              <span className="flex-1 pt-0.5">{instruction}</span>
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
}
