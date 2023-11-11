<template>
    <div class="px-6 col-span-2 flex flex-col pt-4 border-r-[1px] border-gray-200">
      <div>
        <button
          class="flex items-center text-center bg-gray-light px-10 py-1 rounded-xl font-bold mb-3"
        >
          Select LLM
        </button>
      </div>

      <p class="mb-3"><span class="font-medium">ChatGPT</span> loaded.</p>
      <div class="bg-gray-light grow flex flex-col px-3 rounded-xl justify-end py-3 min-h-[1px] shadow-sm">
        <div class="w-full h-full py-3 overflow-y-auto">
            <template v-for="message in evaluatorStore.messages">
                <div :class="['border-gray-300 border-[2px] flex items-center rounded-xl py-1.5 px-1', message.role == 'bot' ? 'mrl-5' : 'ml-5']">
                    {{ message.message }}
                </div>
                <span :class="['text-xs block mb-3 text-gray-dark', message.role == 'bot' ? 'text-left': 'text-right']">{{ message.role == 'bot' ? 'Bot' : 'User' }}</span>
            </template>
        </div>
        <div class="flex items-center">
            <input
                placeholder="Enter a prompt..."
                class="bg-gray-dark w-full h-8 rounded-xl px-2 text-sm font-semibold flex items-center place-self-end"
            />
            <div class="rounded-full cursor-pointer ml-2 p-1 flex items-center border-[1px] border-gray-dark hover:border-black">
                <PaperAirplaneIcon class="w-4 h-4"/>
            </div>
        </div>
      </div>
    </div>
</template>

<script setup>
import { PaperAirplaneIcon } from "@heroicons/vue/24/solid";
import { useEvaluatorStore } from "../stores/evaluator";

const evaluatorStore = useEvaluatorStore();
</script>