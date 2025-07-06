import {defineStore} from 'pinia'

export const useMapStore = defineStore('mapStore',{
  state:()=>({
    mapView:null
  }),
  actions:{
    setMapView(view){
      this.mapView = view
    }
  }
})