import { useState, useMemo } from 'react'

const CATEGORY_LABELS = {
  film: 'Film',
  music: 'Music',
  literature: 'Literature',
  tv: 'TV',
  theatre: 'Theatre',
}

function BottomPanel({ location, onClose }) {
  const [showImagePopup, setShowImagePopup] = useState(false)

  const numHoles = useMemo(() => Math.max(4, Math.floor(window.innerWidth / 140)), [])

  if (!location) {
    return (
      <div className="bottom-panel">
        <div className="film-strip-top">
          {Array.from({ length: numHoles }).map((_, i) => (
            <div key={i} className="film-hole" />
          ))}
        </div>
        <div className="bottom-panel-placeholder">
          <p>Click a marker on the map to see details</p>
        </div>
        <div className="film-strip-bottom">
          {Array.from({ length: numHoles }).map((_, i) => (
            <div key={i} className="film-hole" />
          ))}
        </div>
      </div>
    )
  }

  const categoryLabel = location.category_label
    ? location.category_label
    : CATEGORY_LABELS[location.category] || location.category

  const capitalizeFirst = (str) => {
    if (!str) return str
    return str.charAt(0).toUpperCase() + str.slice(1)
  }

  return (
    <div className="bottom-panel">
      {/* Image Popup Modal */}
      {showImagePopup && location.image && (
        <div className="image-popup-overlay" onClick={() => setShowImagePopup(false)}>
          <div className="image-popup-content" onClick={(e) => e.stopPropagation()}>
            <button className="image-popup-close" onClick={() => setShowImagePopup(false)}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
            <img src={location.image} alt={location.name} />
            {location.image_by && (
              <div className="image-popup-credit">Photo by {location.image_by}</div>
            )}
          </div>
        </div>
      )}

      <div className="film-strip-top">
        {Array.from({ length: numHoles }).map((_, i) => (
          <div key={i} className="film-hole" />
        ))}
      </div>
      <div className="bottom-panel-content">
        <button className="bottom-panel-close" onClick={onClose}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>

        <div className="bottom-cards">
          {/* Card 1: Location Name */}
          <div className="bottom-card location-name-card">
            <span className="card-section-label">Location</span>
            <h2 className="location-name">{location.name}</h2>
            <span className="location-category">{categoryLabel}</span>
            {location.year && <span className="location-year">{location.year}</span>}
            {location.fame_tier && (
              <span className="location-fame">Fame: {location.fame_tier}</span>
            )}
            <div className="location-coordinates">
              <small>
                {location.latitude.toFixed(4)}, {location.longitude.toFixed(4)}
              </small>
            </div>
          </div>

          {/* Card 2: Image */}
          <div className="bottom-card image-card">
            {location.image ? (
              <div
                className="location-image-wrapper"
                onClick={() => setShowImagePopup(true)}
                title="Click to view full image"
              >
                <img src={location.image} alt={location.name} />
                <div className="image-expand-hint">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="15 3 21 3 21 9"/>
                    <polyline points="9 21 3 21 3 15"/>
                    <line x1="21" y1="3" x2="14" y2="10"/>
                    <line x1="3" y1="21" x2="10" y2="14"/>
                  </svg>
                </div>
              </div>
            ) : (
              <div className="image-placeholder">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                  <circle cx="8.5" cy="8.5" r="1.5"/>
                  <polyline points="21 15 16 10 5 21"/>
                </svg>
                <span>No image</span>
              </div>
            )}
          </div>

          {/* Card 3: Location Details */}
          <div className="bottom-card details-card">
            <span className="card-section-label">Description</span>
            {location.description && (
              <p className="location-description">{capitalizeFirst(location.description)}</p>
            )}
            {location.address && (
              <div className="location-address">
                <strong>Address:</strong> {location.address}
              </div>
            )}
            <div className="location-links">
              {location.wikipedia && (
                <a href={location.wikipedia} target="_blank" rel="noopener noreferrer" className="info-link">
                  Wikipedia
                </a>
              )}
            </div>
          </div>

          {/* Card 4: Films / Productions */}
          <div className="bottom-card films-card">
            <span className="card-section-label">Movies</span>
            {location.productions_list && location.productions_list.length > 0 ? (
              <ul className="productions-list">
                {location.productions_list.map((prod) => (
                  <li key={prod.id} className="production-item">
                    <span className="production-name">{prod.name}</span>
                    {prod.production_info && prod.production_info.length > 0 && (
                      <span className="production-meta">
                        {prod.production_info.map((info, idx) => (
                          <span key={idx} className="production-info-chip">
                            {info.year && <span className="production-year">{info.year}</span>}
                            {info.end_year && info.end_year !== info.year && (
                              <span className="production-year-range">–{info.end_year}</span>
                            )}
                            {info.relation && (
                              <span className="production-relation"> · {info.relation}</span>
                            )}
                            {info.wikipedia && (
                              <a href={info.wikipedia} target="_blank" rel="noopener noreferrer" className="production-wiki">
                                Wiki
                              </a>
                            )}
                          </span>
                        ))}
                      </span>
                    )}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="no-productions">No productions listed</p>
            )}
          </div>
        </div>
      </div>
      <div className="film-strip-bottom">
        {Array.from({ length: numHoles }).map((_, i) => (
          <div key={i} className="film-hole" />
        ))}
      </div>
    </div>
  )
}

export default BottomPanel
