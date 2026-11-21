import { useState, useRef } from 'react'

function Header({ onSearch }) {
  const [query, setQuery] = useState('')
  const inputRef = useRef(null)
  const debounceRef = useRef(null)

  const handleInputChange = (e) => {
    const value = e.target.value
    setQuery(value)
    if (debounceRef.current) {
      clearTimeout(debounceRef.current)
    }
    debounceRef.current = setTimeout(() => {
      onSearch(value.trim() || null)
    }, 300)
  }

  const handleClear = () => {
    setQuery('')
    onSearch(null)
    if (inputRef.current) {
      inputRef.current.focus()
    }
  }

  return (
    <header className="header">
      <div className="header-branding">
        <h1 className="header-title">LONDON</h1>
        <p className="header-subtitle">A CITY IN FRAMES</p>
      </div>
      <div className="header-search">
        <span className="search-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
        </span>
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
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        )}
      </div>
    </header>
  )
}

export default Header
