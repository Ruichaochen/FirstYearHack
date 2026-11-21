const CATEGORY_LABELS = {
  film: '🎬 Film',
  music: '🎵 Music',
  literature: '📚 Literature',
  tv: '📺 TV',
  theatre: '🎭 Theatre',
}

const CATEGORY_COLORS = {
  film: '#e74c3c',
  music: '#9b59b6',
  literature: '#3498db',
  tv: '#e67e22',
  theatre: '#2ecc71',
}

function FilterBar({ categories, selectedCategories, onCategoryToggle }) {
  return (
    <div className="filter-bar">
      <div className="filter-bar-content">
        <span className="filter-label">Filter by category:</span>
        <div className="filter-buttons">
          {categories.map((category) => {
            const isSelected = selectedCategories.includes(category)
            return (
              <button
                key={category}
                className={`filter-button ${isSelected ? 'active' : ''}`}
                style={{
                  borderColor: CATEGORY_COLORS[category] || '#333',
                  backgroundColor: isSelected ? (CATEGORY_COLORS[category] || '#333') : 'transparent',
                  color: isSelected ? '#fff' : '#333',
                }}
                onClick={() => onCategoryToggle(category)}
              >
                {CATEGORY_LABELS[category] || category}
              </button>
            )
          })}
        </div>
        {selectedCategories.length > 0 && (
          <button
            className="clear-filters"
            onClick={() => {
              // Trigger toggle for each selected category to clear them
              selectedCategories.forEach((cat) => onCategoryToggle(cat))
            }}
          >
            Clear filters
          </button>
        )}
      </div>
    </div>
  )
}

export default FilterBar
