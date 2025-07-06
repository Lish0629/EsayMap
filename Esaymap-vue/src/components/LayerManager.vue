<template>
  <v-card class="pa-4 rounded-xl layer-card" elevation="2">
    <h3 class="text-h6 mb-4">图层管理器</h3>

    <v-expansion-panels
      v-model="expanded"
      multiple
      elevation="0"
      variant="accordion"
    >
      <v-expansion-panel
        v-for="layer in layers"
        :key="layer.id"
      >
        <v-expansion-panel-title>
          <!-- 左侧：可视勾选框 -->
          <v-checkbox
            :model-value="layer.visible"
            @update:model-value="val => toggleVisibility(layer.id, val)"
            hide-details
            density="compact"
            class="mr-2"
          />
          <span class="font-weight-medium">{{ layer.title }}</span>
        </v-expansion-panel-title>

        <v-expansion-panel-text>
          <!-- 图层标题编辑 -->
          <v-text-field
            v-model="layer.title"
            label="图层名称"
            variant="outlined"
            density="compact"
            hide-details
            @change="updateTitle(layer.id, layer.title)"
          />

          <!-- 透明度控制 -->
          <v-slider
            v-model="layer.opacity"
            min="0"
            max="1"
            step="0.01"
            label="透明度"
            class="mt-4"
            @change="updateOpacity(layer.id, layer.opacity)"
          >
            <template #prepend>
              <span class="text-caption">透明度</span>
            </template>
          </v-slider>

          <!-- 栅格图层特殊设置（仅预留） -->
          <div v-if="layer.type === 'raster'" class="mt-2">
            <v-select
              label="渲染类型"
              :items="['continuous', 'discrete']"
              v-model="layer.renderType"
              @change="updateRenderType(layer.id, layer.renderType)"
              variant="outlined"
              density="compact"
              hide-details
            />
          </div>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-card>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useMapStore } from '@/store/mapStore'
import { ref } from 'vue'

const mapStore = useMapStore()
const { layers } = storeToRefs(mapStore)

const toggleVisibility = mapStore.toggleVisibility
const updateOpacity = mapStore.updateOpacity
const updateTitle = mapStore.updateTitle
const updateRenderType = mapStore.updateRenderType

const expanded = ref([]) // 控制每个图层展开状态
</script>

<style scoped>
.v-expansion-panel-title {
  align-items: center;
}
.layer-card{

  height: calc(100% - 8px);
  display: flex;
  flex-direction: column;
  border-radius: 20px;
  overflow: hidden;
  background-color: white;
  margin:6px -3px -2px 4px !important;

}
</style>
