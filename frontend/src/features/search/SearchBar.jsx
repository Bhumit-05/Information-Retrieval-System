import React from 'react';

function SearchBar({ query, setQuery, onSearch, isLoading }) {
  return (
    <form onSubmit={onSearch} className="flex space-x-2 mb-8">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search for... 'aerodynamic wing'"
        className="grow p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        type="submit"
        disabled={isLoading}
        className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 disabled:bg-gray-400"
      >
        {isLoading ? '...' : 'Search'}
      </button>
    </form>
  );
}

export default SearchBar;