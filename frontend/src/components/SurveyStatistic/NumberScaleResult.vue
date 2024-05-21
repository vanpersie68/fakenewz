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
        <p class="questionAVG" v-model="questionData.average">
          AVG: {{ questionData.average }}
        </p>
      </div>
      <div class="graph">
        <apexchart
          width="500"
          type="bar"
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
  name: 'NumberScaleResult',
  created() {
    this.number = this.index
    this.questionData = this.question

    function string2int(list) {
      let res = []
      for (let i = 0; i < list.length; i++) {
        res[i] = Number(list[i])
      }
      return res
    }

    this.chartOptions.xaxis.categories = this.question.x
    this.series[0].data = string2int(this.question.y)
  },
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
}
</script>
<style>
.questionType {
  float: left;
}
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
