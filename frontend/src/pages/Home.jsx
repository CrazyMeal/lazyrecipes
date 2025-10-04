import { useNavigate } from 'react-router-dom';

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            LazyRecipes
          </h1>
          <p className="text-xl md:text-2xl text-gray-700 mb-4">
            Save money on groceries with AI-powered recipe suggestions
          </p>
          <p className="text-lg text-gray-600 mb-12">
            We scan weekly grocery store promotions and generate delicious recipes
            that help you maximize your savings
          </p>

          <button
            onClick={() => navigate('/recipes')}
            className="btn-primary text-lg px-8 py-4 shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
          >
            Find This Week's Best Recipes
          </button>

          <div className="grid md:grid-cols-3 gap-8 mt-16">
            <div className="card">
              <div className="text-4xl mb-4">🛒</div>
              <h3 className="text-xl font-semibold mb-2">Smart Shopping</h3>
              <p className="text-gray-600">
                Automatically finds the best deals from local grocery stores
              </p>
            </div>

            <div className="card">
              <div className="text-4xl mb-4">🤖</div>
              <h3 className="text-xl font-semibold mb-2">AI-Powered</h3>
              <p className="text-gray-600">
                Generates personalized recipes using items currently on sale
              </p>
            </div>

            <div className="card">
              <div className="text-4xl mb-4">💰</div>
              <h3 className="text-xl font-semibold mb-2">Save Money</h3>
              <p className="text-gray-600">
                Track your savings and build your shopping list effortlessly
              </p>
            </div>
          </div>

          <div className="mt-16 p-6 bg-white rounded-lg shadow-md">
            <h2 className="text-2xl font-bold mb-4">How It Works</h2>
            <div className="grid md:grid-cols-4 gap-4 text-left">
              <div>
                <div className="font-bold text-primary-600 mb-2">1. Scrape</div>
                <p className="text-sm text-gray-600">
                  We scan current grocery store flyers for promotions
                </p>
              </div>
              <div>
                <div className="font-bold text-primary-600 mb-2">2. Generate</div>
                <p className="text-sm text-gray-600">
                  AI creates recipes using discounted ingredients
                </p>
              </div>
              <div>
                <div className="font-bold text-primary-600 mb-2">3. Select</div>
                <p className="text-sm text-gray-600">
                  Choose the recipes that fit your taste
                </p>
              </div>
              <div>
                <div className="font-bold text-primary-600 mb-2">4. Shop</div>
                <p className="text-sm text-gray-600">
                  Get a complete shopping list with estimated savings
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
