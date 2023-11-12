<template>
    <div class="px-6 col-span-2 pt-4 flex flex-col">
      <p class="mb-4 font-bold">Hardware Performance</p>
      <!-- <button @click="increase">Increase</button> -->
      <div class="bg-gray-light py-4 px-2 text-sm gap-y-4 rounded-xl flex flex-col justify-between h-full overflow-y-auto shadow-sm">
        <template v-if="evaluatorStore.performance[0].data[0].x.length > 4">
          <div v-for="(measure, perfKey) in evaluatorStore.performance" class="px-1 pt-3 pb-5 bg-gray-dark rounded-xl h-full">
          <p class="text-lg text-center font-semibold mb-3">{{measure.hw}}</p>
          <VuePlotly
              :data="measure.data"
              :layout="measure.layout"
              :config="measure.config"
              :key="`${key}-${perfKey}`"
              class="w-[80%] h-40 mx-auto"
          />
        </div>
        </template>
        <div v-else class="text-center">No indicators yet. Run some LLM queries.</div>
      </div>
    </div>

</template>

<script setup>
import { ref, onMounted, reactive, watch } from 'vue'
import { VuePlotly } from 'vue3-plotly'
import { useEvaluatorStore } from "../stores/evaluator";

const evaluatorStore = useEvaluatorStore();

const key = ref(0)

var trace1 = {
    x: [1, 2, 3, 4, 5, 6, 7, 8, 9],
    y: [10, 15, 18, 20, 25, 30, 35, 40, 45],
    type: 'scatter'
  };

</script>