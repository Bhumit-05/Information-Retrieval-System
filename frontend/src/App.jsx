import { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import { API_URL } from './constants';
import SearchView from './features/search/SearchView';
import DocumentView from './features/document/DocumentView';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  
  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    setError(null);
    setResults([]);
    setCurrentPage(1);

    const params = new URLSearchParams({
      q: query,
      k: 100
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

  return (
    <div className="min-h-screen bg-gray-100 p-4 md:p-8">
      <div className="max-w-3xl mx-auto">

        <h1 className="text-3xl font-bold text-center text-gray-800 mb-6">
          Information Retrieval System
        </h1>
        
        <Routes>
          <Route
            path="/"
            element={
              <SearchView
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
          <Route path="/doc/:docId" element={<DocumentView />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;