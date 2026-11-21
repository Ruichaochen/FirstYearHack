import { Map } from 'react-map-gl/maplibre'
import 'maplibre-gl/dist/maplibre-gl.css'
import { setWorkerUrl } from 'maplibre-gl'
import { useState, useCallback, useRef } from 'react'
import LocationMarker from './LocationMarker'

// Let Vite build the MapLibre worker as a proper separate file
import maplibreWorkerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url'

setWorkerUrl(maplibreWorkerUrl)

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
  const [popupLocationId, setPopupLocationId] = useState(null)
  const [viewState, setViewState] = useState({
    longitude: LONDON_CENTER.lng,
    latitude: LONDON_CENTER.lat,
    zoom: 12,
  })
  const programmaticZoom = useRef(false)

  const handleMapClick = useCallback((e) => {
    // Deselect when clicking on the map (not on a marker)
    setPopupLocationId(null)
    if (onLocationSelect) {
      onLocationSelect(null)
    }
  }, [onLocationSelect])

  const handleMarkerSelect = useCallback((location) => {
    // Close any open popup and open the new one
    setPopupLocationId(location.id)
    // Fly to the selected location with a closer zoom
    programmaticZoom.current = true
    setViewState({
      longitude: location.longitude,
      latitude: location.latitude,
      zoom: 16,
    })
    /*mapInstance.current.flyTo({
      center: [location.latitude, location.longitude],
      zoom: 16,
      duration: 1000,
      essential: true,
    })*/
    if (onLocationSelect) {
      onLocationSelect(location)
    }
  }, [onLocationSelect])

  const handlePopupClose = useCallback(() => {
    setPopupLocationId(null)
  }, [])

  const handleChange = useCallback((e) => {
    // Ignore onMove events that are caused by our own programmatic zoom
    if (programmaticZoom.current) {
      programmaticZoom.current = false
      return
    }
    setViewState(e.viewState)
  }, [])

  if (loading) {
    return <div className="map-loading">Loading map...</div>
  }

  return (
      <div className="map-container">
        <Map
            {...viewState}
            onMove={handleChange}
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
                  showPopup={popupLocationId === location.id}
                  onSelect={handleMarkerSelect}
                  onPopupClose={handlePopupClose}
              />
          ))}
        </Map>
      </div>
  )
}

export default MapView
