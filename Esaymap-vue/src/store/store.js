import {defineStore} from 'pinia'

import {ref,shallowRef} from 'vue'

export const useMapStore = defineStore('mapStore', () => { 
 const mapView = shallowRef(null)

 const setMapView = (view) => {
   mapView.value = view
 }
 const map =shallowRef(null)
 const setMap = (map) => {
   map.value = map
 }
  return {mapView,setMapView,map,setMap}
})