<template>
  <!-- for PC -->
  <div id="app" v-if="PageType">
    <!-- <the-tool-bar /> -->
    <div class="editor-content" v-if="survey.currentPage === 'editor'">
      <the-panel-base :editorData="survey.editorData" />
      <the-work-space />
    </div>

    <div class="flow-content" v-if="survey.currentPage === 'flow'">
      <the-flow-editor />
      <div class="button-row bottom-row">
        <button-base class="secondary standard" :title="'Cancel'" />
        <button-base class="primary standard" :title="'Save'" />
      </div>
    </div>
  </div>
  <!-- for mobile -->
  <div id="app" v-else>
    <div id='testtt'></div>
    <!-- <the-tool-bar /> -->
    <div class="editor-content" v-if="survey.currentPage === 'editor'">
      <the-panel-base-m-b :editorData="survey.editorData" />
      <the-work-space />
    </div>

    <div class="flow-content" v-if="survey.currentPage === 'flow'">
      <the-flow-editor />
      <div class="button-row bottom-row">
        <the-panel-base-m-b :editorData="survey.editorData" />
        <button-base class="secondary standard" :title="'Cancel'" />
        <button-base class="primary standard" :title="'Save'" />
      </div>
    </div>
  </div>
</template>


<script>
import TheToolBar from '../components/SurveyBuilder/TheToolBar.vue'
import ThePanelBase from '../components/SurveyBuilder/ThePanelBase.vue'
import ThePanelBaseMB from '../components/SurveyBuilder/ThePanelBaseForMobile.vue'
import TheWorkSpace from '../components/SurveyBuilder/TheWorkSpace.vue'
import store from '../store/SurveyBuilder'
import TheFlowEditor from '../components/SurveyBuilder/TheFlowEditor.vue'
import ButtonBase from '../components/ButtonBase.vue'
import { relativeTimeRounding } from 'moment'

export default {
  name: 'SurveyBuilder',
  store: store,
  data() {
    return {
      // Page Type:PC/Mobile
      PageType: true,
      // Record the size of the screen
      screenWidth: null,
      // Flag for reload
      render: true
    }
  },
  watch: {},
  mounted() {
    // When initialization, get the screen width
    window.addEventListener('load', this.checkWidth)
    //If the window size hange, reload the page
    window.addEventListener('resize', this.checkWidth)
    window.addEventListener('resize', this.reload)
  },
  destroyed() {
    window.removeEventListener('resize', this.reload)
  },
  methods: {
    // Reload the page
    reload() {
      this.render = false
      this.$nextTick(() => {
        this.render = true
      })
    },
    // Check the screen width
    checkWidth() {
      this.screenWidth = document.body.clientWidth
      console.log("screenwidth:" + this.screenWidth)
      if (this.screenWidth < 766) {
        this.PageType = false;
      }
      else {
        this.PageType = true;
      }
    }
  },
  components: {
    TheToolBar,
    ThePanelBase,
    ThePanelBaseMB,
    TheWorkSpace,
    TheFlowEditor,
    ButtonBase,
  },
  data() {
    return {
      updatesocket: null,
      locksocket: null,
      wsdata: null,
      wsmark: 1,
      state: false
    };
  },
  computed: {
    survey() {
      return store.getters['wholeSurvey']
    },
    currentQuestionID() {
      return store.state.currentQuestionID
    },
  },

  created() {
    store.dispatch('loadSurvey', this.$route.params.id);
  },
  beforeMount() {
    //this.updatesocket = new WebSocket(`ws://127.0.0.1:8000/ws/test/${this.$route.params.id}/`);
    this.updatesocket = new WebSocket(`ws://111.231.14.233:8000/ws/test/${this.$route.params.id}/`);
    this.$store.dispatch('setLockSocket', new WebSocket(`ws://111.231.14.233:8000/ws/focus/`));
    //this.$store.dispatch('setLockSocket', new WebSocket(`ws://127.0.0.1:8000/ws/focus/`));
    this.updatesocket.onmessage = (event) => {
      const response = JSON.parse(event.data).survey_data
      // Formats data type so that it works with the current Vue code
      response.currentPage = 'editor'

      if (response.blocks == null) {
        response.blocks = []
      }

      for (var i = 0; i < response.blocks.length; i++) {
        // console.log('for循环的信息',response.blocks[i]);
        response.blocks[i] = {
          title: response.blocks[i].title,
          questionData: {
            currentQuestion: this.currentQuestionID,
            questions: response.blocks[i].questions,
          },
          ...response.blocks[i],
        }

        for (
          var k = 0;
          k < response.blocks[i].questionData.questions.length;
          k++
        ) {
          response.blocks[i].questionData.questions[k] = {
            ...response.blocks[i].questionData.questions[k].typedata,
            ...response.blocks[i].questionData.questions[k],
          }

          delete response.blocks[i].questionData.typedata
          response.blocks[i].questionData.questions[k].title =
            response.blocks[i].questionData.questions[k].name

          if (
            response.blocks[i].questionData.questions[k].type == 'Text entry'
          ) {
            response.blocks[i].questionData.questions[k].answerType = 'Text'
          }

          if (
            response.blocks[i].questionData.questions[k].type == 'Number entry'
          ) {
            response.blocks[i].questionData.questions[k].answerType = 'Integer'
          }

          if (
            response.blocks[i].questionData.questions[k].type == 'News post'
          ) {
            response.blocks[i].questionData.questions[k].articleImage =
              response.blocks[i].questionData.questions[k].articleImageLink
            response.blocks[i].questionData.questions[k].likeCount =
              response.blocks[i].questionData.questions[k].articleLikes
            response.blocks[i].questionData.questions[k].shareCount =
              response.blocks[i].questionData.questions[k].articleShares
            response.blocks[i].questionData.questions[k].commentCount =
              response.blocks[i].questionData.questions[k].articleComments
            response.blocks[i].questionData.questions[k].retweetCount =
              response.blocks[i].questionData.questions[k].articleRetweets
            response.blocks[i].questionData.questions[k].sendCount =
              response.blocks[i].questionData.questions[k].articleSends

          }

          if (
            response.blocks[i].questionData.questions[k].type ==
            'Multiple choice'
          ) {
            for (
              var y = 0;
              y < response.blocks[i].questionData.questions[k].choices.length;
              y++
            ) {
              response.blocks[i].questionData.questions[k].choices[y].text =
                response.blocks[i].questionData.questions[k].choices[y].title
              response.blocks[i].questionData.questions[k].choices.sort(
                (a, b) => (a.order - b.order ? 1 : b.order - a.order ? -1 : 0)
              )
            }
          }
          if (
            response.blocks[i].questionData.questions[k].type == 'Rank order'
          ) {
            for (
              var y = 0;
              y < response.blocks[i].questionData.questions[k].choices.length;
              y++
            ) {
              response.blocks[i].questionData.questions[k].choices[y].text =
                response.blocks[i].questionData.questions[k].choices[y].title
              response.blocks[i].questionData.questions[k].choices.sort(
                (a, b) => (a.order - b.order ? 1 : b.order - a.order ? -1 : 0)
              )
            }
          }

          if (
            response.blocks[i].questionData.questions[k].type == 'Number scale'
          ) {
            // console.log(response.blocks[i].questionData.questions[k])
            response.blocks[i].questionData.questions[k].minNum =
              response.blocks[i].questionData.questions[k].numberMin
            response.blocks[i].questionData.questions[k].maxNum =
              response.blocks[i].questionData.questions[k].numberMax
            response.blocks[i].questionData.questions[k].midTitle =
              response.blocks[i].questionData.questions[k].middleTitle
            response.blocks[i].questionData.questions[k].minTitleOn =
              response.blocks[i].questionData.questions[k].minTitleOn
            response.blocks[i].questionData.questions[k].maxTitleOn =
              response.blocks[i].questionData.questions[k].maxTitleOn
            response.blocks[i].questionData.questions[k].midTitleOn =
              response.blocks[i].questionData.questions[k].midTitleOn
            response.blocks[i].questionData.questions[k].interval =
              response.blocks[i].questionData.questions[k].interval

            if (response.blocks[i].questionData.questions[k].interval == 0) {
              response.blocks[i].questionData.questions[k].interval += 1
            }
          }

          if (
            response.blocks[i].questionData.questions[k].type == 'Button row'
          ) {
            // response.blocks[i].questionData.questions[k].goToEnd = false
            response.blocks[i].questionData.questions[k].terminating =
              response.blocks[i].questionData.questions[k].goToEnd
            for (
              var q = 0;
              q < response.blocks[i].questionData.questions[k].buttons.length;
              q++
            ) {
              response.blocks[i].questionData.questions[k].buttons[q].text =
                response.blocks[i].questionData.questions[k].buttons[
                  q
                ].buttonText
              // response.blocks[i].questionData.questions[k].buttons[q].goToEnd = false
              response.blocks[i].questionData.questions[k].buttons[
                q
              ].terminates =
                response.blocks[i].questionData.questions[k].buttons[q].goToEnd
              response.blocks[i].questionData.questions[k].buttons.sort(
                (a, b) => (a.order - b.order ? 1 : b.order - a.order ? -1 : 0)
              )
            }
          }
        }

        delete response.blocks[i].questions   //删除后端来的questions  因为已经放入questionData
        // console.log('for循环的信息结束',response.blocks[i]);
      }

      response.title = response.name
      response.flowData = {}
      response.settingsData = {}
      response.editorData = {
        flowView: this.wsmark == 1 ? this.state : this.survey.editorData.flowView,
        questionTypes: [
          'News post',
          'Multiple choice',
          'Text entry',
          'Number scale',
          'Button row',
          'Rank order',
          'Matrix table',
          'Sliders',
          'Groups',
          // "Matrix",
          // "Drag and Drop",
        ],
        questionIcons: [
          'fas fa-newspaper',
          'fas fa-dot-circle',
          'fas fa-pen',
          'fas fa-list-ol',
          'fas fa-grip-horizontal',
          "fas fa-th-list",
          "fa fa-table",
          "fa fa-sliders",
          "fa fa-columns",
        ],
        currentBlock: this.wsmark == 1 ? this.state : this.survey.editorData.currentBlock,
        blocks: response.blocks,
        randomSections: response.randomSections,
      }
      delete response.blocks
      if (this.wsmark == 1) {
        this.wsmark++
      }
      // console.log('刷新后的数据', response);
      store.dispatch('updateSurvey', response);
    };

  },
  beforeDestroy() {
    // 关闭WebSocket连接
    this.updatesocket.close();
    this.locksocket.close();
  },
}
</script>

<style scoped>
/* TODO: fix up rtl button styling */
html:lang(ur) * {
  text-align: right;
}

#app {
  font-family: Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  margin-top: 0px;
  width: 100%;
  /* height: calc(100vh - 112px); */
  overflow: hidden;
}

.editor-content {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  width: 100%;
  max-height: calc(100vh - 56px);
  min-height: calc(100vh - 56px);
  /* max-height: calc(100% - 112px); */
  overflow: hidden;
}

.button-row {
  display: flex;
  flex-direction: row;
  /* padding: 16px 0; */
  align-items: center;
}

.bottom-row {
  position: sticky;
  bottom: 0;
  left: 0;
  background-color: white;
  width: 100%;
  justify-content: flex-end;
  border-top: 1px solid #566370;
}
</style>
