<script setup>
import { useMapStore } from '@/store/mapStore'
const mapStore = useMapStore()
defineProps({ layer: Object })

</script>

<template>
  <div class="pl-6 pr-2 pt-2">
    <v-text-field
      v-model="layer.title"
      label="底图名称"
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
      @update:modelValue="mapStore.updateOpacity(layer.id,$event)"
    />
  </div>
</template>
