<template>
    <div class="px-6 col-span-2 flex flex-col pt-4 border-r-[1px] border-gray-200">
      <div>
        <button
          class="flex items-center text-center bg-gray-light px-10 py-1 rounded-xl font-bold mb-3"
        >
          orca_mini_3B-GGML
        </button>
      </div>

      <p class="mb-3 font-bold">Prompts</p>
      <div class="bg-gray-light grow flex flex-col px-3 rounded-xl justify-end py-3 min-h-[1px] shadow-sm">
        <div v-if="evaluatorStore.messages.length == 0" class="text-center h-full text-sm">No promts yet. Input some!</div>
        <div v-else class="w-full h-full py-3 overflow-y-auto">
            <template v-for="message in evaluatorStore.messages">
                <div :class="['border-gray-300 border-[2px] flex items-center rounded-xl py-1.5 px-1 fadeIn', message.role == 'bot' ? 'mrl-5' : 'ml-5']" v-html="message.message"></div>
                <span :class="['text-xs block mb-3 text-gray-dark fadeIn', message.role == 'bot' ? 'text-left': 'text-right']">{{ message.role == 'bot' ? 'Bot' : 'User' }}</span>
            </template>

            <div v-if="evaluatorStore.waitingForAnswer" class="border-gray-300 border-[2px] items-center gap-x-1 rounded-xl py-1.5 px-1 inline-flex fadeIn delay-500">
              <span class="w-2 h-2 rounded-full bg-gray-500 animate-pulse"></span>
              <span class="w-2 h-2 rounded-full bg-gray-500 animate-pulse delay-150"></span>
              <span class="w-2 h-2 rounded-full bg-gray-500 animate-pulse delay-300"></span>
            </div>
        </div>
        <div class="flex items-center">
            <input
                v-model="message"
                placeholder="Enter a prompt..."
                class="bg-gray-dark w-full h-8 rounded-xl px-2 text-sm font-semibold flex items-center place-self-end"
            />
            <div 
              :disabled="evaluatorStore.waitingForAnswer"
              class="rounded-full cursor-pointer ml-2 p-1 flex items-center border-[1px] border-gray-dark hover:border-black transition-opacity	" 
              @click="() => {
                  if (message == '') return
                  evaluatorStore.addMessage(message, 'user')
                  evaluatorStore.waitForAnswer()
                  message = ''
                }"
              >
                <PaperAirplaneIcon class="w-4 h-4"/>
            </div>
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref } from "vue";
import { PaperAirplaneIcon } from "@heroicons/vue/24/solid";
import { useEvaluatorStore } from "../stores/evaluator";

const evaluatorStore = useEvaluatorStore();
const message = ref("");
</script>

<style scoped>
@keyframes fadein {
    from { opacity: 0; }
    to   { opacity: 1; }
}

.fadeIn {
    -webkit-animation: fadein 0.4s; /* Safari, Chrome and Opera > 12.1 */
       -moz-animation: fadein 0.4s; /* Firefox < 16 */
        -ms-animation: fadein 0.4s; /* Internet Explorer */
         -o-animation: fadein 0.4s; /* Opera < 12.1 */
            animation: fadein 0.4s;
}
</style>
