<template>
  <div class="mainBlock">
    <div class="question-box">
      <div class="word">
        <h2 class="questionName">{{ $t('surveyStatistic.browserInfo') }}</h2>
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
    browser: Object,
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
    console.log('END')
    // setTimeout(() => {
    //   console.log("Hello World", this.browser)
    //   let val = JSON.parse(JSON.stringify( this.browser));
    //   console.log("val",val.x);
    //   this.chartOptions.xaxis.categories = val.x;
    //   this.series[0].data = val.y;
    // }, 100)
    // // console.log("Hello World!", this.browser)
    // let val = JSON.parse(JSON.stringify(this.browser));
    // // console.log("val", val.x);
    // this.chartOptions.xaxis.categories = val.x;
    // this.series[0].data = val.y;
    // this.questionData = this.browser;
    // function string2int(list) {
    //   console.log("list",list)
    //   let res = [];
    //   for (let i = 0; i < list.length; i++) {
    //     res[i] = list[i];
    //   }
    //   return res;
    // }
    this.chartOptions.xaxis.categories = this.browser.x
    console.log(
      'this.chartOptions.xaxis.categories',
      this.chartOptions.xaxis.categories
    )
    this.series[0].data = this.browser.y
    console.log('this.series[0].data', this.series[0].data)
    // this.$forceUpdate();
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
