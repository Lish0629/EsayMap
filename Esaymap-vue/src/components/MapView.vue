<template>
  <div class="map-container" ref="mapDiv">
    <img :src="logoImage" alt="EsayMap Logo" class="logo-image" />
  </div>
</template>

<script setup>
import { onMounted, ref, watch ,markRaw} from 'vue'

import '@arcgis/core/assets/esri/themes/light/main.css'
import Map from '@arcgis/core/Map'
import MapView from '@arcgis/core/views/MapView'
import WebTileLayer from '@arcgis/core/layers/WebTileLayer'

import { useMapStore } from '@/store/mapStore'
const mapDiv = ref(null)
const mapStore = useMapStore()
import logoImage from '@/assets/logo.png';
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
  //高德地图底图
  const gaodeLayer = new WebTileLayer({
    urlTemplate:
      'https://webrd03.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
    subDomains: ['1', '2', '3', '4'],
    id: 'gaodeLayer',
    title: '高德矢量底图',
    opacity: 1
  })
  mapStore.addLayer({
    id: gaodeLayer.id,
    title: gaodeLayer.title,
    visible: gaodeLayer.visible,
    opacity: gaodeLayer.opacity,
    type: 'basemap',
    instance: markRaw(gaodeLayer)
  })
  // mapStore.addLayer({
  //   id: tdLayer.id,
  //   title: tdLayer.title,
  //   visible: tdLayer.visible,
  //   opacity: tdLayer.opacity,
  //   type: 'basemap',
  //   instance: markRaw(tdLayer)
  // })

  // mapStore.addLayer({
  //   id: tdLayer_POI.id,
  //   title: tdLayer_POI.title,
  //   visible: tdLayer_POI.visible,
  //   opacity: tdLayer_POI.opacity,
  //   type: 'basemap',
  //   instance: markRaw(tdLayer_POI)
  // })

})



</script>


<style scoped>
.map-container {
  width: 100%;
  height: 100%;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0px 2px 1px -1px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.2)), 0px 1px 1px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.14)), 0px 1px 3px 0px var(--v-shadow-key-ambient-opacity, rgba(0, 0, 0, 0.12));
  position: relative;
}
.logo-image {
  height: 92px;
  width: auto;
  position: absolute;
  bottom: 0;  /* 距离包含块底部 0 像素 */
  right: 10px; 
}
</style>
