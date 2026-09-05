<script setup lang="ts">
import { VisualizationOptions } from '../model/VisualizationOptions'

const options = defineModel<VisualizationOptions>( {
  required: true
})
</script>

<template>
  <div class="visualization-controls">
    <h2>Settings</h2>
    <div>
      <label>
          Show as hierarchy
      </label>
      <input type="checkbox" v-model="options.showAsHierarchy" />
    </div>
    <div>
     <label>
        Data:
      </label>
      <select disabled v-model="options.dataSource">
        <option value="opt1">Breakdown of "leap"</option>
        <option value="opt2">Circular definition</option>
        <option value="opt3">Big graph</option>
      </select>
    </div>
  </div>
</template>

<style lang="css" scoped>
.visualization-controls {
  border: 1px solid #d1d5db;
  border-radius: 12px;
  padding: 8px;
}
</style>