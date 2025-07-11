<template>
  <div class="map-container" ref="mapDiv"></div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import '@arcgis/core/assets/esri/themes/light/main.css'
import Map from '@arcgis/core/Map'
import MapView from '@arcgis/core/views/MapView'
import WebTileLayer from '@arcgis/core/layers/WebTileLayer'

import { useMapStore } from '@/store/mapStore'
import { useLayerStore } from '@/store/layerStore'

const mapDiv = ref(null)
const mapStore = useMapStore()
const layerStore = useLayerStore()

onMounted(() => {
  const tdLayer = new WebTileLayer({
    urlTemplate:
      'http://{subDomain}.tianditu.gov.cn/DataServer?T=vec_w&x={col}&y={row}&l={level}&tk=9aa49772a6d157afe863294b50b104a3',
    subDomains: ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7'],
    id: 'tdLayer',
    title: '天地图矢量',
    visible: true,
    opacity: 1
  })

  const tdLayer_POI = new WebTileLayer({
    urlTemplate:
      'http://{subDomain}.tianditu.gov.cn/DataServer?T=cva_w&x={col}&y={row}&l={level}&tk=9aa49772a6d157afe863294b50b104a3',
    subDomains: ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7'],
    id: 'tdPOI',
    title: '天地图注记',
    visible: true,
    opacity: 1
  })
  const map = new Map({
    layers: [tdLayer, tdLayer_POI]
  })

  const view = new MapView({
    container: mapDiv.value,
    map: map,
    center: [120.2, 30.3],
    zoom: 10
  })

  view.ui.remove('attribution')
  mapStore.setMapView(view)

  // 注册图层到 Pinia
  layerStore.addLayer({
    id: tdLayer.id,
    title: tdLayer.title,
    visible: tdLayer.visible,
    opacity: tdLayer.opacity,
    type: 'basemap',
    instance: tdLayer
  })

  layerStore.addLayer({
    id: tdLayer_POI.id,
    title: tdLayer_POI.title,
    visible: tdLayer_POI.visible,
    opacity: tdLayer_POI.opacity,
    type: 'basemap',
    instance: tdLayer_POI
  })

  // 使用 watch 响应式同步图层状态变化
  watch(
    () => layerStore.layers.map(l => ({ id: l.id, visible: l.visible, opacity: l.opacity })),
    (newList) => {
      for (const config of newList) {
        const layer = map.layers.find(l => l.id === config.id)
        if (layer) {
          layer.visible = config.visible
          layer.opacity = config.opacity
        }
      }
    },
    { deep: true }
    )  
  })
</script>


<style scoped>
.map-container {
  width: 100%;
  height: 100%;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0px 2px 1px -1px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.2)), 0px 1px 1px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.14)), 0px 1px 3px 0px var(--v-shadow-key-ambient-opacity, rgba(0, 0, 0, 0.12));
}
</style>
