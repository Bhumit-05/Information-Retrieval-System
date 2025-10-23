import { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import { API_URL } from './constants';

// Import the new/modified route components
import SearchView from './features/search/SearchView';
import DocumentView from './features/document/DocumentView';

function App() {
  // --- All search-related state is kept here ---
  // This preserves results when navigating away and back.
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  
  // Note: All "doc" related state is GONE.
  // The DocumentView component will manage itself.

  /**
   * This function is called when the user clicks the "Search" button.
   * It will be passed down to the SearchView.
   */
  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    setError(null);
    setResults([]);
    setCurrentPage(1);

    const params = new URLSearchParams({
      q: query,
      k: 100 // Fetch 100 results for frontend pagination
    });

    try {
      const response = await fetch(`${API_URL}/search?${params}`);
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData.error || `HTTP error! Status: ${response.status}`;
        throw new Error(errorMessage);
      }
      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(`Search failed: ${err.message}. Is the backend server running?`);
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };


  // --- Render the UI ---
  return (
    <div className="min-h-screen bg-gray-100 p-4 md:p-8">
      <div className="max-w-3xl mx-auto">

        {/* Header (Stays on all pages) */}
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-6">
          Cranfield Search Engine
        </h1>
        
        {/* Define the routes */}
        <Routes>
          {/* Route 1: The main search page */}
          <Route
            path="/"
            element={
              <SearchView
                // Pass all state and handlers to the search page
                query={query}
                setQuery={setQuery}
                results={results}
                isLoading={isLoading}
                error={error}
                currentPage={currentPage}
                setCurrentPage={setCurrentPage}
                onSearch={handleSearch}
              />
            }
          />

          {/* Route 2: The document page, with a dynamic docId */}
          {/* This component will fetch its own data */}
          <Route path="/doc/:docId" element={<DocumentView />} />
          
        </Routes>
      </div>
    </div>
  );
}

export default App;