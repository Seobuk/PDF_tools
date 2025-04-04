import React, { useState } from 'react';

function Button({ onClick, children }) {
  const [isLoading, setIsLoading] = useState(false);
  
  const handleClick = async () => {
    setIsLoading(true);
    await onClick();
    setIsLoading(false);
  };

  return (
    <button 
      className={`button ${isLoading ? 'loading' : ''}`}
      onClick={handleClick}
      disabled={isLoading}
    >
      {isLoading ? '처리중...' : children}
    </button>
  );
}

export default Button; 