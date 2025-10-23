import React from 'react';

function LoadingIndicator({ message }) {
  return (
    <div className="text-center p-10">
      <p className="text-lg font-medium text-gray-600">{message}</p>
    </div>
  );
}

export default LoadingIndicator;