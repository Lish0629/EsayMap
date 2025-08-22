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
  const updateColor = (id, color) => {
    const layer = layers.value.find(l => l.id === id)
    if (!layer || !layer.instance || !layer.instance.renderer) return

    let rgb
    if (Array.isArray(color)) {
      rgb = color // 直接使用
    } else if (color && color.r !== undefined) {
      rgb = [color.r, color.g, color.b] // 对象转数组
    } else {
      return // 无效颜色，不处理
    }

    layer.color = rgb // 更新状态
    // 更新 ArcGIS 图层渲染器
    const symbol = layer.instance.renderer.symbol

    if (symbol.type === 'simple-marker') {
      symbol.color = color
    } else if (symbol.type === 'simple-line') {
      symbol.color = color
    } else if (symbol.type === 'simple-fill') {
      const alpha = symbol.color ? symbol.color[3] : 0.6
      symbol.color = [...color,alpha]
    }
  }
  return {
    mapView,
    layers,
    setMapView,
    addLayer,
    removeLayer,
    updateVisibility,
    updateOpacity,
    updateTitle,
    updateColor
  }
})
