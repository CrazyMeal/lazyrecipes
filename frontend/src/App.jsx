import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { PersistQueryClientProvider } from '@tanstack/react-query-persist-client';
import { createSyncStoragePersister } from '@tanstack/query-sync-storage-persister';
import ErrorBoundary from './components/ErrorBoundary';
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
  storage: window.sessionStorage,
  key: 'lazyrecipes-cache',
  throttleTime: 1000,
});

// Clear cache older than 10 minutes on app load
const MAX_CACHE_AGE = 10 * 60 * 1000; // 10 minutes
const cacheTimestamp = sessionStorage.getItem('lazyrecipes-cache-timestamp');
if (cacheTimestamp) {
  const age = Date.now() - parseInt(cacheTimestamp, 10);
  if (age > MAX_CACHE_AGE) {
    sessionStorage.removeItem('lazyrecipes-cache');
    sessionStorage.removeItem('lazyrecipes-cache-timestamp');
  }
} else {
  sessionStorage.setItem('lazyrecipes-cache-timestamp', Date.now().toString());
}

function App() {
  return (
    <ErrorBoundary>
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
    </ErrorBoundary>
  );
}

export default App;
