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
          {location.category_label
            ? location.category_label
            : CATEGORY_LABELS[location.category] || location.category}
        </span>
        {location.year && <span className="info-panel-year">{location.year}</span>}
        {location.fame_tier && (
          <span className="info-panel-fame">Fame: {location.fame_tier}</span>
        )}
        {location.description && (
          <p className="info-panel-description">{location.description}</p>
        )}
        {location.address && (
          <div className="info-panel-address">
            <strong>Address:</strong> {location.address}
          </div>
        )}
        {location.image && (
          <div className="info-panel-image">
            <img src={location.image} alt={location.name} />
            {location.image_by && (
              <small className="image-credit">Photo by {location.image_by}</small>
            )}
            {location.image_licence && (
              <small className="image-licence">
                {location.image_licence_url ? (
                  <a href={location.image_licence_url} target="_blank" rel="noopener noreferrer">
                    {location.image_licence}
                  </a>
                ) : (
                  location.image_licence
                )}
              </small>
            )}
          </div>
        )}
        {location.productions_list && location.productions_list.length > 0 && (
          <div className="info-panel-productions">
            <strong>Productions:</strong>
            <ul>
              {location.productions_list.map((prod) => (
                <li key={prod.id}>
                  {prod.name}
                  {prod.production_source && (
                    <small className="production-type"> ({prod.production_source})</small>
                  )}
                </li>
              ))}
            </ul>
          </div>
        )}
        <div className="info-panel-links">
          {location.wikipedia && (
            <a href={location.wikipedia} target="_blank" rel="noopener noreferrer" className="info-link">
              Wikipedia
            </a>
          )}
          {location.wikidata && (
            <a href={location.wikidata} target="_blank" rel="noopener noreferrer" className="info-link">
              Wikidata
            </a>
          )}
          {location.url && (
            <a href={location.url} target="_blank" rel="noopener noreferrer" className="info-link">
              Website
            </a>
          )}
        </div>
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
