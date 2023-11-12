import { ref, computed, reactive } from 'vue'
import { defineStore } from 'pinia'

var rec = {
  "total_cpu_usage": 53276100,
  "memory_usage": 10760192,
  "read_time": "2023-11-11T23:09:01.278449",
  "rx_bytes": 5159,
  "tx_bytes": 3394
}

var judge = ''

var cpu1 = 0
var mem1 = 0
var time1 = 0
var rx1 = 0
var tx1 = 0

var cpu2 = 0
var mem2 = 0
var time2 = 0
var rx2 = 0
var tx2 = 0

var cpua = []
var mema = []
var timea = []
var rxa = []
var txa = []

const socket = new WebSocket('ws://localhost:3000');

socket.addEventListener('answer', (event) => {
  useEvaluatorStore().justInputted = false
  useEvaluatorStore().waitingForAnswer = false
  useEvaluatorStore().addMessage(event.data, 'bot')
});

socket.addEventListener('message', (event) => {
  console.log('WebSocket connection opened:', event);
  sendData(rec);
});

socket.addEventListener('analysis', (event) => {
  event.data.text().then((data) => {
    console.log(data)
    judge = JSON.parse(data);
    console.log('Received data:', judge);
    analysis.value.push({
      typeOf: 'Faithfulness',
      content: judge.faithfulness
    }, {
      typeOf: 'Answer Relevancy',
      content: judge.answer_relevancy
    }, {
      typeOf: 'Context Precision',
      content: judge.context_precision
    }, {
      typeOf: 'Context Recall',
      content: judge.context_recall
    }, {
      typeOf: 'Harmfulness',
      content: judge.harmfulness
    })
  })
})

function sendData(data) {
  // Ensure the socket is open before sending
  if (socket.readyState === WebSocket.OPEN) {
    const jsonData = JSON.stringify(data);
    socket.send(jsonData);
    console.log('Sent data:', jsonData);
  } else {
    console.error('WebSocket not open. Unable to send data.');
  }
}

export const useEvaluatorStore = defineStore('evaluator', () => {
  const waitingForAnswer = ref(false)
  const justInputted = ref(false)
  const messages = ref([])
  // const messages = ref([{
  //   'role': 'user',
  //   'message': 'Hi!',
  // },{
  //   'role': 'bot',
  //   'message': 'Hi there, I\'m a bot. I\'m here to help you evaluate your performance.',
  // }, {
  //   'role': 'user',
  //   'message': 'Tell me a joke!',
  // },{
  //   'role': 'bot',
  //   'message': 'What did one snowman say to the other? \n Do you smell carrots?',
  // }])
  const analysis = ref([{
    typeOf: 'Faithfulness',
    content: ''
  }, {
    typeOf: 'Answer Relevancy',
    content: ''
  }, {
    typeOf: 'Context Precision',
    content: ''
  }, {
    typeOf: 'Context Recall',
    content: ''
  }, {
    typeOf: 'Harmfulness',
    content: ''
  }])



  const all_performance = reactive({
    "total_cpu_usage": [],
    "memory_usage": [],
    "read_time": [],
    "rx_bytes": [],
    "tx_bytes": []
  })


  socket.addEventListener('hardware', (event) => {
    event.data.text().then((data) => {
      console.log(data)
      const compdata = JSON.parse(data);
      console.log('Received data:', compdata);

      all_performance.total_cpu_usage.push(compdata.total_cpu_usage)
      all_performance.memory_usage.push(compdata.memory_usage)
      all_performance.read_time.push(new Date(compdata.read_time))
      all_performance.rx_bytes.push(compdata.rx_bytes)
      all_performance.tx_bytes.push(compdata.tx_bytes)
    })

  });

  const performance = computed(() => {

    const layout = {
      margin: {
        l: 20,  // left margin
        r: 20,  // right margin
        t: 20,  // top margin
        b: 20   // bottom margin
      },
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: 'rgba(0,0,0,0)',
      width: 300,
      height: 160,
      xanchor: 'center', // Set the x anchor to center
      yanchor: 'bottom', // Set the y anchor to bottom
    }

    const config = {
      displayModeBar: false
    }

    const deltas = (arr) => {
      return arr.map((x, i) => {
        if (i == 0) {
          return null
        }
        return x - arr[i - 1]
      }).filter(x => x != null)
    }

    const res = [{
      data: [{
        x: all_performance.read_time,
        y: deltas(all_performance.memory_usage),
        type: 'scatter'
      }],
      layout,
      config,
      hw: "RAM"
    },
    {
      data: [{
        x: all_performance.read_time,
        y: deltas(all_performance.total_cpu_usage),
        type: 'scatter'
      }],
      layout,
      config,
      hw: "CPU"
    },
    {
      data: [{
        x: all_performance.read_time,
        y: deltas(all_performance.rx_bytes),
        type: 'scatter',
        name: 'Received',
      }, {
        x: all_performance.read_time,
        y: deltas(all_performance.tx_bytes),
        type: 'scatter',
        name: 'Transmitted',
      }],
      layout: {
        ...layout,
        legend: {
          x: 0.5,       // Set the x position of the legend (0 to 1)
          y: 1.05,      // Set the y position of the legend (0 to 1)

        },
      },
      config,
      hw: "Network"
    }]
    console.log(res)
    return res
  })



  function addMessage(messageContent, role) {
    messages.value.push({
      role: role,
      message: messageContent,
    })
  }

  function waitForAnswer() {
    justInputted.value = true

    setTimeout(() => {
      if (justInputted.value) {
        waitingForAnswer.value = true
        justInputted.value = false
      }
    })
  }


  return { performance, messages, analysis, waitingForAnswer, addMessage, waitForAnswer }
})



