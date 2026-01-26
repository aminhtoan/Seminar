import React, { useState } from "react";

export default function Search({ onSearch }) {
  const [query, setQuery] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <input
        type="text"
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
          onSearch(e.target.value); // Real-time search
        }}
        placeholder="Search posts..."
        className="search-input"
      />
      <button type="submit" className="search-btn">
        🔍
      </button>
    </form>
  );
}