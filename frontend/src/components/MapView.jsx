import { MapContainer, TileLayer, useMapEvents, Marker } from 'react-leaflet'
import { useState } from 'react'
import L from 'leaflet'
import LocationMarker from './LocationMarker'
import 'leaflet/dist/leaflet.css'

// Fix for default marker icon issue in Leaflet with webpack/vite
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
})

const LONDON_CENTER = [51.5074, -0.1278]

function LocationClickHandler({ onLocationSelect }) {
  useMapEvents({
    click(e) {
      // Deselect when clicking on the map (not on a marker)
      if (onLocationSelect) {
        onLocationSelect(null)
      }
    },
  })
  return null
}

function MapView({ locations, onLocationSelect, selectedLocation, loading }) {
  if (loading) {
    return <div className="map-loading">Loading map...</div>
  }

  return (
    <div className="map-container">
      <MapContainer
        center={LONDON_CENTER}
        zoom={12}
        scrollWheelZoom={true}
        className="map"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <LocationClickHandler onLocationSelect={onLocationSelect} />
        {locations.map((location) => (
          <LocationMarker
            key={location.id}
            location={location}
            isSelected={selectedLocation?.id === location.id}
            onSelect={onLocationSelect}
          />
        ))}
      </MapContainer>
    </div>
  )
}

export default MapView
