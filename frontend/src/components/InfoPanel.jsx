const CATEGORY_LABELS = {
  film: '🎬 Film',
  music: '🎵 Music',
  literature: '📚 Literature',
  tv: '📺 TV',
  theatre: '🎭 Theatre',
}

function InfoPanel({ location, onClose }) {
  if (!location) {
    return (
      <div className="info-panel closed">
        <div className="info-panel-placeholder">
          <p>Click a marker on the map to see details</p>
        </div>
      </div>
    )
  }

  return (
    <div className="info-panel open">
      <button className="info-panel-close" onClick={onClose}>
        ✕
      </button>
      <div className="info-panel-content">
        <h2>{location.name}</h2>
        <span className="info-panel-category">
          {CATEGORY_LABELS[location.category] || location.category}
        </span>
        {location.year && <span className="info-panel-year">{location.year}</span>}
        <p className="info-panel-description">{location.description}</p>
        {location.address && (
          <div className="info-panel-address">
            <strong>Address:</strong> {location.address}
          </div>
        )}
        {location.media_url && (
          <div className="info-panel-media">
            <a href={location.media_url} target="_blank" rel="noopener noreferrer">
              View media
            </a>
          </div>
        )}
        <div className="info-panel-coordinates">
          <small>
            {location.latitude.toFixed(4)}, {location.longitude.toFixed(4)}
          </small>
        </div>
      </div>
    </div>
  )
}

export default InfoPanel
