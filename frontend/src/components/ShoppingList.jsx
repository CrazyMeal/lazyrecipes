import PropTypes from 'prop-types';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  useSortable,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';

// Sortable item component with drag handle
function SortableItem({ item, onRemoveItem }) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: item.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`shopping-list-item flex items-center gap-3 p-3 bg-gray-50 rounded-lg ${
        isDragging ? 'shadow-lg' : 'hover:bg-gray-100'
      } transition-colors`}
    >
      {/* Drag Handle */}
      <button
        {...attributes}
        {...listeners}
        className="drag-handle cursor-grab active:cursor-grabbing text-gray-400 hover:text-gray-600 p-1"
        aria-label="Drag to reorder"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-5 w-5"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
        </svg>
      </button>

      {/* Item Content */}
      <div className="flex items-center gap-3 flex-1">
        <div className="flex-1">
          {item.is_promotion ? (
            // Promotional item display
            <>
              <div className="font-medium text-gray-900">
                {item.item}
              </div>
              <div className="text-sm text-gray-600">
                ${item.price_per_unit.toFixed(2)}/{item.unit} at {item.store}
                {item.recipes_using > 1 && (
                  <span className="ml-2 text-primary-600">
                    • Used in {item.recipes_using} recipes
                  </span>
                )}
              </div>
              <div className="text-sm text-gray-500">
                Suggested: {item.amount}
              </div>
            </>
          ) : (
            // Regular ingredient display
            <>
              <div className="font-medium text-gray-900">
                {item.amount} {item.item}
              </div>
            </>
          )}
        </div>
      </div>

      {/* Price and Remove Button */}
      <div className="flex items-center gap-3">
        {item.price && (
          <div className={`font-semibold ${
            item.on_sale ? 'text-primary-700' : 'text-gray-900'
          }`}>
            ${item.price.toFixed(2)}
            {item.discount && (
              <span className="text-sm text-green-600 ml-1">
                ({item.discount})
              </span>
            )}
          </div>
        )}
        {onRemoveItem && (
          <button
            onClick={() => onRemoveItem(item.id)}
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
  );
}

export default function ShoppingList({
  shoppingList,
  totalCost,
  estimatedSavings,
  onRemoveItem,
  onReorder,
}) {
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  if (!shoppingList || shoppingList.length === 0) {
    return (
      <div className="card text-center py-8">
        <p className="text-gray-500 text-lg">
          No items in your shopping list
        </p>
      </div>
    );
  }

  // Separate promotional items from other ingredients
  const promotionalItems = shoppingList.filter(item => item.is_promotion);
  const otherItems = shoppingList.filter(item => !item.is_promotion);

  // All items should have IDs from the API/mock data
  // Log warning if any items are missing IDs
  if (shoppingList.some(item => !item.id)) {
    console.warn('Shopping list items missing IDs - this may cause drag-and-drop issues');
  }

  function handleDragEnd(event) {
    const { active, over } = event;

    if (over && active.id !== over.id) {
      const oldIndex = shoppingList.findIndex((item) => item.id === active.id);
      const newIndex = shoppingList.findIndex((item) => item.id === over.id);

      const newOrder = arrayMove(shoppingList, oldIndex, newIndex);
      onReorder(newOrder);
    }
  }

  return (
    <div className="card">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">
        Your Shopping List
      </h2>

      <DndContext
        sensors={sensors}
        collisionDetection={closestCenter}
        onDragEnd={handleDragEnd}
        aria-label="Reorderable shopping list items"
      >
        <SortableContext
          items={shoppingList}
          strategy={verticalListSortingStrategy}
        >
          {/* Promotional Items Section */}
          {promotionalItems.length > 0 && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-primary-700 mb-3 flex items-center gap-2">
                <span>💰</span>
                Items On Sale
              </h3>
              <div className="space-y-3">
                {promotionalItems.map((item) => (
                  <SortableItem
                    key={item.id}
                    item={item}
                    onRemoveItem={onRemoveItem}
                  />
                ))}
              </div>
            </div>
          )}

          {/* Other Ingredients Section */}
          {otherItems.length > 0 && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-700 mb-3 flex items-center gap-2">
                <span>🛒</span>
                Other Ingredients
              </h3>
              <div className="space-y-3">
                {otherItems.map((item) => (
                  <SortableItem
                    key={item.id}
                    item={item}
                    onRemoveItem={onRemoveItem}
                  />
                ))}
              </div>
            </div>
          )}
        </SortableContext>
      </DndContext>

      <div className="border-t pt-4 space-y-2">
        <div className="flex justify-between text-lg">
          <span className="text-gray-700">Estimated Total:</span>
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
        <p className="text-sm text-gray-500 italic mt-2">
          * Actual cost may vary based on quantities purchased
        </p>
      </div>

      <button
        onClick={() => window.print()}
        className="btn-secondary w-full mt-4 flex items-center justify-center gap-2"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-5 w-5"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fillRule="evenodd"
            d="M5 4v3H4a2 2 0 00-2 2v3a2 2 0 002 2h1v2a2 2 0 002 2h6a2 2 0 002-2v-2h1a2 2 0 002-2V9a2 2 0 00-2-2h-1V4a2 2 0 00-2-2H7a2 2 0 00-2 2zm8 0H7v3h6V4zm0 8H7v4h6v-4z"
            clipRule="evenodd"
          />
        </svg>
        Print Shopping List
      </button>
    </div>
  );
}

// PropTypes for type safety
const shoppingListItemShape = PropTypes.shape({
  id: PropTypes.string.isRequired,
  item: PropTypes.string.isRequired,
  amount: PropTypes.string,
  price: PropTypes.number,
  on_sale: PropTypes.bool,
  is_promotion: PropTypes.bool,
  store: PropTypes.string,
  unit: PropTypes.string,
  price_per_unit: PropTypes.number,
  original_price: PropTypes.number,
  discount: PropTypes.string,
  recipes_using: PropTypes.number,
});

SortableItem.propTypes = {
  item: shoppingListItemShape.isRequired,
  onRemoveItem: PropTypes.func,
};

ShoppingList.propTypes = {
  shoppingList: PropTypes.arrayOf(shoppingListItemShape).isRequired,
  totalCost: PropTypes.number.isRequired,
  estimatedSavings: PropTypes.number.isRequired,
  onRemoveItem: PropTypes.func,
  onReorder: PropTypes.func,
};
