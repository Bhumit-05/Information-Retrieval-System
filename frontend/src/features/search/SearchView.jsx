import React from 'react';
import { RESULTS_PER_PAGE } from '../../constants';
import Pagination from '../../components/Pagination';
import ErrorMessage from '../../components/ErrorMessage';
import LoadingIndicator from '../../components/LoadingIndicator';
import SearchBar from './SearchBar';
import ResultsList from './ResultsList';

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

  const indexOfLastResult = currentPage * RESULTS_PER_PAGE;
  const indexOfFirstResult = indexOfLastResult - RESULTS_PER_PAGE;
  const currentResults = results.slice(indexOfFirstResult, indexOfLastResult);

  return (
    <>
      <ErrorMessage message={error} />
    
      <SearchBar
        query={query}
        setQuery={setQuery}
        onSearch={onSearch}
        isLoading={isLoading}
      />

      {isLoading && <LoadingIndicator message="Searching..." />}

      {!isLoading && results.length > 0 && (
        <>
          <ResultsList
            results={results}
            currentResults={currentResults}
          />
          
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