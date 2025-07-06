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

  mapStore.setMapView(view) // 注册到全局
})
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 100%;
  border-radius: 16px;
  overflow: hidden;
}
</style>
