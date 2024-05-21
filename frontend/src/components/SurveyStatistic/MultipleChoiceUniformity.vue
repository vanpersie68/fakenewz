<template>
  <div class="mainBlock">
    <div class="question-box">
      <div class="word">
        <h2 class="questionName">{{ $t('surveyStatistic.uniformity') }}</h2>
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
  name: 'BrowserResult',
  props: {
    uniformity: Array,
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
  async created() {
    this.chartOptions.xaxis.categories = this.uniformity.map(
      (e) => `${e.qTitle}`
    )
    console.log(
      'this.chartOptions.xaxis.categories',
      this.uniformity.map((e) => `${e.blockTitle} ${e.qTitle}`)
    )
    this.series[0].data = this.uniformity.map((e) => e.uniformity)
    console.log(
      'this.series[0].data',
      this.uniformity.map((e) => e.uniformity * 100 + '%')
    )
  },
}
</script>
<style>
.question-box {
  width: 550px;
  border: 2px solid #eff2f5;
  border-radius: 4px;
  margin: 20px;
  padding: 8px;
}

.mainBlock {
  width: 610px;
  border: 2px solid #eff2f5;
  border-radius: 4px;
  margin: 20px 20px 20px 35%;
  padding: 8px;
}
</style>
