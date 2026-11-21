const CATEGORY_LABELS = {
  film: '🎬 Film',
  music: '🎵 Music',
  literature: '📚 Literature',
  tv: '📺 TV',
  theatre: '🎭 Theatre',
}

function FilterBar({ categories, selectedCategories, onCategoryToggle }) {
  return (
    <div className="filter-bar">
      <div className="filter-buttons">
        {categories.map((category) => {
          const isSelected = selectedCategories.includes(category)
          return (
            <button
              key={category}
              className={`filter-button ${isSelected ? 'active' : ''}`}
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
            selectedCategories.forEach((cat) => onCategoryToggle(cat))
          }}
        >
          Clear
        </button>
      )}
    </div>
  )
}

export default FilterBar
