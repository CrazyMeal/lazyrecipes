import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';

export function useScrapePromotions(store = 'metro') {
  return useQuery({
    queryKey: ['promotions', store],
    queryFn: () => api.scrapePromotions(store),
    staleTime: 5 * 60 * 1000, // 5 minutes - promotions considered fresh
    gcTime: 10 * 60 * 1000, // 10 minutes - keep in cache (matches global TTL)
    retry: 1,
  });
}
