import { ref, computed } from 'vue'
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

var cpua = 0
var mema = 0
var timea = 0
var rxa = 0
var txa = 0

const socket = new WebSocket('ws://localhost:3000');

socket.addEventListener('open', (event) => {
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

socket.addEventListener('hardware', (event) => {
  event.data.text().then((data) => {
    console.log(data)
    const compdata = JSON.parse(data);
    console.log('Received data:', compdata);

    if (cpu1 == 0) {
      cpu1 = compdata.total_cpu_usage
      mem1 = compdata.memory_usage
      time1 = compdata.read_time.split('T')[1].split('.')[1].split('Z')[0]
      rx1 = compdata.rx_bytes
      tx1 = compdata.tx_bytes
    }
    else if (cpu2 == 0) {
      cpu2 = compdata.total_cpu_usage
      mem2 = compdata.memory_usage
      time2 = compdata.read_time.split('T')[1].split('.')[1].split('Z')[0]
      rx2 = compdata.rx_bytes
      tx2 = compdata.tx_bytes
    }

    if (cpu1 != 0 && cpu2 != 0) {
      var cpu = cpu2 - cpu1
      var mem = mem2 - mem1
      var time = time2 - time1
      var rx = rx2 - rx1
      var tx = tx2 - tx1

      cpu1 = cpu2
      mem1 = mem2
      time1 = time2
      rx1 = rx2
      tx1 = tx2

      cpu2 = compdata.total_cpu_usage
      mem2 = compdata.memory_usage
      time2 = compdata.read_time.split('T')[1].split('.')[1] //.split('Z')[0]
      rx2 = compdata.rx_bytes
      tx2 = compdata.tx_bytes

      cpua.push(cpu.toFixed(2)) 
      mema.push(mem.toFixed(2))
      timea.push(time.toFixed(2))
      rxa.push(rx.toFixed(2))
      txa.push(tx.toFixed(2))

    }
  })
  // Handle the received data as needed
});

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


  const performance = ref([{
    data:[{
  x: mema,
  y: timea,
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
    },
    hw: "RAM"
  },
  {
    data:[{
  x: cpua,
  y: timea,
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
    },
    hw: "CPU"
  },
  {
    data:[{
  x: rxa,
  y: timea,
  type: 'scatter',
  name: 'Received',
  }, {
    x: txa,
    y: timea,
    type: 'scatter',
    name: 'Transmitted',
    }],
    layout:{
      margin: {
  l: 20,  // left margin
  r: 20,  // right margin
  t: 20,  // top margin
  b: 20   // bottom margin
  },
  legend: {
    x: 0.5,       // Set the x position of the legend (0 to 1)
    y: 1.05,      // Set the y position of the legend (0 to 1)
    xanchor: 'center', // Set the x anchor to center
    yanchor: 'bottom', // Set the y anchor to bottom
  },
    },
    config: {
        displayModeBar: false
    },
    hw: "Network"
  }])
  
  const count = ref(0)
  const doubleCount = computed(() => count.value * 2)
  function increment() {
    count.value++
  }

  return { performance, messages, analysis, count, doubleCount, increment }
})



