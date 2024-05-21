<template>
  <div class="chart-wrapper">
    <canvas id="chart"></canvas>
  </div>
</template>

<script>
import Chart from 'chart.js/auto'
import 'chartjs-adapter-date-fns'
import moment from 'moment'

export default {
  name: 'SubmissionBarChart',
  data: function () {
    return {
      labels: [],
      data: [],
      config: {
        type: 'bar',
        data: {
          datasets: [
            {
              label: 'Number of Response Submissions',
              data: [],
              backgroundColor: 'rgba(54,73,93,.5)',
              borderColor: '#36495d',
              borderWidth: 3,
            },
          ],
        },
        options: {
          lineTension: 1,
          scales: {
            x: {
              type: 'time',
              time: {
                unit: 'day',
              },
            },
          },
        },
      },
    }
  },
  mounted() {
    const res_per_day = new Map()
    this.$axios
      .get('survey/response_day/' + this.$route.params.id + '/')
      .then((res) => {
        for (var el of res.data) {
          var local_time = moment(el[1])
            .tz(moment.tz.guess())
            .format('YYYY-MM-DD')
          if (!this.labels.includes(local_time)) {
            this.labels.push(local_time)
            res_per_day.set(local_time, 0)
          }
          res_per_day.set(local_time, res_per_day.get(local_time) + 1)
        }
        for (const el of this.labels) {
          const point = { x: el, y: res_per_day.get(el) }
          this.data.push(point)
        }
        // this.config.data.labels = this.labels;
        this.config.data.datasets[0].data = this.data
        const ctx = document.getElementById('chart')
        Chart.defaults.font.family = 'sans-serif'
        let chart = new Chart(ctx, this.config)
      })
  },
}
</script>
<style scoped>
.chart-wrapper {
  width: 50vw;
  min-width: 900px;
  padding: 50px;
}
</style>
