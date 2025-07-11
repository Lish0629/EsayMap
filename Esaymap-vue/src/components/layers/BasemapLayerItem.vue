<script setup>
import { useMapStore } from '@/store/mapStore'
const layerStore = useMapStore ()
defineProps({ layer: Object })
</script>

<template>
  <div class="pl-6 pr-2 pt-2">
    <v-text-field
      v-model="layer.title"
      label="底图名称"
      density="compact"
      @change="layerStore.updateTitle(layer.id, layer.title)"
    />
    <v-slider
      v-model="layer.opacity"
      min="0"
      max="1"
      step="0.01"
      label="透明度"
      class="mt-2"
      @change="layerStore.updateOpacity(layer.id, layer.opacity)"
    />
  </div>
</template>
