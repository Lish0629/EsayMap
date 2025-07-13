<script setup>
import { useMapStore } from '@/store/mapStore'
defineProps({ layer: Object })

const mapStore = useMapStore()
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
    <v-select
      class="mt-2"
      label="渲染类型"
      :items="['连续型', '离散型']"
      v-model="layer.renderType"
      disabled
    />
    <small class="text-grey">* 暂未实现渲染逻辑</small>
  </div>
</template>
