import React from 'react';
import { RESULTS_PER_PAGE } from '../../constants';

// Reusable Components
import Pagination from '../../components/Pagination';
import ErrorMessage from '../../components/ErrorMessage';
import LoadingIndicator from '../../components/LoadingIndicator';

// Feature Components
import SearchBar from './SearchBar';
import ResultsList from './ResultsList';

/**
 * This component renders the complete search UI (bar, results, pagination).
 * It is a "container" for the search feature.
 */
function SearchView({
  query,
  setQuery,
  results,
  isLoading,
  error,
  currentPage,
  setCurrentPage,
  onSearch
}) {

  // --- Pagination Logic (Moved from App.js) ---
  const indexOfLastResult = currentPage * RESULTS_PER_PAGE;
  const indexOfFirstResult = indexOfLastResult - RESULTS_PER_PAGE;
  const currentResults = results.slice(indexOfFirstResult, indexOfLastResult);

  return (
    <>
      {/* Error Message */}
      <ErrorMessage message={error} />
    
      {/* Search Bar */}
      <SearchBar
        query={query}
        setQuery={setQuery}
        onSearch={onSearch}
        isLoading={isLoading}
      />

      {/* Loading Spinner for Search */}
      {isLoading && <LoadingIndicator message="Searching..." />}

      {/* Results List */}
      {!isLoading && results.length > 0 && (
        <>
          <ResultsList
            results={results}
            currentResults={currentResults}
            // onDocClick is no longer needed, Link is used inside
          />
          
          {/* Pagination Controls */}
          <Pagination
            currentPage={currentPage}
            totalResults={results.length}
            resultsPerPage={RESULTS_PER_PAGE}
            onPageChange={setCurrentPage}
          />
        </>
      )}
    </>
  );
}

export default SearchView;