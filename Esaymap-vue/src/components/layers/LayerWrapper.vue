<script setup>
import VectorLayerItem from './VectorLayerItem.vue'
import RasterLayerItem from './RasterLayerItem.vue'
import BasemapLayerItem from './BasemapLayerItem.vue'

defineProps({
  layer: Object
})
</script>

<template>
  <component
    :is="layer.type === 'vector' ? VectorLayerItem
         : layer.type === 'raster' ? RasterLayerItem
         : BasemapLayerItem"
    :layer="layer"
  />
</template>

<style>
.v-slider{
  width:90%;
}
</style>
