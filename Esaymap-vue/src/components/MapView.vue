<!-- src/components/MapView.vue -->
<template>
  <div class="map-container" ref="mapDiv"></div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import Map from '@arcgis/core/Map'
import MapView from '@arcgis/core/views/MapView'
import { useMapStore } from '@/store/mapStore'

import '@arcgis/core/assets/esri/themes/light/main.css'

const mapDiv = ref(null)
const mapStore = useMapStore()

onMounted(() => {
  const map = new Map({
    basemap: 'topo-vector'
  })

  const view = new MapView({
    container: mapDiv.value,
    map: map,
    center: [120.2, 30.3],
    zoom: 10
  })
  view.ui.remove('attribution')
  mapStore.setMapView(view) // 注册到全局
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
