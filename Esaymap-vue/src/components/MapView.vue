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
const gjson=arcgisToGeoJSON(
  {
    "geometryType": "esriGeometryPoint",
    "geometries": [{"rings": [
    [
 [
  120.51962973500008,
  35.28953747700007
 ],
 [
  120.51955026500002,
  35.28953747700007
 ],
 [
  120.5194711050001,
  35.28954321000003
 ],
 [
  120.51939287500011,
  35.28955463200003
 ],
 [
  120.51931618800006,
  35.289571651000074
 ],
 [
  120.51924164500008,
  35.28959413700005
 ],
 [
  120.51916982700004,
  35.28962191200009
 ],
 [
  120.51910129800001,
  35.289654759000086
 ],
 [
  120.519036594,
  35.28969242100004
 ],
 [
  120.518976221,
  35.289734604000046
 ],
 [
  120.51892065100003,
  35.28978097700008
 ],
 [
  120.51887032100001,
  35.28983117700005
 ],
 [
  120.51882562200001,
  35.289884811000036
 ],
 [
  120.51878690600006,
  35.28994146000008
 ],
 [
  120.51875447500004,
  35.29000068000005
 ],
 [
  120.51872858400009,
  35.29006200800006
 ],
 [
  120.51870943400002,
  35.290124964000086
 ],
 [
  120.51869717500006,
  35.29018905500004
 ],
 [
  120.51869190500008,
  35.29025377900007
 ],
 [
  120.51869366300002,
  35.29031863000006
 ],
 [
  120.51870243600001,
  35.29038310100009
 ],
 [
  120.5187181550001,
  35.29044668600005
 ],
 [
  120.5187406980001,
  35.29050888900008
 ],
 [
  120.51876988800007,
  35.290569221000055
 ],
 [
  120.51880549600003,
  35.29062721200006
 ],
 [
  120.51884724400009,
  35.290682408000066
 ],
 [
  120.51889480600005,
  35.290734375000056
 ],
 [
  120.51894780800001,
  35.29078270800005
 ],
 [
  120.51900583600002,
  35.29082702900007
 ],
 [
  120.519068436,
  35.29086699000004
 ],
 [
  120.51913511700002,
  35.29090227800009
 ],
 [
  120.51920535900001,
  35.290932619000046
 ],
 [
  120.51927861200011,
  35.29095777300006
 ],
 [
  120.51935430100002,
  35.29097754500009
 ],
 [
  120.51943183500009,
  35.29099177900008
 ],
 [
  120.51951060700003,
  35.29100036400007
 ],
 [
  120.51959000000011,
  35.29100323400007
 ],
 [
  120.51966939300007,
  35.29100036400007
 ],
 [
  120.51974816500001,
  35.29099177900008
 ],
 [
  120.51982569900008,
  35.29097754500009
 ],
 [
  120.51990138800011,
  35.29095777300006
 ],
 [
  120.51997464100009,
  35.290932619000046
 ],
 [
  120.52004488300008,
  35.29090227800009
 ],
 [
  120.5201115640001,
  35.29086699000004
 ],
 [
  120.52017416400008,
  35.29082702900007
 ],
 [
  120.5202321920001,
  35.29078270800005
 ],
 [
  120.52028519400005,
  35.290734375000056
 ],
 [
  120.52033275600002,
  35.290682408000066
 ],
 [
  120.52037450400007,
  35.29062721200006
 ],
 [
  120.52041011200004,
  35.290569221000055
 ],
 [
  120.520439302,
  35.29050888900008
 ],
 [
  120.520461845,
  35.29044668600005
 ],
 [
  120.52047756400009,
  35.29038310100009
 ],
 [
  120.52048633700008,
  35.29031863000006
 ],
 [
  120.52048809500002,
  35.29025377900007
 ],
 [
  120.52048282500004,
  35.29018905500004
 ],
 [
  120.52047056600009,
  35.290124964000086
 ],
 [
  120.52045141600001,
  35.29006200800006
 ],
 [
  120.52042552500006,
  35.29000068000005
 ],
 [
  120.52039309400004,
  35.28994146000008
 ],
 [
  120.52035437800009,
  35.289884811000036
 ],
 [
  120.52030967900009,
  35.28983117700005
 ],
 [
  120.52025934900007,
  35.28978097700008
 ],
 [
  120.5202037790001,
  35.289734604000046
 ],
 [
  120.5201434060001,
  35.28969242100004
 ],
 [
  120.52007870200009,
  35.289654759000086
 ],
 [
  120.52001017300006,
  35.28962191200009
 ],
 [
  120.51993835500002,
  35.28959413700005
 ],
 [
  120.51986381200004,
  35.289571651000074
 ],
 [
  120.51978712500011,
  35.28955463200003
 ],
 [
  120.51970889500001,
  35.28954321000003
 ],
 [
  120.51962973500008,
  35.28953747700007
 ]
]]}]
}
);
console.log(arcgis)
console.log(gjson)
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
