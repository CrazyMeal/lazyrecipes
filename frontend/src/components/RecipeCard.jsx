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
        <h4 className="font-semibold text-gray-900 mb-2">Ingredients:</h4>
        <ul className="space-y-1">
          {recipe.ingredients.map((ingredient, index) => (
            <li
              key={index}
              className={`text-sm flex items-center gap-2 ${
                ingredient.on_sale ? 'text-primary-700 font-medium' : 'text-gray-700'
              }`}
            >
              {ingredient.on_sale && <span className="text-green-500">💰</span>}
              <span>{ingredient.amount} {ingredient.item}</span>
            </li>
          ))}
        </ul>
      </div>

      <details className="text-sm">
        <summary className="font-semibold text-gray-900 cursor-pointer hover:text-primary-600">
          View Instructions
        </summary>
        <ol className="mt-2 space-y-2 text-gray-700 list-decimal list-inside">
          {recipe.instructions.map((instruction, index) => (
            <li key={index}>{instruction}</li>
          ))}
        </ol>
      </details>
    </div>
  );
}
