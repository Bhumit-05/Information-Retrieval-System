import React from 'react';
import { Link } from 'react-router-dom'; // 1. Import Link

function ResultsList({ results, currentResults }) {
  if (!results.length) {
    return null;
  }
  console.log(results);

  return (
    <div className="space-y-4">
      <div className="text-gray-600">
        Showing {currentResults.length} of {results.length} results.
      </div>

      {currentResults.map((result) => (
        // A single result item
        <div key={result.doc_id} className="bg-white p-5 rounded-lg shadow border border-gray-200">
          <span className="text-sm font-medium text-blue-600">
            DOC ID: {result.doc_id} (Score: {result.score.toFixed(4)})
          </span>
          
          {/* 2. Replace <h2> with <Link> */}
          <Link to={`/doc/${result.doc_id}`}>
            <h2 className="text-xl font-semibold text-gray-900 mt-1 cursor-pointer hover:underline">
              {result.title}
            </h2>
          </Link>
          
          <p className="text-gray-700 mt-2">
            {result.snippet}
          </p>
        </div>
      ))}
    </div>
  );
}

export default ResultsList;