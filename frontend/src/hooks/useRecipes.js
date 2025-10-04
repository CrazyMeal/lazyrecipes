import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';

export function useGenerateRecipes(promotions, numRecipes = 5, preferences = {}) {
  // Create a stable cache key based on the promotions content
  const promotionsKey = promotions
    ? JSON.stringify(promotions.map(p => `${p.item}_${p.price}`))
    : null;

  return useQuery({
    queryKey: ['recipes', promotionsKey, numRecipes, preferences],
    queryFn: () => api.generateRecipes(promotions, numRecipes, preferences),
    enabled: !!promotions && promotions.length > 0, // Only run if we have promotions
    staleTime: 5 * 60 * 1000, // 5 minutes - recipes considered fresh
    gcTime: 10 * 60 * 1000, // 10 minutes - keep in cache (matches global TTL)
    retry: 1,
  });
}
