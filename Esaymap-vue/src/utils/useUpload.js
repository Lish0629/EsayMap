// src/composables/useUpload.js
import shp from 'shpjs'
import Papa from 'papaparse'
import GeoJSONLayer from '@arcgis/core/layers/GeoJSONLayer'
import CSVLayer from '@arcgis/core/layers/CSVLayer'

import { useMapStore } from '@/store/mapStore'
import { markRaw } from 'vue'
export function useUpload() {
  const layerStore = useMapStore()
  function handleFileUpload(file) {
    const name = file.name.toLowerCase()

    if (name.endsWith('.geojson')) {
      const url = URL.createObjectURL(file)
      console.log(url)
      const layer = new GeoJSONLayer({ url, title: file.name, visible: true })
      layerStore.addLayer({
        id: file.name,
        title: file.name,
        visible: true,
        opacity: 1,
        type: 'vector',
        instance: markRaw(layer)
      })
      } else if (name.endsWith('.zip')) {
      const reader = new FileReader()
      reader.onload = async e => {
        const buffer = e.target.result
        const geojson = await shp(buffer)
        const blob = new Blob([JSON.stringify(geojson)], { type: 'application/json' })
        const url = URL.createObjectURL(blob)
        const layer = new GeoJSONLayer({ url, title: file.name, visible: true })
        layerStore.addLayer({
          id: file.name,
          title: file.name,
          visible: true,
          opacity: 1,
          type: 'vector',
          instance: markRaw(layer)
        })
      }
      reader.readAsArrayBuffer(file)
    } else if (name.endsWith('.csv')) {
      const url = URL.createObjectURL(file)
      const layer = new CSVLayer({
        url,
        title: file.name,
        latitudeField: 'lat',
        longitudeField: 'lon',
        visible: true
      })
      layerStore.addLayer({
        id: file.name,
        title: file.name,
        visible: true,
        opacity: 1,
        type: 'vector',
        instance: markRaw(layer)
      })
    } else {
      alert('仅支持 .geojson / .zip / .csv 文件')
    }
  }
  return { handleFileUpload }
}
