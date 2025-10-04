// Mock data for frontend development while backend is being implemented

export const mockPromotions = {
  promotions: [
    {
      item: "Chicken breast",
      price: 4.99,
      unit: "lb",
      store: "Metro",
      discount: "30% off",
      original_price: 7.13
    },
    {
      item: "Honey",
      price: 3.49,
      unit: "375ml",
      store: "Metro",
      discount: "Save $1.50",
      original_price: 4.99
    },
    {
      item: "Brown rice",
      price: 2.99,
      unit: "2lb bag",
      store: "Metro",
      discount: "40% off",
      original_price: 4.99
    },
    {
      item: "Bell peppers",
      price: 1.99,
      unit: "3-pack",
      store: "Metro",
      discount: "Save $2.00",
      original_price: 3.99
    },
    {
      item: "Garlic",
      price: 0.99,
      unit: "bulb",
      store: "Metro",
      discount: "50% off",
      original_price: 1.98
    },
    {
      item: "Soy sauce",
      price: 2.49,
      unit: "250ml",
      store: "Metro",
      discount: "Save $1.00",
      original_price: 3.49
    },
    {
      item: "Olive oil",
      price: 6.99,
      unit: "500ml",
      store: "Metro",
      discount: "25% off",
      original_price: 9.32
    },
    {
      item: "Tomatoes",
      price: 2.49,
      unit: "lb",
      store: "Metro",
      discount: "Save $1.50",
      original_price: 3.99
    },
    {
      item: "Pasta",
      price: 1.49,
      unit: "500g",
      store: "Metro",
      discount: "40% off",
      original_price: 2.49
    },
    {
      item: "Parmesan cheese",
      price: 4.99,
      unit: "200g",
      store: "Metro",
      discount: "Save $2.00",
      original_price: 6.99
    }
  ],
  store: "Metro",
  scraped_at: new Date().toISOString()
};

export const mockRecipes = {
  recipes: [
    {
      id: "recipe_1",
      name: "Honey Garlic Chicken Stir-Fry",
      description: "Quick and delicious weeknight dinner with tender chicken in a sweet garlic sauce",
      ingredients: [
        { item: "Chicken breast", amount: "1.5 lb", on_sale: true },
        { item: "Honey", amount: "3 tbsp", on_sale: true },
        { item: "Garlic", amount: "4 cloves", on_sale: true },
        { item: "Soy sauce", amount: "2 tbsp", on_sale: true },
        { item: "Bell peppers", amount: "2 medium", on_sale: true },
        { item: "Olive oil", amount: "2 tbsp", on_sale: true },
        { item: "Salt", amount: "1 tsp", on_sale: false },
        { item: "Black pepper", amount: "1/2 tsp", on_sale: false }
      ],
      instructions: [
        "Cut chicken into bite-sized pieces and season with salt and pepper",
        "Mince garlic and slice bell peppers into strips",
        "Mix honey, soy sauce, and half the garlic in a bowl",
        "Heat oil in a large pan over medium-high heat",
        "Cook chicken until golden brown (6-8 minutes)",
        "Add remaining garlic and bell peppers, cook for 3 minutes",
        "Pour in honey-soy mixture and cook until sauce thickens (2-3 minutes)",
        "Serve hot with rice or noodles"
      ],
      cooking_time: "25 mins",
      servings: 4
    },
    {
      id: "recipe_2",
      name: "Mediterranean Chicken Rice Bowl",
      description: "Healthy and flavorful rice bowl with Mediterranean-inspired ingredients",
      ingredients: [
        { item: "Chicken breast", amount: "1 lb", on_sale: true },
        { item: "Brown rice", amount: "2 cups cooked", on_sale: true },
        { item: "Tomatoes", amount: "2 medium", on_sale: true },
        { item: "Garlic", amount: "3 cloves", on_sale: true },
        { item: "Olive oil", amount: "3 tbsp", on_sale: true },
        { item: "Lemon juice", amount: "2 tbsp", on_sale: false },
        { item: "Oregano", amount: "1 tsp", on_sale: false },
        { item: "Feta cheese", amount: "1/2 cup", on_sale: false }
      ],
      instructions: [
        "Cook brown rice according to package directions",
        "Season chicken with oregano, salt, and pepper",
        "Heat 1 tbsp olive oil in a pan and cook chicken (6-7 minutes per side)",
        "Dice tomatoes and mince garlic",
        "Mix tomatoes, garlic, remaining olive oil, and lemon juice",
        "Slice cooked chicken into strips",
        "Assemble bowls with rice, chicken, tomato mixture, and feta",
        "Drizzle with extra olive oil if desired"
      ],
      cooking_time: "35 mins",
      servings: 4
    },
    {
      id: "recipe_3",
      name: "Honey Roasted Chicken with Vegetables",
      description: "Simple one-pan roasted chicken with sweet honey glaze and colorful vegetables",
      ingredients: [
        { item: "Chicken breast", amount: "2 lb", on_sale: true },
        { item: "Honey", amount: "1/4 cup", on_sale: true },
        { item: "Bell peppers", amount: "3 medium", on_sale: true },
        { item: "Garlic", amount: "6 cloves", on_sale: true },
        { item: "Olive oil", amount: "3 tbsp", on_sale: true },
        { item: "Thyme", amount: "2 tsp", on_sale: false },
        { item: "Salt", amount: "1 tsp", on_sale: false },
        { item: "Black pepper", amount: "1 tsp", on_sale: false }
      ],
      instructions: [
        "Preheat oven to 400°F (200°C)",
        "Cut bell peppers into chunks and place in a baking dish",
        "Add whole garlic cloves to the vegetables",
        "Season chicken with salt, pepper, and thyme",
        "Place chicken on top of vegetables",
        "Drizzle everything with olive oil and honey",
        "Roast for 35-40 minutes until chicken is cooked through",
        "Let rest for 5 minutes before serving"
      ],
      cooking_time: "50 mins",
      servings: 6
    },
    {
      id: "recipe_4",
      name: "Creamy Garlic Parmesan Pasta",
      description: "Rich and creamy pasta dish with garlic and fresh parmesan cheese",
      ingredients: [
        { item: "Pasta", amount: "500g", on_sale: true },
        { item: "Parmesan cheese", amount: "1 cup grated", on_sale: true },
        { item: "Garlic", amount: "6 cloves", on_sale: true },
        { item: "Olive oil", amount: "1/4 cup", on_sale: true },
        { item: "Heavy cream", amount: "1 cup", on_sale: false },
        { item: "Butter", amount: "2 tbsp", on_sale: false },
        { item: "Fresh basil", amount: "1/4 cup", on_sale: false },
        { item: "Salt and pepper", amount: "to taste", on_sale: false }
      ],
      instructions: [
        "Cook pasta according to package directions, reserve 1 cup pasta water",
        "Mince garlic finely",
        "Heat olive oil and butter in a large pan over medium heat",
        "Sauté garlic until fragrant (about 1 minute)",
        "Add heavy cream and bring to a gentle simmer",
        "Stir in parmesan cheese until melted",
        "Toss cooked pasta in the sauce, adding pasta water if needed",
        "Season with salt and pepper, garnish with fresh basil"
      ],
      cooking_time: "20 mins",
      servings: 4
    },
    {
      id: "recipe_5",
      name: "Asian-Style Rice with Honey Chicken",
      description: "Flavorful fried rice topped with sweet and savory honey-glazed chicken",
      ingredients: [
        { item: "Chicken breast", amount: "1.5 lb", on_sale: true },
        { item: "Brown rice", amount: "3 cups cooked", on_sale: true },
        { item: "Honey", amount: "3 tbsp", on_sale: true },
        { item: "Soy sauce", amount: "1/4 cup", on_sale: true },
        { item: "Garlic", amount: "4 cloves", on_sale: true },
        { item: "Bell peppers", amount: "2 medium", on_sale: true },
        { item: "Eggs", amount: "2 large", on_sale: false },
        { item: "Green onions", amount: "3 stalks", on_sale: false },
        { item: "Sesame oil", amount: "1 tbsp", on_sale: false }
      ],
      instructions: [
        "Cut chicken into cubes and dice bell peppers",
        "Mix honey and 2 tbsp soy sauce for the glaze",
        "Cook chicken in a hot pan until done, brush with honey glaze",
        "Remove chicken and set aside",
        "Scramble eggs in the same pan, then remove",
        "Add sesame oil, minced garlic, and bell peppers",
        "Add cold cooked rice and remaining soy sauce, stir-fry for 5 minutes",
        "Mix in scrambled eggs and top with sliced chicken and green onions"
      ],
      cooking_time: "30 mins",
      servings: 5
    }
  ],
  generated_at: new Date().toISOString()
};

export const mockShoppingList = (recipeIds) => {
  // Aggregate ingredients from selected recipes
  const selectedRecipes = mockRecipes.recipes.filter(r => recipeIds.includes(r.id));

  const ingredientMap = new Map();

  selectedRecipes.forEach(recipe => {
    recipe.ingredients.forEach(ingredient => {
      const key = ingredient.item;
      if (ingredientMap.has(key)) {
        const existing = ingredientMap.get(key);
        // Simple aggregation (in real implementation, would parse amounts properly)
        existing.count += 1;
      } else {
        ingredientMap.set(key, {
          item: ingredient.item,
          amount: ingredient.amount,
          on_sale: ingredient.on_sale,
          count: 1
        });
      }
    });
  });

  const shoppingList = Array.from(ingredientMap.values()).map(item => {
    // Find matching promotion to get price
    const promotion = mockPromotions.promotions.find(
      p => p.item.toLowerCase() === item.item.toLowerCase()
    );

    const unitPrice = promotion?.price || 2.99;
    const price = unitPrice * item.count;

    return {
      item: item.item,
      amount: item.count > 1 ? `${item.amount} (×${item.count})` : item.amount,
      on_sale: item.on_sale,
      price: parseFloat(price.toFixed(2)),
      unit_price: promotion ? unitPrice : null
    };
  });

  const totalCost = shoppingList.reduce((sum, item) => sum + item.price, 0);
  const savingsPerItem = shoppingList
    .filter(item => item.on_sale && item.unit_price)
    .map(item => {
      const promotion = mockPromotions.promotions.find(
        p => p.item.toLowerCase() === item.item.toLowerCase()
      );
      if (promotion?.original_price) {
        return (promotion.original_price - promotion.price) * item.price / promotion.price;
      }
      return 0;
    });

  const estimatedSavings = savingsPerItem.reduce((sum, saving) => sum + saving, 0);

  return {
    shopping_list: shoppingList,
    total_cost: parseFloat(totalCost.toFixed(2)),
    estimated_savings: parseFloat(estimatedSavings.toFixed(2)),
    created_at: new Date().toISOString()
  };
};
