import { Marker, Popup } from 'react-leaflet'
import L from 'leaflet'

// Category-specific colors for markers
const CATEGORY_COLORS = {
  film: '#e74c3c',
  music: '#9b59b6',
  literature: '#3498db',
  tv: '#e67e22',
  theatre: '#2ecc71',
}

function createCategoryIcon(category) {
  const color = CATEGORY_COLORS[category] || '#3388ff'

  return L.divIcon({
    className: 'custom-marker',
    html: `<div style="
      width: 30px;
      height: 30px;
      background-color: ${color};
      border-radius: 50%;
      border: 3px solid white;
      box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    "></div>`,
    iconSize: [30, 30],
    iconAnchor: [15, 15],
    popupAnchor: [0, -15],
  })
}

function LocationMarker({ location, isSelected, onSelect }) {
  const icon = createCategoryIcon(location.category)

  const handleMarkerClick = () => {
    if (onSelect) {
      onSelect(location)
    }
  }

  return (
    <Marker
      position={[location.latitude, location.longitude]}
      icon={icon}
      eventHandlers={{
        click: handleMarkerClick,
      }}
    >
      <Popup>
        <div className="popup-content">
          <h3>{location.name}</h3>
          <p className="popup-category">{location.category}</p>
          <p>{location.description.substring(0, 100)}...</p>
        </div>
      </Popup>
    </Marker>
  )
}

export default LocationMarker
