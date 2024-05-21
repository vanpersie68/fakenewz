<template>
  <body>
  <div>
    <!-- Red points to calibrate -->
    <div class='calibrationDiv'>
      <input
        type='button'
        class='Calibration'
        :id='CalibrationPoints[currentCalibrationIndex]'
        v-show='showCalibration'
        @click='calibrate'
        :value='clickTimes'
      />
    </div>
    <!-- Dialog before start to calibrate -->
    <el-dialog
      :title="$t('gaze.calibration')"
      :visible.sync='calibrationDialog'
      width='350px'
      :before-close='startCalibration'
      :center='true'
    >
      <!-- Video Dialog -->
      <div id='dialogVideoDiv'>
        <p style='word-wrap: break-word; word-break: normal'>
          {{ $t('gaze.helpInfo') }}
        </p>
      </div>
      <!-- Button to start calibration -->
      <span slot='footer' class='dialog-footer'>
          <el-button type='primary' @click='startCalibration'>{{
              $t('gaze.start')
            }}</el-button>
        </span>
    </el-dialog>
    <!-- Dialog to show privacy and get user's camera permission -->
    <el-dialog
      :title="$t('gaze.privacyTitle')"
      :visible.sync='showPrivacyNotice'
      width='350px'
      :before-close='startCalibration'
      :center='true'
    >
      <div>
        <p
          style='word-wrap: break-word; word-break: normal'
          v-html="$t('gaze.privacyInfo')"
        ></p>
      </div>
      <span slot='footer' class='dialog-footer'>
          <el-button type='primary' @click='endSurvey'>{{
              $t('gaze.cancel')
            }}</el-button>
          <el-button type='primary' @click='openCalibrationDialog'>{{
              $t('gaze.agree')
            }}</el-button>
        </span>
    </el-dialog>
  </div>
  <!-- End of the calibration -->
  <div v-show='showQuestion'>
    <div class='survey-title'>
      <h1>
        {{ surveyTitle }}
      </h1>
      <div class='countDown' v-if='this.duration !== -1 && submitFlag'>
        <countdown :time='this.duration' @progress='handleCountdownProgress'>
          <template slot-scope='props'
          >{{
              $t('surveyTaker.Time Remaining: ') +
              props.hours +
              $t('surveyTaker.hours') +
              props.minutes +
              $t('surveyTaker.minutes') +
              props.seconds +
              $t('surveyTaker.seconds')
            }}
          </template>
        </countdown>
      </div>
    </div>
    <div class='block-segment' v-for='(block, index) in sortedBlocks'>
      <Block
        :block='block'
        :index='index'
        v-show='currentId === block.id'
        @updateBlock='updateBlock'
        @updateJumpBlockId='updateJumpBlockId'
        @randomQuestions='randomQuestions'
        :ref="'block' + index"
        :currentId='currentId'
        :uuid='answer.uuid'
      />
      <div class='end-of-survey' v-show='currentId === block.id'>
        <el-button-group>
          <el-button
            type='primary'
            @click='previousQuestion(index)'
            :disabled='preDisable'
            class='button-size'
            style='margin-right: 50px'
          >
            <i class='el-icon--left el-icon-arrow-left'></i>
            {{ $t('surveyTaker.Back') }}
          </el-button>
          <el-button
            type='primary'
            @click='nextQuestion(index)'
            :disabled='nextDisable'
            class='button-size'
          >
            {{ $t('surveyTaker.Next') }}
            <i class='el-icon-arrow-right el-icon--right'></i
            ></el-button>
        </el-button-group>
      </div>
      <div
        class='submit-button'
        v-show='
            currentId === block.id && currentIndex === showIdOrder.length - 1
          '
      >
        <el-button type='success' @click='submit' class='button-size'>{{
            $t('surveyTaker.Submit')
          }}
        </el-button>
      </div>
    </div>
  </div>
  <!-- <div class="test-button-1">
    <el-button class="button-size"></el-button>
  </div> -->
  </body>
</template>

<script>
import Block from '@/components/SurveyTaker/Block'
import store from '../../store/SurveyBuilder'
import SurveyServices from '../../services/SurveyServices'
import { mapGetters } from 'vuex'
import Cookies from 'js-cookie'

import webgazer from 'webgazer'

export default {
  name: 'SurveyTaker',
  store: store,
  components: { Block },
  computed: {
    ...mapGetters(['surveyTitle', 'sortedBlocks', 'wholeSurvey'])
  },
  data() {
    return {
      userAction: [],
      answer: {
        uuid: this.generateUuId(),
        respondent_identifier: '',
        survey_id: 0,
        researcher: 0,
        create_datatime: '',
        end_datatime: '',
        contact_info: '',
        response_blocks: [],
        completion_rate: '',
        camera_state: false,
        screen_size: {
          width: 0,
          height: 0
        },
        calibration_acc: 0,
        questionsOrder: []
      },
      createTime: '',
      duration: -1,
      ifDuration: false,
      blockIndex: 0,
      currentIndex: 0,
      currentId: 0,
      idOrder: [],
      showIdOrder: [],
      preDisable: true,
      showQuestion: true,
      nextDisable: false,
      previousDisable: false,
      randomSections: [],
      pushPosition: [],
      jumpBlockId: 0,
      showIndex: [],
      currentShowIndex: 0,
      submitFlag: true,
      // web gaze related
      showPrivacyNotice: false,
      calibrationDialog: false,
      showCalibration: false,
      calibrated: false,
      currentCalibrationIndex: 0,
      clickTimes: 5,
      CalibrationPoints: [
        'Pt1',
        'Pt2',
        'Pt3',
        'Pt4',
        'Pt5',
        'Pt6',
        'Pt7',
        'Pt8',
        'Pt9'
      ],
      gazeData: [],
      checkReadyInterval: null,
      gazeInterval: null,
      startRecord: false,
      clickEvent: [],
      touchEvent: [],
      check: false,
      if_agree_answer: false,
      if_camera_open: false,
      avgAccuracy: 0,
      accuracies: []
    }
  },
  mounted() {
    document.addEventListener('visibilitychange', this.handleVisiable)
    // window.addEventListener('beforeunload', e => this.beforeunloadHandler(e),false)
    // window.addEventListener('unload', e => this.unloadHandler(e))
    window.addEventListener('offline', () => {
      this.handleCloseCookie()
    })
    history.pushState(null, null, document.URL)
    window.addEventListener('popstate', this.goBack, false)
    window.addEventListener('click', this.handleClick)
    window.addEventListener('touchstart', this.handleTouch)
  },
  destroyed() {
    document.removeEventListener('visibilitychange', this.handleVisiable)
    clearInterval(this.gazeInterval)
    if (webgazer.isReady()) {
      webgazer.end()
    }
    window.removeEventListener('click', this.handleClick)
    window.removeEventListener('touchstart', this.handleTouch)
    // window.removeEventListener('beforeunload', e => this.beforeunloadHandler(e), false)
    // window.removeEventListener('unload',  e => this.unloadHandler(e))
    window.removeEventListener('offline', () => {
      this.handleCloseCookie()
    })
    window.removeEventListener('popstate', this.goBack, false)
  },

  methods: {
    handleCountdownProgress(data) {
      // console.log(data.totalSeconds)
      sessionStorage.setItem(`${this.wholeSurvey.id}`, data.totalSeconds * 1000)
      if (data.totalSeconds === 59) {
        this.$message({
          message:
            'You only have 1 minute to answer the question, then it will automatically submit',
          type: 'warning'
        })
      }
      if (data.totalSeconds === 300) {
        this.$message({
          message:
            'You only have 5 minutes to answer the question, then it will automatically submit',
          type: 'warning'
        })
      }
      if (data.totalSeconds === 1) {
        setTimeout(() => {
          // console.log('END')
          this.forceSubmit()
        }, 1000)
      }
    },

    generateUuId() {
      // console.log('11111111111111')
      console.log(sessionStorage.getItem(this.$route.params.code + 'Uuid'))
      if (sessionStorage.getItem(this.$route.params.code + 'Uuid') === null) {
        let uuid = this.randomString()
        // console.log('22222222222222222')
        sessionStorage.setItem(this.$route.params.code + 'Uuid', uuid)
        return uuid
      } else {
        // console.log('33333333333333')
        return sessionStorage.getItem(this.$route.params.code + 'Uuid')
      }
    },

    handleCloseCookie() {
      Cookies.set(this.$route.params.code + 'Success', true)
      sessionStorage.removeItem(this.$route.params.code + 'Uuid')
    },

    goBack() {
      sessionStorage.clear()
      window.history.back()
      history.pushState(null, null, document.URL)
      this.handleCloseCookie()
    },
    // beforeunloadHandler(e){
    //   this._beforeUnload_time=new Date().getTime();
    // },
    // unloadHandler(e) {
    //   this._gap_time = new Date().getTime() - this._beforeUnload_time;
    //   if (this._gap_time <= 5) {
    //     this.handleCloseCookie()
    //   }
    // },
    handleVisiable() {
      if (document.visibilityState === 'visible') {
        this.userAction.push({ time: new Date(), action: 'get focus' })
      } else {
        this.userAction.push({ time: new Date(), action: 'lose focus' })
      }
    },
    handleTouch(touch) {
      const clientX = touch.touches[0].clientX
      const clientY = touch.touches[0].clientY
      const target = touch.touches[0].target
      this.touchEvent.push({
        clientX,
        clientY,
        target,
        time: new Date(),
        scrollTop: document.documentElement.scrollTop,
        scrollLeft: document.documentElement.scrollLeft
      })
    },
    // Click event to calibrate
    async handleClick(click) {
      // console.log('click: ' + JSON.stringify(this.clickEvent))
      // console.log('touch: ' + JSON.stringify(this.touchEvent))
      let clickX = click.clientX
      let clickY = click.clientY
      let gazeX = 0
      let gazeY = 0
      let accuracy = 0
      try {
        let gazePosition = await webgazer.getCurrentPrediction()
        if (gazePosition) {
          gazeX = gazePosition.x
          gazeY = gazePosition.y
          accuracy = this.calculateAccuracy(clickX, clickY, gazeX, gazeY)
        }
      } catch (error) {
      }
      this.accuracies.push(accuracy)
      if (this.showQuestion) {
        this.clickEvent.push({
          clientX: clickX,
          clientY: clickY,
          Accuracy: accuracy,
          time: new Date(),
          scrollTop: document.documentElement.scrollTop,
          scrollLeft: document.documentElement.scrollLeft
        })
      }
    },
    updateBlock(data, index) {
      this.answer.response_blocks[index] = data
    },
    updateJumpBlockId(id) {
      this.jumpBlockId = id
    },
    randomQuestions(questions) {
      const order = questions.map((question) => {
        return question.originalOrder
      })

      this.answer.questionsOrder.push(order)
    },
    computeCompletionRate() {
      let completion = this.currentIndex / this.showIdOrder.length
      let percent = Number(completion * 100).toFixed(2)
      percent += '%'
      this.answer.completion_rate = percent
    },
    async submit() {
      const h = this.$createElement
      this.$confirm('', {
        message: h('div', null, [
          h('i', { class: 'el-icon-question' }),
          h('span', { class: 'hint-title' }, this.$t('surveyTaker.Hint')),
          h(
            'p',
            { class: 'hint-content' },
            this.$t(
              'surveyTaker.This action will submit the survey, do you want to continue?'
            )
          )
        ]),
        confirmButtonText: this.$t('surveyTaker.Confirm'),
        cancelButtonText: this.$t('surveyTaker.Cancel'),
        closeOnClickModal: false,
        closeOnPressEscape: false
      })
        .then(async () => {
          this.answer.completion_rate = '100%'
          await this.submitResponse()
          if (this.check) {
            this.handleCloseCookie()
            this.$message({
              message: this.$t('surveyTaker.Submit successfully'),
              type: 'success'
            })
            await this.$router.push(`/success`)
            console.log('Submit answer: ' + this.answer)
          }
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: this.$t('surveyTaker.Submission cancelled')
          })
        })
    },
    async submitResponse() {
      this.answer.survey_id = this.wholeSurvey.id
      this.answer.researcher = this.wholeSurvey.researcher
      this.answer.create_datatime = this.createTime
      this.answer.end_datatime = new Date()
      this.answer.user_agent = navigator.userAgent
      this.answer.user_action = JSON.stringify(this.userAction)
      this.answer.preview = !this.submitFlag
      this.answer.screen_size.height = window.screen.height
      this.answer.screen_size.width = window.screen.width
      this.answer.calibration_acc = this.avgAccuracy
      this.setGazeToCurrentBlock()
      this.setClickToCurrentBlock()
      if (
        !this.checkValidity(this.wholeSurvey.editorData.blocks.length - 1) &&
        !(this.jumpBlockId === -1)
      ) {
        this.check = false
        this.$message.error(
          this.$t('surveyTaker.The information you filled in is not correct')
        )
      } else {
        this.check = true
        if (Cookies.get(this.$route.params.code + 'id') === undefined) {
          this.answer.respondent_identifier = this.randomString()
          Cookies.set(
            this.$route.params.code + 'id',
            this.answer.respondent_identifier
          )
        } else {
          this.answer.respondent_identifier = Cookies.get(
            this.$route.params.code + 'id',
            this.answer.respondent_identifier
          )
        }
        let message = await SurveyServices.publishSurveyAnswer(this.answer)
      }
    },

    async forceSubmit() {
      await this.forceSubmitPre()
      this.$message({
        message: 'Submit successfully',
        type: 'success'
      })
      Cookies.set(this.$route.params.code + 'Success', true)
      this.$router.push(`/success`)
    },

    async forceSubmitPre() {
      this.answer.survey_id = this.wholeSurvey.id
      this.answer.researcher = this.wholeSurvey.researcher
      this.answer.create_datatime = this.createTime
      this.answer.end_datatime = new Date()
      this.answer.user_agent = navigator.userAgent
      this.answer.user_action = JSON.stringify(this.userAction)
      this.answer.preview = !this.submitFlag
      this.answer.screen_size.height = window.screen.height
      this.answer.screen_size.width = window.screen.width
      this.answer.calibration_acc = this.avgAccuracy

      if (Cookies.get(this.$route.params.code + 'id') === undefined) {
        this.answer.respondent_identifier = this.randomString()
        Cookies.set(
          this.$route.params.code + 'id',
          this.answer.respondent_identifier
        )
      } else {
        this.answer.respondent_identifier = Cookies.get(
          this.$route.params.code + 'id',
          this.answer.respondent_identifier
        )
      }
      // let message = await SurveyServices.publishSurveyAnswer(this.answer)
    },

    pushIdOrder() {
      // console.log('Sorted Blocks: ' + JSON.stringify(this.sortedBlocks))
      for (let i = 0; i < this.sortedBlocks.length; i++) {
        this.idOrder.push(this.sortedBlocks[i].id)
      }
    },
    checkValidity(i) {
      if (!this.$refs['block' + i][0].checkValidity()) {
        return false
      }
      return true
    },
    previousQuestion(index) {
      this.setGazeToCurrentBlock()
      this.setClickToCurrentBlock()
      this.showIndex.splice(this.currentShowIndex + 1)
      if (index > 0) {
        this.currentIndex = index - 1
        this.currentShowIndex--
        this.showIndex.push(this.currentIndex)
        this.nextDisable = false
      }
      if (this.currentIndex === 0) {
        this.preDisable = true
        this.computeCompletionRate()
        this.forceSubmitPre()
      }
      this.currentId = this.showIdOrder[this.showIndex[this.currentShowIndex]]
    },
    setGazeToCurrentBlock() {
      this.answer.response_blocks[this.currentIndex].gazeData = JSON.stringify(
        this.gazeData
      )
      this.gazeData = []
    },
    setClickToCurrentBlock() {
      this.answer.response_blocks[this.currentIndex].clickEvent =
        JSON.stringify(this.clickEvent)
      this.clickEvent = []
    },
    setTouchToCurrentBlock() {
      this.answer.response_blocks[this.currentIndex].touchEvent =
        JSON.stringify(this.touchEvent)
      this.touchEvent = []
    },
    nextQuestion(index) {
      this.setGazeToCurrentBlock()
      this.setClickToCurrentBlock()
      this.showIndex.splice(this.currentShowIndex + 1)
      if (this.checkValidity(index)) {
        if (this.jumpBlockId === 0) this.currentIndex++
        else if (this.jumpBlockId === -1) {
          this.submit()
        } else {
          for (let i = 0; i < this.showIdOrder.length; i++) {
            if (this.showIdOrder[i] === this.jumpBlockId) {
              this.currentIndex = i
              this.jumpBlockId = 0
            }
          }
        }
        this.currentShowIndex++
        this.showIndex.push(this.currentIndex)
        this.preDisable = false
        if (this.currentIndex === this.showIdOrder.length - 1)
          this.nextDisable = true
        this.computeCompletionRate()
        this.forceSubmitPre()
      } else {
        this.$message.error(
          this.$t('surveyTaker.The information you filled in is not correct')
        )
      }
      this.currentId = this.showIdOrder[this.showIndex[this.currentShowIndex]]
    },
    checkNextDisable() {
      if (this.showIdOrder.length === 1) {
        this.nextDisable = true
      }
    },
    checkNormalBlock() {
      this.randomSections = this.wholeSurvey.editorData.randomSections
      if (this.randomSections.length !== 0) {
        let start = 0
        let end = this.randomSections[0].startWith
        for (let i = 0; i < this.randomSections.length; i++) {
          end = this.randomSections[i].startWith
          for (let j = start; j < end - 1; j++) {
            this.showIdOrder.push(this.idOrder[j])
          }
          this.pushPosition.push(this.showIdOrder.length)
          start = this.randomSections[i].endWith
        }
        for (
          let i = this.randomSections[this.randomSections.length - 1].endWith;
          i < this.idOrder.length;
          i++
        ) {
          this.showIdOrder.push(this.idOrder[i])
        }
        // console.log(this.showIdOrder)
      } else {
        this.showIdOrder = this.idOrder
      }
    },
    checkRandomSections() {
      for (let i = 0; i < this.randomSections.length; i++) {
        this.handleSingleRandomSection(this.randomSections[i], i)
      }
    },
    handleSingleRandomSection(randomSection, i) {
      let display = randomSection.display
      let startWith = randomSection.startWith
      let endWith = randomSection.endWith
      let idNum = []
      for (let i = 0; i < endWith - startWith + 1; i++) {
        idNum.push(this.idOrder[startWith - 1 + i])
      }
      while (display > 0) {
        let rand = Math.floor(Math.random() * idNum.length)
        let data = idNum[rand]
        idNum.splice(rand, 1)
        this.showIdOrder.splice(this.pushPosition[i], 0, data)
        for (let i = 0; i < this.pushPosition.length; i++) {
          this.pushPosition[i]++
        }
        display--
      }
    },
    randomString() {
      let str = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
      let result = ''
      for (let i = 10; i > 0; --i)
        result += str[Math.floor(Math.random() * str.length)]
      return result
    },
    // web gaze related
    endSurvey() {
      if (!this.if_agree_answer) {
        this.$message({
          message:
            'Since this survey requires the camera to be turned on, you have been forced to submit',
          type: 'warning'
        })
        this.$router.push(`/success`)
      } else {
        this.showPrivacyNotice = false
        this.showQuestion = true
      }
    },
    // After the user click agree
    async openCalibrationDialog() {
      this.showPrivacyNotice = false
      await webgazer
        .setRegression('ridge') /* currently must set regression and tracker */
        .saveDataAcrossSessions(true)
        .begin()
      webgazer.clearData()
      webgazer.showVideoPreview(true)
      webgazer.showPredictionPoints(true)
      webgazer.showFaceOverlay(true)
      webgazer.applyKalmanFilter(true)
      this.calibrationDialog = true
      // Every 100ms, check if webgazer is ready
      this.checkReadyInterval = setInterval(this.checkWebGazerReady, 100)
      let that = this
      navigator.getUserMedia(
        { video: true },
        function onSuccess(stream) {
          that.if_camera_open = true
        },
        function onError(error) {
          // console.log('onError')
          if (!that.if_agree_answer) {
            that.$message({
              message:
                'Since this survey requires the camera to be turned on, you have been forced to submit',
              type: 'warning'
            })
            that.$router.push(`/success`)
          } else {
            that.calibrationDialog = false
            that.calibrated = true
            that.showQuestion = true
            that.answer.camera_state = true
            that.showCalibration = false
            webgazer.showPredictionPoints(false)
            that.gazeInterval = setInterval(that.recordGaze, 1000)
            window.addEventListener('click', that.handleClick)
            window.addEventListener('touchstart', that.handleTouch)
          }
        }
      )
    },
    checkWebGazerReady() {
      // Show the video preview if webgazer is ready
      if (webgazer.isReady()) {
        let dialogVideoDiv = document.getElementById('dialogVideoDiv')
        let videoPreview = document.getElementById('webgazerVideoContainer')
        let webgazerVideoFeed = document.getElementById('webgazerVideoFeed')
        webgazerVideoFeed.playsInline = true
        let webgazerFaceOverlay = document.getElementById('webgazerFaceOverlay')
        let feedBox = document.getElementById('webgazerFaceFeedbackBox')
        clearInterval(this.checkReadyInterval)
        dialogVideoDiv.appendChild(videoPreview)
        videoPreview.style.cssText =
          'display: flex; justify-content: center; height:250px'
        webgazerVideoFeed.style.cssText =
          'position: absolute; width: 320px; height: 240px; display: block; transform: scale(-1, 1);'
        webgazerFaceOverlay.style.cssText =
          'display: block; position: absolute; transform: scale(-1, 1); width: 320px; height: 240px;'
        feedBox.style.cssText =
          'display: block; border: solid green; position: absolute; bottom: 150px; width: 158.4px; height: 158.4px;'
      }
    },
    calibrate() {
      this.clickTimes--
      if (this.clickTimes <= 0) {
        this.clickTimes = 5
        this.currentCalibrationIndex++
      }
      // Finish calibration after clicking 9 points
      if (this.currentCalibrationIndex >= this.CalibrationPoints.length) {
        this.calibrated = true
        this.showQuestion = true
        this.answer.camera_state = true
        this.showCalibration = false
        webgazer.showPredictionPoints(false)
        // TODO: Show calibration accuracy
        this.avgAccuracy = this.calculateAvgAccuracy(this.accuracies)
        window.alert(`Your calibration accuracy is ${this.avgAccuracy}%`)
        // Gaze data every second while user is taking the survey
        this.gazeInterval = setInterval(this.recordGaze, 1000)
      }
    },
    calculateAvgAccuracy(accuracies) {
      let sumOfAccuracies = 0
      for (let i = 0; i < accuracies.length; i++) {
        sumOfAccuracies += accuracies[i]
      }

      return Math.round(sumOfAccuracies / accuracies.length)
    },
    calculateAccuracy(x, y, gazeX, gazeY) {
      let xDiff = x - gazeX
      let yDiff = y - gazeY
      let distance = Math.sqrt(xDiff * xDiff + yDiff * yDiff)
      let threshold = y / 2

      let accuracy = 0
      if (distance <= threshold && distance > -1) {
        accuracy = 100 - (distance / threshold) * 100
      } else if (distance > threshold) {
        accuracy = 0
      } else if (distance > -1) {
        accuracy = 100
      }

      return accuracy
    },
    // After the user click start
    startCalibration() {
      if (this.if_camera_open) {
        // Hide video preview and start calibration
        webgazer.showVideoPreview(false)
        this.calibrationDialog = false
        this.showCalibration = true
      } else {
        this.$message({
          message: 'You must first select camera permission',
          type: 'warning'
        })
      }
    },
    async recordGaze() {
      try {
        let position = await webgazer.getCurrentPrediction()
        if (position) {
          this.gazeData.push({
            gazeX: position.x,
            gazeY: position.y,
            // Error: Math.sqrt(
            //   Math.pow(position.x - 70, 2) + Math.pow(position.y - 70, 2)
            // ),
            time: new Date(),
            scrollTop: document.documentElement.scrollTop,
            scrollLeft: document.documentElement.scrollLeft
          })
        }
      } catch (error) {
      }
    }
  },
  async created() {
    if (this.$route.params.code != null) {
      let result = await SurveyServices.getSurveyQuestions(
        this.$route.params.code
      )
      await store.dispatch('loadSurvey', result)
      let val = await SurveyServices.getSurveyData(result)
      this.if_agree_answer = val.camera
      this.duration = val.duration
      if (sessionStorage.getItem(`${val.id}`)) {
        this.duration = Number(sessionStorage.getItem(`${val.id}`))
      }
      if (this.duration === -1) {
        this.ifDuration = true
      }

      if (
        !this.wholeSurvey.is_repeat_answer &&
        Cookies.get(this.$route.params.code + 'Success')
      ) {
        this.$message({
          message: 'You have already submitted the survey',
          type: 'success'
        })
        this.$router.push(`/success`)
      }
      this.submitFlag = true
      let cookieOrder = Cookies.get(this.$route.params.code + 'showIdOrder')
      // console.log('Check normal block: ' + JSON.stringify(this.randomSections))
      // console.log('Block id: ' + cookieOrder) // 130,131
      // console.log('Whole survey: ' + JSON.stringify(this.wholeSurvey))
      // console.log('Sorted blocks: ' + JSON.stringify(this.sortedBlocks))
      if (cookieOrder === undefined) {
        this.pushIdOrder()
        this.checkNormalBlock()
        this.checkRandomSections()
        setTimeout(() => {
          Cookies.set(this.$route.params.code + 'showIdOrder', this.showIdOrder)
        }, 800)
        // console.log('Set cookieOrder: ' + this.showIdOrder)
      } else {
        let stringOrder = cookieOrder.split(',')
        for (let i = 0; i < stringOrder.length; i++) {
          this.showIdOrder.push(Number(stringOrder[i])) // [130, 131]
        }
      }
    } else {
      await store.dispatch('loadSurvey', this.$route.params.id)
      this.submitFlag = false
      this.pushIdOrder()
      this.checkNormalBlock()
      this.checkRandomSections()
      // console.log(this.showIdOrder)
    }
    this.createTime = new Date()
    this.checkNextDisable()

    this.currentId = this.showIdOrder[this.currentIndex]
    this.showIndex.push(this.currentIndex)

    if (this.$store.state.survey.if_capture_gaze === true) {
      this.showPrivacyNotice = true
      this.showQuestion = false
    } else {
      window.addEventListener('click', this.handleClick)
    }
    this.computeCompletionRate()
    if (this.$route.params.code != null) {
      // console.log(this.answer)
      await this.forceSubmitPre()
    }
  }
}
</script>

<style scoped>
.countDown {
  /*margin-left: 40%;*/
  text-align: center;
}

.block-segment {
  display: flex;
  flex-direction: column;
  justify-content: center;
  max-width: 816px;
  min-width: 200px;
  margin: 0 auto;
}

.hint-title {
  margin-left: 10px;
  font-size: 16px;
  line-height: 30px;
  font-weight: 600;
  vertical-align: top;
}

.hint-content {
  margin-left: 10px;
  margin-top: 10px;
  font-size: 15px;
}

.el-icon-question {
  color: #f90;
  font-size: 30px;
}

@media (min-width: 1130px) {
  .survey-title {
    margin-top: 80px;
    margin-bottom: 80px;
  }

  h1 {
    margin: 1em 0 0.5em 0;
    font-weight: 100;
    text-transform: uppercase;
    color: black;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 58px;
    line-height: 54px;
    text-shadow: 2px 5px 0 rgba(0, 0, 0, 0.2);
    text-align: center;
  }

  .end-of-survey {
    text-align: center;
    color: #7f7f7f;
    margin-top: 50px;
    margin-bottom: 30px;
  }

  .submit-button {
    text-align: center;
    margin-bottom: 50px;
  }
}

@media (max-width: 1129px) and (min-width: 890px) {
  .survey-title {
    margin-top: 60px;
    margin-bottom: 60px;
  }

  h1 {
    margin: 1em 0 0.5em 0;
    font-weight: 100;
    text-transform: uppercase;
    color: black;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 50px;
    line-height: 54px;
    text-shadow: 2px 5px 0 rgba(0, 0, 0, 0.2);
    text-align: center;
  }

  .end-of-survey {
    text-align: center;
    color: #7f7f7f;
    margin-top: 35px;
    margin-bottom: 25px;
  }

  .submit-button {
    text-align: center;
    margin-bottom: 35px;
  }
}

@media (max-width: 889px) {
  .survey-title {
    margin-top: 40px;
    margin-bottom: 30px;
  }

  h1 {
    margin: 1em 0 0.5em 0;
    font-weight: 100;
    text-transform: uppercase;
    color: black;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 40px;
    line-height: 54px;
    text-shadow: 2px 5px 0 rgba(0, 0, 0, 0.2);
    text-align: center;
  }

  .end-of-survey {
    text-align: center;
    color: #7f7f7f;
    margin-top: 20px;
    margin-bottom: 20px;
  }

  .button-size {
    font-size: 14px;
    text-align: center;
  }

  .submit-button {
    text-align: center;
    margin-bottom: 20px;
  }

  .hint-title {
    margin-left: 5px;
    font-size: 8px;
    line-height: 15px;
    font-weight: 600;
    vertical-align: top;
  }

  .hint-content {
    margin-left: 5px;
    margin-top: 5px;
    font-size: 8px;
  }

  .el-icon-question {
    color: #f90;
    font-size: 15px;
  }
}

.Calibration {
  width: 30px;
  height: 30px;
  -webkit-border-radius: 25px;
  -moz-border-radius: 25px;
  border-radius: 25px;
  background-color: red;
  border-color: black;
  border-style: solid;
  position: fixed;
}

#Pt1 {
  top: 70px;
  left: 2vw;
}

#Pt2 {
  top: 70px;
  left: 50vw;
}

#Pt3 {
  top: 70px;
  right: 2vw;
}

#Pt4 {
  top: 50vh;
  left: 2vw;
}

#Pt5 {
  top: 50vh;
  left: 50vw;
}

#Pt6 {
  top: 50vh;
  right: 2vw;
}

#Pt7 {
  bottom: 8vw;
  left: 2vw;
}

#Pt8 {
  bottom: 8vw;
  left: 50vw;
}

#Pt9 {
  bottom: 8vw;
  right: 2vw;
}

.test-button-1 {
  position: absolute;
  top: 70px;
  left: 2vw;
}
</style>

<style>
@media (max-width: 450px) {
  .el-message-box {
    top: 60%;
    width: 90%;
  }
}
</style>
