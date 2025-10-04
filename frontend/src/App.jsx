import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { PersistQueryClientProvider } from '@tanstack/react-query-persist-client';
import { createSyncStoragePersister } from '@tanstack/query-sync-storage-persister';
import Home from './pages/Home';
import Recipes from './pages/Recipes';
import ShoppingListPage from './pages/ShoppingListPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutes
      gcTime: 10 * 60 * 1000, // 10 minutes (previously called cacheTime)
    },
  },
});

// Create persister with 10 minute TTL
const persister = createSyncStoragePersister({
  storage: window.localStorage,
  key: 'lazyrecipes-cache',
  throttleTime: 1000,
});

// Clear cache older than 10 minutes on app load
const MAX_CACHE_AGE = 10 * 60 * 1000; // 10 minutes
const cacheTimestamp = localStorage.getItem('lazyrecipes-cache-timestamp');
if (cacheTimestamp) {
  const age = Date.now() - parseInt(cacheTimestamp, 10);
  if (age > MAX_CACHE_AGE) {
    localStorage.removeItem('lazyrecipes-cache');
    localStorage.removeItem('lazyrecipes-cache-timestamp');
  }
} else {
  localStorage.setItem('lazyrecipes-cache-timestamp', Date.now().toString());
}

function App() {
  return (
    <PersistQueryClientProvider
      client={queryClient}
      persistOptions={{
        persister,
        maxAge: MAX_CACHE_AGE,
        buster: 'v1', // Change this to invalidate all cached data
      }}
    >
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/recipes" element={<Recipes />} />
          <Route path="/shopping-list" element={<ShoppingListPage />} />
        </Routes>
      </Router>
    </PersistQueryClientProvider>
  );
}

export default App;
