<template>
    <div class="px-6 col-span-2 pt-4 flex flex-col">
      <p class="mb-4">Hardware Performance</p>
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
        <div v-else class="text-center">No Indicators Yet. Run a LLM query.</div>
      </div>
    </div>

</template>

<script setup>
import { ref, onMounted, reactive, watch } from 'vue'
import { VuePlotly } from 'vue3-plotly'
import { useEvaluatorStore } from "../stores/evaluator";

const evaluatorStore = useEvaluatorStore();

const chart = ref()
const chartData = ref({
      data:[{
  x: [1, 2, 3, 4, 5, 6, 7, 8, 9],
  y: [10, 15, 18, 20, 25, 30, 35, 40, 45],
  type: 'scatter'
}],
      layout:{
        margin: {
    l: 20,  // left margin
    r: 20,  // right margin
    t: 20,  // top margin
    b: 20   // bottom margin
  }
      },
      config: {
          displayModeBar: false
      }
    })
const key = ref(0)
function increase() {
  chartData.value.data[0].x.push(chartData.value.data[0].x[chartData.value.data[0].x.length-1] + 1)
  chartData.value.data[0].y.push(chartData.value.data[0].y[chartData.value.data[0].y.length-1] + 5)
  key.value += 1
}

var trace1 = {
    x: [1, 2, 3, 4, 5, 6, 7, 8, 9],
    y: [10, 15, 18, 20, 25, 30, 35, 40, 45],
    type: 'scatter'
  };

  var layout = {
  margin: {
    l: 20,  // left margin
    r: 20,  // right margin
    t: 20,  // top margin
    b: 20   // bottom margin
  }
};

  
  var data = [trace1];


//   onMounted(() => {
//     Plotly.newPlot(chart.value, data, layout);
// })
  

</script>