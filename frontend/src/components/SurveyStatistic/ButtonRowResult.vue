<template>
  <div>
    <div class="question-box">
      <div class="word">
        <h1 class="questionNumber" v-model="index">
          Q{{ index + 1 }} {{ questionData.type }}
        </h1>
        <h2 class="questionName" v-model="questionData">
          {{ questionData.title }}
        </h2>
      </div>
      <div class="graph" id="chart">
        <apexchart
          type="bar"
          height="350"
          :options="chartOptions"
          :series="series"
        ></apexchart>
      </div>
    </div>
  </div>
</template>

<script>
import VueApexCharts from 'vue-apexcharts'

export default {
  name: 'ButtonRowResult',
  props: {
    question: Object,
    index: Number,
  },
  data() {
    return {
      questionData: '',
      number: 0,
      series: [
        {
          data: [],
        },
      ],
      chartOptions: {
        chart: {
          type: 'bar',
          height: 350,
        },
        plotOptions: {
          bar: {
            borderRadius: 4,
            horizontal: true,
            dataLabels: {
              position: 'top',
            },
          },
        },
        dataLabels: {
          enabled: true,
          offsetX: -6,
          style: {
            fontSize: '12px',
            colors: ['#fff'],
          },
        },
        xaxis: {
          categories: [],
        },
      },
    }
  },
  created() {
    this.number = this.index
    this.questionData = this.question

    function string2int(list) {
      console.log('list', list)
      let res = []
      for (let i = 0; i < list.length; i++) {
        res[i] = Number(list[i])
      }
      return res
    }

    this.chartOptions.xaxis.categories = this.question.x
    this.series[0].data = string2int(this.question.y)
  },
  // data() {
  //   return {
  //     questions: {
  //       "id": 4,
  //       "block": 2,
  //       "name": "Please answer these questions according to your own situation",
  //       "type": "Button row",
  //       "description": "",
  //       "order": 2,
  //       "count": 60,
  //       "choices": [
  //         {
  //           "id": 4,
  //           "question": 2,
  //           "order": 1,
  //           "title": "A",
  //           "number": 20,
  //           "percentage": 0.2
  //         },
  //         {
  //           "id": 5,
  //           "question": 2,
  //           "order": 2,
  //           "title": "B",
  //           "number": 80,
  //           "percentage": 0.8
  //         }
  //       ]
  //     },
  //     series: [{
  //       data: [3, 2, 5]
  //     }],
  //     chartOptions: {
  //       chart: {
  //         type: 'bar',
  //         height: 350
  //       },
  //       plotOptions: {
  //         bar: {
  //           borderRadius: 4,
  //           horizontal: true,
  //           dataLabels: {
  //             position: 'top',
  //           }
  //         }
  //       },
  //       dataLabels: {
  //         enabled: true,
  //         offsetX: -6,
  //         style: {
  //           fontSize: '12px',
  //           colors: ['#fff']
  //         }
  //       },
  //       xaxis: {
  //         categories: ['I do not know', 'I am a student', 'I am 16 years old'],
  //       }
  //     }
  //   }
  // }
}
</script>
<style>
.questionAVG {
  color: red;
  font-size: 20px;
  margin-left: 370px;
}

.question-box {
  width: 550px;
  border: 2px solid #eff2f5;
  border-radius: 4px;
  margin: 20px;
  padding: 8px;
}
</style>
