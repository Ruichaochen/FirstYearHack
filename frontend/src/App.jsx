import { useState, useEffect } from 'react'
import Header from './components/Header'
import FilterBar from './components/FilterBar'
import MapView from './components/MapView'
import InfoPanel from './components/InfoPanel'
import { fetchLocations, fetchCategories } from './services/api'

function App() {
  const [locations, setLocations] = useState([])
  const [categories, setCategories] = useState([])
  const [selectedCategories, setSelectedCategories] = useState([])
  const [selectedLocation, setSelectedLocation] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadData() {
      try {
        const [locationsData, categoriesData] = await Promise.all([
          fetchLocations(),
          fetchCategories(),
        ])
        setLocations(locationsData)
        setCategories(categoriesData)
      } catch (error) {
        console.error('Failed to load data:', error)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [])

  const handleCategoryToggle = (category) => {
    setSelectedCategories((prev) => {
      if (prev.includes(category)) {
        return prev.filter((c) => c !== category)
      } else {
        return [...prev, category]
      }
    })
  }

  const handleLocationSelect = (location) => {
    setSelectedLocation(location)
  }

  const filteredLocations =
    selectedCategories.length > 0
      ? locations.filter((loc) => selectedCategories.includes(loc.category))
      : locations

  return (
    <div className="app">
      <Header />
      <FilterBar
        categories={categories}
        selectedCategories={selectedCategories}
        onCategoryToggle={handleCategoryToggle}
      />
      <div className="main-content">
        <MapView
          locations={filteredLocations}
          onLocationSelect={handleLocationSelect}
          selectedLocation={selectedLocation}
          loading={loading}
        />
        <InfoPanel
          location={selectedLocation}
          onClose={() => setSelectedLocation(null)}
        />
      </div>
    </div>
  )
}

export default App
