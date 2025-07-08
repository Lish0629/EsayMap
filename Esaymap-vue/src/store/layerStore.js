// src/store/layerStore.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLayerStore = defineStore('layerStore', () => {
  const layers = ref([])

  const addLayer = (layerConfig) => {
    const exists = layers.value.find(l => l.id === layerConfig.id)
    if (!exists) {
      layers.value.push({ ...layerConfig })
    }
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
    layers,
    addLayer,
    removeLayer,
    updateVisibility,
    updateOpacity,
    updateTitle
  }
})
