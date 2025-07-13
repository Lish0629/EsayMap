<script setup>

defineProps({ layer: Object })
import { useMapStore } from '@/store/mapStore'
const mapStore = useMapStore ()
</script>

<template>
  <div class="pl-6 pr-2 pt-2">
    <v-text-field
      v-model="layer.title"
      label="图层名称"
      density="compact"
      @change="mapStore.updateTitle(layer.id, layer.title)"
    />
    <v-slider
      v-model="layer.opacity"
      min="0"
      max="1"
      step="0.01"
      label="透明度"
      class="mt-2"
      @change="mapStore.updateOpacity(layer.id, layer.opacity)"
    />
  </div>
</template>
