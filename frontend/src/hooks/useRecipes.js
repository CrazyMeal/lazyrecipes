import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';

export function useGetRecipes(numRecipes = 5, preferences = {}) {
  return useQuery({
    queryKey: ['recipes', numRecipes, preferences],
    queryFn: () => api.getRecipes(numRecipes, preferences),
    staleTime: 5 * 60 * 1000, // 5 minutes - recipes considered fresh
    gcTime: 10 * 60 * 1000, // 10 minutes - keep in cache (matches global TTL)
    retry: 1,
  });
}
