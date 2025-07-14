// src/store/mapStore.js
import { defineStore } from 'pinia'
import {ref,shallowRef } from 'vue'

export const useMapStore = defineStore('mapStore', () => {
  const mapView = shallowRef(null)
  const layers = ref([])

  const setMapView = (view) => {
    mapView.value = view
  }

  const addLayer = (layerConfig) => {
    const exists = layers.value.find(l => l.id === layerConfig.id)
    if (!exists) {
      layers.value.push({ ...layerConfig })
    }
    mapView.value.map.add(layerConfig.instance)
  }

  const removeLayer = (id) => {
    const index = layers.value.findIndex(l => l.id === id)
    if (index !== -1) layers.value.splice(index, 1)
  }

  const updateVisibility = (id, visible) => {
    const layer = layers.value.find(l => l.id === id)
    if (layer) {
      layer.visible = visible
      if (layer.instance) layer.instance.visible = visible
    }
  }

  const updateOpacity = (id, opacity) => {
    const layer = layers.value.find(l => l.id === id)
    if (layer) {
      layer.opacity = opacity
      if (layer.instance) layer.instance.opacity = opacity
    }
  }

  const updateTitle = (id, title) => {
    const layer = layers.value.find(l => l.id === id)
    if (layer) layer.title = title
  }

  return {
    mapView,
    layers,
    setMapView,
    addLayer,
    removeLayer,
    updateVisibility,
    updateOpacity,
    updateTitle
  }
})
