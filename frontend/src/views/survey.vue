<template>
  <div>
    <div>
      <button class="statistic-btn" v-on:click="getStatisticView()">
        Back
      </button>
      <div class="mainBlock">
        <div class="Block">
          <h2 class="timeName">{{ $t('surveyStatistic.timeInfo') }}</h2>
          <div
            class="metadata-display"
            style="margin-left: 13.5%; margin-bottom: 2%"
          >
            <h3>{{ $t('surveyStatistic.minTime') }}</h3>
            <span class="metadata-figure">{{
              statistic.timeData.minTime
            }}</span>
          </div>
          <div class="metadata-display">
            <h3>{{ $t('surveyStatistic.midTime') }}</h3>
            <span class="metadata-figure">{{
              statistic.timeData.midTime
            }}</span>
          </div>
          <div class="metadata-display">
            <h3>{{ $t('surveyStatistic.maxTime') }}</h3>
            <span class="metadata-figure">{{
              statistic.timeData.maxTime
            }}</span>
          </div>
          <div class="metadata-display">
            <h3>{{ $t('surveyStatistic.averageTime') }}</h3>
            <span class="metadata-figure">{{
              statistic.timeData.averageTime
            }}</span>
          </div>
        </div>
      </div>
      <div v-if="statisticView === true" class="block-segment">
        <BrowserResult :browser="this.statistic.browserData" />
      </div>
      <MultipleChoiceUniformity :uniformity="this.uniformity" />
      <div
        class="block-segment"
        v-for="(block, index) in this.statistic.blocks"
      >
        <Results :block="block" :index="index" />
      </div>
    </div>
  </div>
</template>

<script>
import SubmissionBarChart from '../components/SubmissionBarChart.vue'
import Results from '../components/SurveyStatistic/Results'
import MultipleChoiceUniformity from '../components/SurveyStatistic/MultipleChoiceUniformity'
import BrowserResult from '../components/SurveyStatistic/BrowserResult'

export default {
  data: function () {
    return {
      statisticView: false,
      survey: {},
      statistic: {},
      // uniformity:{}
    }
  },
  created() {
    this.statisticView = false
  },
  methods: {
    getStatisticView() {
      this.$router.push('/My_Survey')
    },

    getResponseExportUrl(id) {
      return this.$axios.defaults.baseURL + 'survey/response/' + id + '/'
    },
    getConfigurationExportUrl(id) {
      return this.$axios.defaults.baseURL + 'survey/export/' + id + '/'
    },
  },
  beforeMount() {
    this.$axios
      .get('api/surveys/' + this.$route.params.id)
      .then((res) => {
        this.survey = res.data
      })
      .catch((reason) => {
        this.$router.replace({ name: 'index' })
      })

    this.$axios
      .get('api/st/survey/result/0/' + this.$route.params.id)
      .then((res) => {
        this.statistic = res.data
        this.statisticView = true
        console.log('Start')
      })
      .catch((reason) => {
        this.$axios
          .get('api/st/survey/result/1/' + this.$route.params.id)
          .then((res) => {
            this.statistic = res.data
            this.statisticView = true
            console.log('Start')
          })
          .catch((reason) => {
            this.$router.replace({ name: 'index' })
          })
      })
  },
  computed: {
    uniformity() {
      const arr = []
      this.statistic.blocks.forEach((b) => {
        b.questions &&
          b.questions.forEach((q) => {
            if (!q.choices) return
            const choArr = Object.values(q.choices)
            arr.push({
              blockTitle: b.title,
              blockId: b.id,
              qTitle: q.title,
              uniformity:
                Math.max(...choArr) /
                choArr.reduce((pre, cur, idx) => pre + cur),
            })
          })
      })

      console.log(arr)
      return arr
    },
  },
  components: {
    BrowserResult,
    Results,
    SubmissionBarChart,
    MultipleChoiceUniformity,
  },
}
</script>

<style scoped>
.timeName {
  margin-top: 4%;
  margin-left: 10%;
  margin-bottom: 8%;
}

.Block {
  border: 2px solid #eff2f5;
  border-radius: 4px;
  margin: 20px 20px 20px 20px;
  padding: 8px;
}

h1 {
  font-weight: 300;
}

#page {
  padding: 20px;
}

.metadata-display {
}

h3 {
  font-weight: 300;
  margin: 0;
  font-size: 20px;
}

h2 {
  margin: 0;
}

.action-btn {
  border: 1px solid black;
  padding: 5px 10px;
  color: black;
  font-size: 15px;
  border-radius: 5px;
  text-decoration: none;
  margin: 2px 10px 2px 0px;
  display: inline-block;
}

.metadata-figure {
  font-size: 40px;
  font-weight: 300;
}

.metadata-display {
  border: 1px solid #000;
  border-radius: 5px;
  display: inline-block;
  padding: 20px;
  margin-right: 30px;
  text-align: center;
  width: 21%;
  margin-left: 13.5%;
  margin-bottom: 2%;
}

.metadata-display-average {
  border: 1px solid #000;
  border-radius: 5px;
  display: inline-block;
  padding: 20px;
  margin-right: 30px;
  width: 21%;
  margin-left: 13.5%;
  margin-bottom: 2%;
}

.mainBlock h2 {
  font-weight: bold;
}

.statistic-btn {
  background-color: white;
  border: 1px solid black;
  padding: 5px 10px;
  color: black;
  font-size: 15px;
  border-radius: 5px;
  text-decoration: none;
  margin: 10px;
  display: inline-block;
}

.mainBlock {
  width: 610px;
  border: 2px solid #eff2f5;
  border-radius: 4px;
  margin: 20px 20px 20px 35%;
  padding: 8px;
}
</style>
