import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { API_URL } from '../../constants';
import ErrorMessage from '../../components/ErrorMessage';
import LoadingIndicator from '../../components/LoadingIndicator';

function DocumentView() {
  // --- Component-level state ---
  const [doc, setDoc] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // 1. Get the 'docId' from the URL
  const { docId } = useParams();

  // 2. Fetch data when the component loads
  useEffect(() => {
    const fetchDocument = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        const response = await fetch(`${API_URL}/doc/${docId}`);
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          const errorMessage = errorData.error || `HTTP error! Status: ${response.status}`;
          throw new Error(errorMessage);
        }
        const data = await response.json();
        setDoc(data); // Store the full document object in state
      } catch (err) {
        setError(`Failed to fetch document: ${err.message}.`);
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchDocument();
  }, [docId]); // Re-run this effect if docId changes

  // --- 3. Render component state ---
  if (isLoading) {
    return <LoadingIndicator message="Loading document..." />;
  }
  
  if (error) {
    return <ErrorMessage message={error} />;
  }

  if (!doc) {
    return null; // Should be covered by loading/error
  }

  // --- 4. Render the document view ---
  return (
    <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
      {/* Use <Link> for the back button */}
      <Link
        to="/"
        className="mb-4 inline-block px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg shadow-sm hover:bg-blue-700"
      >
        &larr; Back to Results
      </Link>
      <h2 className="text-2xl font-bold text-gray-900 mb-2">
        {doc.title}
      </h2>
      <p className="text-gray-700 leading-relaxed">
        {doc.text}
      </p>
    </div>
  );
}

export default DocumentView;