import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';

export function useGetRecipes(numRecipes = 5, preferences = {}) {
  return useQuery({
    queryKey: ['recipes', numRecipes, preferences],
    queryFn: () => api.getRecipes(numRecipes, preferences),
    staleTime: 0, // Always fetch fresh data from backend
    gcTime: 0, // Don't cache
    retry: 1,
  });
}
