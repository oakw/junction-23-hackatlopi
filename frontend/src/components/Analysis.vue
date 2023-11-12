<template>
    <div class="px-6 col-span-3 flex pt-4 flex-col h-full justify-end border-r-[1px] border-gray-200">
      <p class="mb-4 font-bold">Truthfulness Rating</p>
      <div class="bg-gray-light h-full py-4 px-2 text-sm flex flex-col gap-y-4 rounded-xl overflow-y-auto shadow-sm">
        <template v-if="evaluator.analysis[0].content != ''" >
          <div v-for="judgement in evaluator.analysis" class="px-2 py-3 bg-gray-dark rounded-xl h-24">
            <b>{{ judgement.typeOf }}.</b> {{ judgement.content }} 
        </div>
        </template>
        <div v-else class="text-center">No analysis yet. Run some LLM queries.</div>
      </div>
    </div>
</template>

<script setup>
import { useEvaluatorStore } from '../stores/evaluator';


const evaluator = useEvaluatorStore();
</script>