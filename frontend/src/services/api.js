const API_BASE = '/api'

export async function fetchLocations(category) {
  const url = category ? `${API_BASE}/locations?category=${category}` : `${API_BASE}/locations`
  const response = await fetch(url)
  if (!response.ok) throw new Error('Failed to fetch locations')
  return response.json()
}

export async function fetchLocationById(id) {
  const response = await fetch(`${API_BASE}/locations/${id}`)
  if (!response.ok) throw new Error('Failed to fetch location')
  return response.json()
}

export async function fetchCategories() {
  const response = await fetch(`${API_BASE}/categories`)
  if (!response.ok) throw new Error('Failed to fetch categories')
  return response.json()
}
