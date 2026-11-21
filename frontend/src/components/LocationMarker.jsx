import { Marker, Popup } from 'react-map-gl/maplibre'
import { useState } from 'react'

// Category-specific colors for markers
const CATEGORY_COLORS = {
  film: '#e74c3c',
  music: '#9b59b6',
  literature: '#3498db',
  tv: '#e67e22',
  theatre: '#2ecc71',
}

function LocationMarker({ location, isSelected, onSelect }) {
  const [showPopup, setShowPopup] = useState(false)
  const color = CATEGORY_COLORS[location.category] || '#3388ff'

  const handleMarkerClick = (e) => {
    e.originalEvent.stopPropagation()
    setShowPopup(true)
    if (onSelect) {
      onSelect(location)
    }
  }

  const handlePopupClose = () => {
    setShowPopup(false)
  }

  const markerStyle = {
    width: '30px',
    height: '30px',
    backgroundColor: color,
    borderRadius: '50%',
    border: '3px solid white',
    boxShadow: '0 2px 5px rgba(0,0,0,0.3)',
    cursor: 'pointer',
  }

  if (isSelected) {
    markerStyle.width = '36px'
    markerStyle.height = '36px'
    markerStyle.borderWidth = '4px'
    markerStyle.boxShadow = '0 0 0 4px rgba(0,0,0,0.2), 0 2px 8px rgba(0,0,0,0.4)'
  }

  return (
    <Marker
      longitude={location.longitude}
      latitude={location.latitude}
      anchor="bottom"
      onClick={handleMarkerClick}
    >
      <div style={markerStyle} />
      {showPopup && (
        <Popup
          longitude={location.longitude}
          latitude={location.latitude}
          anchor="bottom"
          onClose={handlePopupClose}
          closeButton={true}
          closeOnClick={false}
        >
          <div className="popup-content">
            <h3>{location.name}</h3>
            <p className="popup-category">{location.category}</p>
            {location.description && (
              <p>{location.description.length > 100 ? location.description.substring(0, 100) + '...' : location.description}</p>
            )}
          </div>
        </Popup>
      )}
    </Marker>
  )
}

export default LocationMarker
