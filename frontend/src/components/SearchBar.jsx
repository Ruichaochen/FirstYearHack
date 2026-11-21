import { useState, useCallback, useRef } from 'react'

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState('')
  const inputRef = useRef(null)
  const debounceRef = useRef(null)

  const handleInputChange = (e) => {
    const value = e.target.value
    setQuery(value)

    // Debounce the search to avoid excessive API calls
    if (debounceRef.current) {
      clearTimeout(debounceRef.current)
    }
    debounceRef.current = setTimeout(() => {
      onSearch(value.trim() || null)
    }, 300)
  }

  const handleClear = useCallback(() => {
    setQuery('')
    onSearch(null)
    if (inputRef.current) {
      inputRef.current.focus()
    }
  }, [onSearch])

  return (
    <div className="search-bar">
      <div className="search-bar-content">
        <span className="search-icon">🔍</span>
        <input
          ref={inputRef}
          type="text"
          className="search-input"
          placeholder="Search locations or productions..."
          value={query}
          onChange={handleInputChange}
        />
        {query && (
          <button className="search-clear" onClick={handleClear} title="Clear search">
            ✕
          </button>
        )}
      </div>
    </div>
  )
}

export default SearchBar
