import { useMutation } from '@tanstack/react-query';
import { api } from '../services/api';

export function useGenerateRecipes() {
  return useMutation({
    mutationFn: ({ promotions, numRecipes = 5, preferences = {} }) =>
      api.generateRecipes(promotions, numRecipes, preferences),
    onError: (error) => {
      console.error('Failed to generate recipes:', error);
    },
  });
}
