import { Map } from 'react-map-gl/maplibre'
import 'maplibre-gl/dist/maplibre-gl.css'
import LocationMarker from './LocationMarker'

const LONDON_CENTER = { lat: 51.5074, lng: -0.1278 }

// OpenStreetMap-compatible style for MapLibre (avoids MIME type issues with demotiles)
const OSM_STYLE = {
  version: 8,
  name: 'OpenStreetMap',
  sources: {
    'osm-tiles': {
      type: 'raster',
      tiles: [
        'https://a.tile.openstreetmap.org/{z}/{x}/{y}.png',
        'https://b.tile.openstreetmap.org/{z}/{x}/{y}.png',
        'https://c.tile.openstreetmap.org/{z}/{x}/{y}.png',
      ],
      tileSize: 256,
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    },
  },
  layers: [
    {
      id: 'osm-tiles-layer',
      type: 'raster',
      source: 'osm-tiles',
      minzoom: 0,
      maxzoom: 19,
    },
  ],
}

function MapView({ locations, onLocationSelect, selectedLocation, loading }) {
  if (loading) {
    return <div className="map-loading">Loading map...</div>
  }

  const handleMapClick = (e) => {
    // Deselect when clicking on the map (not on a marker)
    if (onLocationSelect) {
      onLocationSelect(null)
    }
  }

  return (
    <div className="map-container">
      <Map
        initialViewState={{
          longitude: LONDON_CENTER.lng,
          latitude: LONDON_CENTER.lat,
          zoom: 12,
        }}
        mapLib={import('maplibre-gl')}
        style={{ width: '100%', height: '100%' }}
        mapStyle={OSM_STYLE}
        onClick={handleMapClick}
      >
        {locations.map((location) => (
          <LocationMarker
            key={location.id}
            location={location}
            isSelected={selectedLocation?.id === location.id}
            onSelect={onLocationSelect}
          />
        ))}
      </Map>
    </div>
  )
}

export default MapView
