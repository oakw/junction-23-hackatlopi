import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useEvaluatorStore = defineStore('evaluator', () => {
  const messages = ref([{
    'role': 'user',
    'message': 'Hi!',
  },{
    'role': 'bot',
    'message': 'Hi there, I\'m a bot. I\'m here to help you evaluate your performance.',
  }, {
    'role': 'user',
    'message': 'Tell me a joke!',
  },{
    'role': 'bot',
    'message': 'What did one snowman say to the other? \n Do you smell carrots?',
  }])
  const analysis = ref([{
    typeOf: 'Faithfulness',
    content: 'Short comment and a rating.'
  }, {
    typeOf: 'Answer Relevancy',
    content: 'Short comment and a rating.'
  }, {
    typeOf: 'Context Precision',
    content: 'Short comment and a rating.'
  }, {
    typeOf: 'Context Recall',
    content: 'Short comment and a rating.'
  }, {
    typeOf: 'Harmfulness',
    content: 'Short comment and a rating.'
  }])
  
  const count = ref(0)
  const doubleCount = computed(() => count.value * 2)
  function increment() {
    count.value++
  }

  return { messages, analysis, count, doubleCount, increment }
})
