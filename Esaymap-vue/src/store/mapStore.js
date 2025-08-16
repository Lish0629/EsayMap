import { defineStore } from 'pinia'
import { ref, shallowRef } from 'vue'
import * as geometryEngine from "@arcgis/core/geometry/geometryEngine";

export const useMapStore = defineStore('mapStore', () => {
  const mapView = shallowRef(null)
  const layers = ref([])

  const setMapView = (view) => {
    mapView.value = view
  }

  const getLayerExtent = async (layer) => {
    try {
      // FeatureLayer
      if (layer.type === "feature") {
        const result = await layer.queryExtent()
        return result.extent
      }

      // MapImageLayer / TileLayer / VectorTileLayer
      if (layer.fullExtent) {
        return layer.fullExtent
      }

      // GraphicsLayer
      if (layer.type === "graphics" && layer.graphics.length > 0) {
        const geometries = layer.graphics.map(g => g.geometry)
        return geometryEngine.union(geometries).extent
      }

    } catch (err) {
      console.warn("计算图层范围失败:", err)
    }
    return null
  }

  const addLayer = async (layerConfig) => {
    const exists = layers.value.find(l => l.id === layerConfig.id)
    if (!exists) {
      layers.value.push({ ...layerConfig })
    }

    mapView.value.map.add(layerConfig.instance)

    try {
      await layerConfig.instance.when() // 确保加载完成
      const extent = await getLayerExtent(layerConfig.instance)

      if (extent) {
        await mapView.value.goTo(extent.expand(1.2)) // 适度放大，避免贴边
      }
    } catch (err) {
      console.warn("缩放到图层范围失败:", err)
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
