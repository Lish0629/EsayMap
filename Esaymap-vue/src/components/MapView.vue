<template>
  <div class="map-container" ref="mapDiv"></div>
</template>

<script setup>
import { onMounted, ref, watch ,markRaw} from 'vue'

import '@arcgis/core/assets/esri/themes/light/main.css'
import Map from '@arcgis/core/Map'
import MapView from '@arcgis/core/views/MapView'
import WebTileLayer from '@arcgis/core/layers/WebTileLayer'

import { useMapStore } from '@/store/mapStore'
import { arcgisToGeoJSON, geojsonToArcGIS } from '@esri/arcgis-to-geojson-utils'
const mapDiv = ref(null)
const mapStore = useMapStore()

onMounted(() => {


  //初始化map和mapview
  const map = new Map({
    //layers: [tdLayer, tdLayer_POI]
    //默认的初始图层，但addlayer功能正常，所以注释
  })

  const view = new MapView({
    container: mapDiv.value,
    map: map,
    center: [120.2, 30.3],
    zoom: 10
  })

  view.ui.remove('attribution')
  mapStore.setMapView(markRaw(view))
  
  //天地图底图
  const tdLayer = new WebTileLayer({
    urlTemplate:
      'http://{subDomain}.tianditu.gov.cn/DataServer?T=vec_w&x={col}&y={row}&l={level}&tk=9aa49772a6d157afe863294b50b104a3',
    subDomains: ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7'],
    id: 'tdLayer',
    title: '天地图矢量',
    visible: true,
    opacity: 1
  })
  //天地图注记
  const tdLayer_POI = new WebTileLayer({
    urlTemplate:
      'http://{subDomain}.tianditu.gov.cn/DataServer?T=cva_w&x={col}&y={row}&l={level}&tk=9aa49772a6d157afe863294b50b104a3',
    subDomains: ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7'],
    id: 'tdPOI',
    title: '天地图注记',
    visible: true,
    opacity: 1
  })

  mapStore.addLayer({
    id: tdLayer.id,
    title: tdLayer.title,
    visible: tdLayer.visible,
    opacity: tdLayer.opacity,
    type: 'basemap',
    instance: markRaw(tdLayer)
  })

  mapStore.addLayer({
    id: tdLayer_POI.id,
    title: tdLayer_POI.title,
    visible: tdLayer_POI.visible,
    opacity: tdLayer_POI.opacity,
    type: 'basemap',
    instance: markRaw(tdLayer_POI)
  })

  const arcgis = geojsonToArcGIS({
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "name": "测试点",
        "description": "这是一个用于测试的GeoJSON点"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [120.51959, 35.290270]
      }
    }
  ]
  })

  console.log(arcgis)

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
