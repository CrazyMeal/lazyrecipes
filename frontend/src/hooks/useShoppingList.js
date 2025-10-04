import { useMutation } from '@tanstack/react-query';
import { api } from '../services/api';

export function useCreateShoppingList() {
  return useMutation({
    mutationFn: (recipeIds) => api.createShoppingList(recipeIds),
    onError: (error) => {
      console.error('Failed to create shopping list:', error);
    },
  });
}
