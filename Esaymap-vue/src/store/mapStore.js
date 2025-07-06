import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useMapStore = defineStore('mapStore', () => {
  const mapView = ref(null)

  const setMapView = (view) => {
    mapView.value = view
  }

  return {
    mapView,
    setMapView,
  }
})
