export default function PromotionsList({ promotions, store }) {
  if (!promotions || promotions.length === 0) {
    return null;
  }

  return (
    <div className="card">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">
        Current Promotions at {store}
      </h2>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {promotions.map((promo, index) => (
          <div
            key={index}
            className="border border-primary-200 rounded-lg p-4 bg-primary-50"
          >
            <h3 className="font-semibold text-gray-900 mb-1">{promo.item}</h3>
            <div className="flex justify-between items-center">
              <span className="text-2xl font-bold text-primary-700">
                ${promo.price.toFixed(2)}
              </span>
              {promo.unit && (
                <span className="text-sm text-gray-600">per {promo.unit}</span>
              )}
            </div>
            {promo.discount && (
              <div className="mt-2 inline-block bg-green-500 text-white text-xs font-medium px-2 py-1 rounded">
                {promo.discount}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
