import { useState, useEffect, useCallback, useRef } from 'react'
import Header from './components/Header'
import FilterBar from './components/FilterBar'
import MapView from './components/MapView'
import BottomPanel from './components/BottomPanel'
import { fetchLocations, fetchCategories } from './services/api'

function App() {
  const [locations, setLocations] = useState([])
  const [allLocations, setAllLocations] = useState([])
  const [categories, setCategories] = useState([])
  const [selectedCategories, setSelectedCategories] = useState([])
  const [searchQuery, setSearchQuery] = useState(null)
  const [selectedLocation, setSelectedLocation] = useState(null)
  const [loading, setLoading] = useState(true)
  const [initialized, setInitialized] = useState(false)
  const prevSearchRef = useRef(null)
  const prevCategoriesRef = useRef([])

  const applyFilters = useCallback((data) => {
    // Apply category filter client-side
    if (selectedCategories.length > 0) {
      return data.filter((loc) => selectedCategories.includes(loc.category))
    }
    return data
  }, [selectedCategories])

  const loadLocations = useCallback(async (search) => {
    try {
      if (search === null) {
        // No search: use cached allLocations instead of refetching
        if (allLocations.length > 0) {
          setLocations(applyFilters(allLocations))
          return
        }
      }
      // Fetch locations with the search query
      const locationsData = await fetchLocations(undefined, search)
      if (search === null) {
        setAllLocations(locationsData)
      }
      setLocations(applyFilters(locationsData))
    } catch (error) {
      console.error('Failed to load locations:', error)
    }
  }, [selectedCategories, allLocations, applyFilters])

  useEffect(() => {
    async function loadData() {
      try {
        const [locationsData, categoriesData] = await Promise.all([
          fetchLocations(),
          fetchCategories(),
        ])
        setAllLocations(locationsData)
        setLocations(locationsData)
        setCategories(categoriesData)
      } catch (error) {
        console.error('Failed to load data:', error)
      } finally {
        setLoading(false)
        setInitialized(true)
      }
    }
    loadData()
  }, [])

  // Refetch locations when search query or categories change (only after initial load)
  useEffect(() => {
    if (!initialized) return
    // Skip the first run after initialization — it's the same as the initial load
    if (prevSearchRef.current === null && prevCategoriesRef.current.length === 0 && searchQuery === null && selectedCategories.length === 0) {
      prevSearchRef.current = searchQuery
      prevCategoriesRef.current = [...selectedCategories]
      return
    }
    prevSearchRef.current = searchQuery
    prevCategoriesRef.current = [...selectedCategories]
    setLoading(true)
    loadLocations(searchQuery).then(() => setLoading(false))
  }, [searchQuery, selectedCategories, loadLocations, initialized])

  const handleCategoryToggle = (category) => {
    setSelectedCategories((prev) => {
      if (prev.includes(category)) {
        return prev.filter((c) => c !== category)
      } else {
        return [...prev, category]
      }
    })
  }

  const handleSearch = (query) => {
    setSearchQuery(query)
  }

  const handleLocationSelect = (location) => {
    setSelectedLocation(location)
  }

  return (
    <div className="app">
      <Header onSearch={handleSearch} />
      <div className="main-content">
        <MapView
          locations={locations}
          onLocationSelect={handleLocationSelect}
          selectedLocation={selectedLocation}
          loading={loading}
        />
        <FilterBar
          categories={categories}
          selectedCategories={selectedCategories}
          onCategoryToggle={handleCategoryToggle}
        />
        <BottomPanel
          location={selectedLocation}
          onClose={() => setSelectedLocation(null)}
        />
      </div>
    </div>
  )
}

export default App
