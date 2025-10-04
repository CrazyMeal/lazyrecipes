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
  // Get selected recipes
  const selectedRecipes = mockRecipes.recipes.filter(r => recipeIds.includes(r.id));

  // Track which promotional items are used and in how many recipes
  const promotionUsageMap = new Map();
  const nonPromotedIngredients = new Map();

  selectedRecipes.forEach(recipe => {
    recipe.ingredients.forEach(ingredient => {
      const key = ingredient.item.toLowerCase();

      // Check if this ingredient has a matching promotion
      const promotion = mockPromotions.promotions.find(
        p => p.item.toLowerCase() === key
      );

      if (promotion && ingredient.on_sale) {
        // Track promotional item usage
        if (promotionUsageMap.has(key)) {
          const existing = promotionUsageMap.get(key);
          existing.recipes_using += 1;
          existing.recipe_amounts.push(ingredient.amount);
        } else {
          promotionUsageMap.set(key, {
            promotion: promotion,
            recipes_using: 1,
            recipe_amounts: [ingredient.amount]
          });
        }
      } else {
        // Track non-promoted ingredient
        if (nonPromotedIngredients.has(key)) {
          const existing = nonPromotedIngredients.get(key);
          existing.count += 1;
          existing.amounts.push(ingredient.amount);
        } else {
          nonPromotedIngredients.set(key, {
            item: ingredient.item,
            count: 1,
            amounts: [ingredient.amount]
          });
        }
      }
    });
  });

  // Helper function to parse amount strings and extract numeric values
  const parseAmount = (amountStr) => {
    // Extract first number from strings like "1.5 lb", "3 tbsp", "2 medium", etc.
    const match = amountStr.match(/(\d+\.?\d*)/);
    return match ? parseFloat(match[1]) : 1; // Default to 1 if can't parse
  };

  // Build promotional items list (API compliant structure with extensions)
  const promotionalItems = Array.from(promotionUsageMap.values()).map((usage, index) => {
    const promo = usage.promotion;

    // Calculate total quantity needed by summing amounts from all recipes
    const totalQuantity = usage.recipe_amounts.reduce((sum, amountStr) => {
      return sum + parseAmount(amountStr);
    }, 0);

    // Round up to nearest whole number for practical shopping
    const suggestedQty = Math.ceil(totalQuantity);
    const suggestedQtyStr = `~${suggestedQty} ${promo.unit}`;

    // Calculate estimated cost based on actual quantity needed
    const estimatedCost = promo.price * totalQuantity;

    return {
      // Stable ID for React keys and drag-and-drop
      id: `promo-${promo.item.toLowerCase().replace(/\s+/g, '-')}-${index}`,

      // API compliant fields
      item: promo.item,
      amount: suggestedQtyStr,
      on_sale: true,
      price: parseFloat(estimatedCost.toFixed(2)),

      // Extended fields for better UX
      store: promo.store,
      unit: promo.unit,
      price_per_unit: promo.price,
      original_price: promo.original_price,
      discount: promo.discount,
      recipes_using: usage.recipes_using,
      total_quantity_needed: totalQuantity, // Exact amount for reference
      is_promotion: true
    };
  });

  // Build non-promoted items list (API compliant structure)
  const otherItems = Array.from(nonPromotedIngredients.values()).map((item, index) => {
    const amount = item.count > 1
      ? `${item.amounts[0]} (×${item.count})`
      : item.amounts[0];

    const estimatedPrice = 2.99 * item.count; // Default price for non-promoted items

    return {
      // Stable ID for React keys and drag-and-drop
      id: `item-${item.item.toLowerCase().replace(/\s+/g, '-')}-${index}`,

      // API compliant fields
      item: item.item,
      amount: amount,
      on_sale: false,
      price: parseFloat(estimatedPrice.toFixed(2)),

      // Extended field
      is_promotion: false
    };
  });

  // Combine both lists (promotional items first)
  const shoppingList = [...promotionalItems, ...otherItems];

  // Calculate totals (API compliant)
  const totalCost = shoppingList.reduce((sum, item) => sum + item.price, 0);

  const estimatedSavings = promotionalItems.reduce((sum, item) => {
    if (item.original_price && item.price_per_unit) {
      const savingsPerUnit = item.original_price - item.price_per_unit;
      return sum + (savingsPerUnit * item.recipes_using);
    }
    return sum;
  }, 0);

  return {
    shopping_list: shoppingList,
    total_cost: parseFloat(totalCost.toFixed(2)),
    estimated_savings: parseFloat(estimatedSavings.toFixed(2)),
    created_at: new Date().toISOString()
  };
};
