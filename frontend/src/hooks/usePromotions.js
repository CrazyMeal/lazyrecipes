import { useMutation } from '@tanstack/react-query';
import { api } from '../services/api';

export function useScrapePromotions() {
  return useMutation({
    mutationFn: (store = 'metro') => api.scrapePromotions(store),
    onError: (error) => {
      console.error('Failed to scrape promotions:', error);
    },
  });
}
