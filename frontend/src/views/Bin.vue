<template>
  <div class="main">
    <h1>{{ $t('g5.ms-bin') }}</h1>
    <a @click="goBack" class="action-btn">{{ $t('g5.ms-back') }}</a>
    <a @click="batchRecover" class="action-btn">{{ $t('g5.ms-recover') }}</a>
    <input
      type="file"
      id="file-btn"
      style="visibility: hidden"
      v-on:change="handleFileUpload()"
      accept="application/json"
    />
    <br /><br />
    <table id="survey-table">
      <!-- Survey dashboard -->
      <div class="language"></div>

      <tr>
        <th>
          <el-link :underline="false">
            {{ $t('home.card3Info1') }}
            <i class="el-icon-arrow-down"></i>
          </el-link>
        </th>
        <th v-if="ifTitleOrder">
          <el-link
            :underline="false"
            @click="changeTitleOrder"
            :type="types[2]"
          >
            {{ $t('g5.ms-title') }}
            <i class="el-icon-arrow-down"></i>
          </el-link>
        </th>
        <th v-if="!ifTitleOrder">
          <el-link
            :underline="false"
            @click="changeTitleOrder"
            :type="types[3]"
          >
            {{ $t('g5.ms-title') }}
            <i class="el-icon-arrow-up"></i>
          </el-link>
        </th>
        <th>{{ $t('g5.Survey Language') }}</th>
        <th v-if="ifTimeOrder">
          <el-link :underline="false" @click="changeTimeOrder" :type="types[0]">
            {{ $t('g5.Create time') }}
            <i class="el-icon-arrow-down"></i>
          </el-link>
        </th>
        <th v-if="!ifTimeOrder">
          <el-link :underline="false" @click="changeTimeOrder" :type="types[1]">
            {{ $t('g5.Create time') }}
            <i class="el-icon-arrow-up"></i>
          </el-link>
        </th>
        <th>{{ $t('g5.Expire time') }}</th>
        <th>{{ $t('g5.Time remaining') }}</th>
        <th>{{ $t('g5.Respondents') }}</th>
        <th>{{ $t('g5.Survey Status') }}</th>
        <th>{{ $t('g5.ms-action') }}</th>
      </tr>
      <tr v-for="survey in showSurveys" :key="survey.id">
        <td>
          <el-checkbox
            v-model="survey.checked"
            @change="changeStatus"
          ></el-checkbox>
        </td>
        <td>{{ survey.name }}</td>
        <td>{{ survey.language }}</td>
        <td>{{ computeTime(survey.create_time) }}</td>
        <td>{{ computeExpireTime(survey.expire_time, survey.status) }}</td>
        <td>{{ computeRemainingTime(survey.expire_time, survey.status) }}</td>
        <td>
          {{
            computeRespondents(
              survey.current_submission,
              survey.required_submission,
              survey.status
            )
          }}
        </td>
        <td>
          <span v-if="survey.status === 0"
            ><i class="fas fa-circle" style="color: #1947e5"></i> Saved
          </span>
          <span v-if="survey.status === 1"
            ><i class="fas fa-circle" style="color: #18e200"></i> Published
          </span>
          <span v-if="survey.status === 2"
            ><i class="fas fa-circle" style="color: grey"></i> Finished
          </span>
        </td>
        <td style="padding-right: 0">
          <!--          <a class="action-btn-edit" @click="editSurvey(survey.id)" v-if="survey.status === 0">{{ $t("g5.ms-edit") }}</a>-->
          <!--          <a class="action-btn" v-if="survey.status === 1" @click="showlinkDialogVisible(survey.code)">{{ $t("g5.Share") }}</a>-->
          <!--          <a class="action-btn" v-if="survey.status === 2">{{ $t("g5.Share") }}</a>-->
          <!--          <a @click="getStatUrl(survey.id)" class="action-btn">{{ $t("g5.ms-view-stats") }}</a>-->
          <!--          <a @click="getResponseExportUrl(survey.id)" class="action-btn">{{ $t("g5.Export") }}</a>-->
          <!--          <a :href="getConfigurationExportUrl(survey.id)" class="action-btn">{{ $t("g5.ms-export-conf") }}</a>-->
          <a class="action-btn" @click="deleteSurvey(survey.id, survey.name)">{{
            $t('g5.Delete')
          }}</a>
          <a class="action-btn" @click="recoverSurvey(survey.id)">{{
            $t('g5.ms-recover')
          }}</a>
          <!--          <a class="action-btn-publish" @click="publishSurvey(survey.id)" v-if="survey.status === 0">{{ $t("g5.Publish") }}</a>-->
          <!--          <a class="action-btn-end" @click="endSurvey(survey.id)" v-else-if="survey.status === 1">{{ $t("g5.End Survey") }}</a>-->
          <!--          <a class="action-btn-mute" v-if="survey.status === 2">{{ $t("g5.Finished") }}</a>-->
        </td>
        <el-dialog
          :title="DialogTitle"
          :visible.sync="publishDialogVisible1"
          :append-to-body="true"
          width="30%"
          center
        >
          <el-form ref="form" label-width="20px" class="form-side">
            <el-form-item>
              <el-row>
                <el-col :span="20">
                  Please set the deadline of this survey
                </el-col>
                <el-col :span="4">
                  <el-switch v-model="ifTime"></el-switch>
                </el-col>
              </el-row>
              <el-row>
                <el-col :span="2"><i class="el-icon-time"></i></el-col>
                <el-col :span="3">
                  <el-input v-model="days" @change="showExpireTime"></el-input>
                </el-col>
                <el-col :span="2" :offset="1">days</el-col>
                <el-col :span="3" :offset="1">
                  <el-input v-model="hours" @change="showExpireTime"></el-input>
                </el-col>
                <el-col :span="2" :offset="1">hours</el-col>
                <el-col :span="3" :offset="1">
                  <el-input
                    v-model="minutes"
                    @change="showExpireTime"
                  ></el-input>
                </el-col>
                <el-col :span="2" :offset="1">mins</el-col>
              </el-row>
              <el-row>
                <div class="end-date">
                  The end of the survey is approximately: {{ expireTimeString }}
                </div>
              </el-row>
            </el-form-item>
          </el-form>
          <el-form ref="form" label-width="20px" class="form-side">
            <el-form-item>
              <el-row>
                <el-col :span="20">
                  Please set the duration of this survey
                </el-col>
                <el-col :span="4">
                  <el-switch v-model="ifDuration"></el-switch>
                </el-col>
              </el-row>
              <el-row>
                <el-col :span="2"><i class="el-icon-time"></i></el-col>
                <el-col :span="3" :offset="1">
                  <el-input
                    v-model="durationHours"
                    @change="showDurationExpireTime"
                  ></el-input>
                </el-col>
                <el-col :span="2" :offset="1">hours</el-col>
                <el-col :span="3" :offset="1">
                  <el-input
                    v-model="durationMinutes"
                    @change="showDurationExpireTime"
                  ></el-input>
                </el-col>
                <el-col :span="2" :offset="1">mins</el-col>
              </el-row>
              <el-row> </el-row>
            </el-form-item>
          </el-form>

          <span slot="footer" class="dialog-footer">
            <el-button type="primary" @click="nextPublish">Next</el-button>
          </span>
        </el-dialog>
        <el-dialog
          :title="DialogTitle"
          :visible.sync="publishDialogVisible2"
          :append-to-body="true"
          width="30%"
          center
        >
          <el-form ref="form" label-width="20px" class="form-side">
            <el-form-item>
              <el-row>
                <el-col :span="20">
                  Please set the maximum number of respondents
                </el-col>
                <el-col :span="4">
                  <el-switch v-model="ifVolume"></el-switch>
                </el-col>
              </el-row>
              <el-row>
                <el-col :span="3">
                  <el-input v-model="respondents"></el-input>
                </el-col>
                <el-col :span="5" :offset="1">respondents</el-col>
              </el-row>
            </el-form-item>
          </el-form>

          <el-form ref="form" label-width="20px" class="form-side">
            <el-form-item>
              <el-row>
                <el-col :span="18">
                  Please select whether to allow the same user to answer
                  multiple times?
                </el-col>
                <el-col :span="4" :offset="2">
                  <el-switch v-model="ifMultiple"></el-switch>
                </el-col>
              </el-row>
            </el-form-item>
          </el-form>
          <el-form ref="form" label-width="20px" class="form-side">
            <el-form-item>
              <el-row>
                <el-col :span="18">
                  Please select whether to capture the user gaze?
                </el-col>
                <el-col :span="4" :offset="2">
                  <el-switch v-model="ifCaptureGaze"></el-switch>
                </el-col>
              </el-row>
            </el-form-item>
          </el-form>

          <span slot="footer" class="dialog-footer">
            <el-button type="primary" @click="previousPublish"
              >Previous</el-button
            >
            <el-button type="success" @click="finishSurvey(currentId)"
              >Publish</el-button
            >
          </span>
        </el-dialog>
        <el-dialog
          :title="DialogTitle"
          :visible.sync="linkDialogVisible"
          width="30%"
          center
        >
          <el-row class="linkTop">
            <el-col :offset="2">
              <i class="el-icon-link"></i>
              Get the link or share on social
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="18" :offset="1">
              <el-form class="form-side2">
                <el-link type="primary" :href="link">{{ link }}</el-link>
              </el-form>
            </el-col>
            <el-col :span="2">
              <el-button
                type="info"
                v-clipboard:copy="link"
                v-clipboard:success="onCopy"
                v-clipboard:error="onError"
                >CopyLink</el-button
              >
            </el-col>
          </el-row>
          <span slot="footer" class="dialog-footer">
            <el-button type="primary" @click="linkDialogVisible = false"
              >Finish</el-button
            >
          </span>
        </el-dialog>
      </tr>
    </table>
  </div>
</template>

<script>
import SurveyBuilder from './SurveyBuilder'
window.onclick = function (event) {
  var modal = document.getElementById('surveyModal')
  if (event.target == modal) {
    modal.style.display = 'none'
  }
}

import store from '../store/SurveyBuilder.js'
import SurveyServices from '../services/SurveyServices'
import pubsub from 'pubsub-js'
import axios from 'axios'

export default {
  name: 'Bin',
  store: store,
  components: { SurveyBuilder },
  data() {
    return {
      surveys: [],
      language: 'English',
      showSurveys: [],
      userId: 0,
      publishDialogVisible1: false,
      publishDialogVisible2: false,
      linkDialogVisible: false,
      DialogTitle: '  ',
      days: 0,
      hours: 0,
      minutes: 0,
      durationHours: 0,
      durationMinutes: 0,
      respondents: 0,
      ifDuration: true,
      ifTime: true,
      ifVolume: true,
      ifMultiple: true,
      ifCaptureGaze: true,
      order: 'time',
      ifTimeOrder: true,
      ifTitleOrder: true,
      types: ['primary', '', '', ''],
      currentId: 0,
      durationTime: 0,
      expireTime: ' ',
      expireTimeString: ' ',
      link: '',
    }
  },
  methods: {
    changeStatus() {
      this.$forceUpdate()
    },
    batchRecover() {
      const promises = []
      this.showSurveys
        .filter((i) => i.checked)
        .forEach((i) => {
          const promise = SurveyServices.patchSurvey(i.id, { deleted: 0 })
          promises.push(promise)
        })
      Promise.all(promises).then(() => {
        this.getSurveys()
      })
    },
    async showOrder() {
      this.showSurveys = this.surveys.map((i) =>
        Object.assign(i, {
          checked: false,
        })
      )
      if (this.order === 'time') {
        this.showSurveys.sort(function (a, b) {
          var x = a.id
          var y = b.id
          return x < y ? -1 : x < y ? 1 : 0
        })
      } else if (this.order === 'reverseTime') {
        this.showSurveys.sort(function (a, b) {
          var x = a.id
          var y = b.id
          return x > y ? -1 : x > y ? 1 : 0
        })
      } else if (this.order === 'name') {
        this.showSurveys.sort(function (a, b) {
          var x = a.name
          var y = b.name
          return x < y ? -1 : x < y ? 1 : 0
        })
      } else if (this.order === 'reverseName') {
        this.showSurveys.sort(function (a, b) {
          var x = a.name
          var y = b.name
          return x > y ? -1 : x > y ? 1 : 0
        })
      }
    },
    changeTimeOrder() {
      if (this.ifTimeOrder) {
        this.order = 'reverseTime'
        this.changeType(2)
      } else {
        this.order = 'time'
        this.changeType(1)
      }
      this.ifTimeOrder = !this.ifTimeOrder
      this.showOrder()
    },
    changeTitleOrder() {
      if (this.ifTitleOrder) {
        this.order = 'reverseName'
        this.changeType(4)
      } else {
        this.order = 'name'
        this.changeType(3)
      }
      this.ifTitleOrder = !this.ifTitleOrder
      this.showOrder()
    },
    changeType(num) {
      for (let i = 0; i < this.types.length; i++) {
        this.types[i] = ''
        if (i === num - 1) this.types[i] = 'primary'
      }
    },
    computeRemainingTime(expireTime, status) {
      if (expireTime === null) {
        return 'Unset'
      }
      if (status === 2) return 'Expired'
      let nowTime = new Date()
      let expire = new Date(expireTime)
      let milliseconds = expire.getTime() - nowTime.getTime()
      if (milliseconds <= 0) return 'Expired'
      let remainDays = Math.floor(milliseconds / (1000 * 60 * 60 * 24))
      milliseconds = milliseconds - remainDays * (1000 * 60 * 60 * 24)
      let remainHours = Math.floor(milliseconds / (1000 * 60 * 60))
      milliseconds = milliseconds - remainHours * (1000 * 60 * 60)
      let remainMinutes = Math.floor(milliseconds / (1000 * 60))
      return remainDays + 'd ' + remainHours + 'h ' + remainMinutes + 'mins'
    },
    computeTime(time) {
      let date = new Date(time)
      return (
        date.getFullYear() +
        '-' +
        (date.getUTCMonth() + 1) +
        '-' +
        date.getUTCDate()
      )
    },
    computeExpireTime(time, status) {
      if (status === 0 && time === null) return 'Unpublished'
      if (time === null) return 'Unlimited'
      let date = new Date(time)
      return (
        date.getFullYear() +
        '-' +
        (date.getUTCMonth() + 1) +
        '-' +
        date.getUTCDate()
      )
    },
    computeRespondents(current, required, status) {
      if (status === 0) return 'Unpublished'
      if (required === 0) return 'Unlimited'
      return current + '/' + required
    },
    async publishSurvey(id) {
      this.days = 0
      this.hours = 0
      this.minutes = 0
      this.respondents = 0
      this.ifTime = true
      this.ifVolume = true
      this.ifmultiple = true
      this.durationMinutes = 0
      this.durationHours = 0
      this.ifCaptureGaze = true
      const data = await SurveyServices.getSurvey(id)
      this.DialogTitle = data.name
      this.publishDialogVisible1 = true
      this.currentId = id
    },
    previousPublish() {
      this.publishDialogVisible1 = true
      this.publishDialogVisible2 = false
    },
    nextPublish() {
      this.publishDialogVisible1 = false
      this.publishDialogVisible2 = true
    },
    async finishSurvey(id) {
      let code = await SurveyServices.getSurveyCode(id)
      //111
      //this.$router.push(`/surveytaker/ + ${code}`)
      this.link = process.env.VUE_APP_WEBSITE +'surveytaker/' + code
      this.publishDialogVisible2 = false
      this.linkDialogVisible = true
      let nowDate = new Date()
      await SurveyServices.patchSurvey(id, {
        status: 1,
        publish_time: nowDate,
        is_repeat_answer: this.ifMultiple,
        if_capture_gaze: this.ifCaptureGaze,
      })
      if (this.ifTime) {
        this.expireTime = new Date()
        this.expireTime.setTime(
          nowDate.getTime() +
            1000 * 60 * 60 * 24 * this.days +
            1000 * 60 * 60 * this.hours +
            1000 * 60 * this.minutes
        )
        await SurveyServices.patchSurvey(id, { expire_time: this.expireTime })
      }
      if (this.ifVolume) {
        await SurveyServices.patchSurvey(id, {
          required_submission: this.respondents,
        })
      }
      if (this.ifDuration) {
        console.log('SENDING DURATION', this.durationTime)
        await SurveyServices.patchSurvey(id, { duration: this.durationTime })
      }
      await this.getSurveys()
    },
    showDurationExpireTime() {
      this.durationTime =
        1000 * 60 * 60 * this.durationHours + 1000 * 60 * this.durationMinutes
      console.log(this.durationTime)
    },
    showExpireTime() {
      let nowDate = new Date()
      this.expireTime = new Date()
      this.expireTime.setTime(
        nowDate.getTime() +
          1000 * 60 * 60 * 24 * this.days +
          1000 * 60 * 60 * this.hours +
          1000 * 60 * this.minutes
      )
      this.expireTimeString =
        this.expireTime.getFullYear() +
        '-' +
        (this.expireTime.getUTCMonth() + 1) +
        '-' +
        this.expireTime.getUTCDate() +
        ' ' +
        this.expireTime.getHours() +
        ':' +
        this.expireTime.getMinutes()
    },
    async endSurvey(id) {
      this.$confirm(
        'Do you want to end the release of this survey early???',
        'reminder',
        {
          confirmButtonText: 'Confirm',
          cancelButtonText: 'Cancel',
          type: 'warning',
        }
      )
        .then(async () => {
          this.$message({
            type: 'success',
            message: 'Successful end!',
          })
          await SurveyServices.patchSurvey(id, { status: 2 })
          await this.getSurveys()
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: 'Cancel end!',
          })
        })
    },
    showlinkDialogVisible(code) {
      this.linkDialogVisible = true
      this.link = process.env.VUE_APP_WEBSITE +'surveytaker/' + code
    },
    onCopy(e) {
      this.$message({
        type: 'success',
        message: 'Copy Successfully!',
      })
    },
    onError(e) {
      this.$message({
        type: 'info',
        message: 'Sorry!Copy Failed!',
      })
    },
    editSurvey(id) {
      this.$router.push(`build-survey/${id}`)
      window.location.reload()
    },
    goBack() {
      this.$router.push(`/My_Survey`)
    },
    handleFileUpload(e) {
      const selectedFile = document.getElementById('file-btn').files[0]
      //console.log(selectedFile)
      this.$axios
        .post('survey/import/' + this.userId, selectedFile, {
          headers: {
            'content-type': 'application/json',
          },
        })
        .then((res) => {
          this.$message({
            message: 'Survey has been imported!',
            type: 'success',
          })
          this.getSurveys()
        })
        .catch((reason) => {
          this.$message.error('Cannot import survey! Please check format!')
          this.getSurveys()
        })
    },
    async createSurvey() {
      const response = await SurveyServices.addSurvey({
        name: 'Survey Title',
        language: this.$t('g5.language'),
        consentText: 'qwerty',
        time_limit_minutes: '60',
        status: 0,
        researcher: this.userId,
      })

      this.$router.push(`build-survey/${response.id}`)
    },

    async recoverSurvey(id) {
      this.$confirm(
        'Are you sure you want to reover survey with id' + id,
        'reminder',
        {
          confirmButtonText: 'Confirm',
          cancelButtonText: 'Cancel',
          type: 'warning',
        }
      )
        .then(async () => {
          this.$message({
            type: 'success',
            message: 'successfully recover!',
          })
          await SurveyServices.patchSurvey(id, { deleted: 0 })
          let index = this.surveys.indexOf(
            this.surveys.filter((e) => e.id == id)[0]
          )
          this.surveys.splice(index, 1)
          await this.getSurveys()
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: 'cancel delete',
          })
        })
    },
    async deleteSurvey(id, name) {
      this.$confirm('Are you sure to delete survey: ' + name, 'reminder', {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning',
      })
        .then(async () => {
          this.$message({
            type: 'success',
            message: 'successfully delete!',
          })
          await SurveyServices.deleteSurvey(id)
          let index = this.surveys.indexOf(
            this.surveys.filter((e) => e.id == id)[0]
          )
          this.surveys.splice(index, 1)
          await this.getSurveys()
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: 'cancel delete',
          })
        })
    },
    async getSurveys() {
      await this.$axios
        .get('/api/surveys/deleted/' + this.userId)
        .then((res) => {
          console.log(res.data)
          this.surveys = res.data
        })
      await this.showOrder()
    },
    async getResponseExportUrl(id) {
      const response = await axios
        .get(this.$axios.defaults.baseURL + 'survey/responseNumber/' + id)
        .then((res) => {
          window.location.href =
            this.$axios.defaults.baseURL + 'survey/exportCsv/' + id
        })
        .catch((error) => {
          this.$alert("No submissions yet, can't export responses", 'Warning', {
            confirmButtonText: 'Confirm',
          })
        })
    },
    getConfigurationExportUrl(id) {
      return this.$axios.defaults.baseURL + 'survey/exportSurvey/' + id
    },
    async getStatUrl(id) {
      const response = await axios
        .get(this.$axios.defaults.baseURL + 'survey/responseNumber/' + id)
        .then((res) => {
          this.$router.push('/survey/' + id)
        })
        .catch((error) => {
          this.$alert("No submissions yet, can't view statistics", 'Warning', {
            confirmButtonText: 'Confirm',
          })
        })
    },
  },

  async beforeMount() {
    await this.$axios
      .get('account/user/', {
        headers: {
          Authorization: 'Token ' + localStorage.getItem('token'),
        },
      })
      .catch((reason) => {
        //update user status
        pubsub.publish('logoutAction', false)
        //remove token when logout
        localStorage.removeItem('token')
        this.$router.replace({
          name: 'login',
        })
      })
      .then((res) => {
        this.userId = res.data.pk
      })
    await this.getSurveys()
  },
}
</script>

<style scoped>
.main {
  padding: 30px;
}

#survey-table {
  border-collapse: collapse;
}

#survey-table tr {
  border-bottom: 1px solid black;
}

#survey-table td {
  padding: 8px 30px 8px 0px;
  min-width: 100px;
  text-align: left;
}

#survey-table th {
  text-align: left;
  font-weight: 300;
}

.my-survey-wrapper {
  width: 100%;
  height: 800px;
  background-color: white;
  position: relative;
  display: flex;
  flex-wrap: wrap;
}

.my-survey-item {
  margin-left: 75px;
  margin-top: 50px;
  flex-basis: 25%;
  padding-left: 8px;
  padding-right: 8px;
  width: 200px;
  height: 250px;
  position: relative;
  border-style: solid;
  border-width: 5px;
}

.action-btn {
  cursor: pointer;
  border: 1px solid black;
  padding: 5px 10px;
  color: black;
  font-size: 15px;
  border-radius: 5px;
  text-decoration: none;
  margin: 2px 10px 2px 0px;
  display: inline-block;
}
.action-btn-edit {
  cursor: pointer;
  border: 1px solid black;
  padding: 5px 16px;
  color: black;
  font-size: 15px;
  border-radius: 5px;
  text-decoration: none;
  margin: 2px 10px 2px 0px;
  display: inline-block;
}
.action-btn-edit:hover {
  color: gray;
}

.action-btn-publish {
  cursor: pointer;
  border: 1px solid black;
  padding: 5px 25px;
  background: #18e200;
  color: black;

  font-size: 15px;
  border-radius: 5px;
  text-decoration: none;
  margin: 2px 10px 2px 0px;
  display: inline-block;
}

.action-btn-publish:hover {
  color: gray;
}
.action-btn-end {
  cursor: pointer;
  border: 1px solid black;
  padding: 5px 11px;
  background: #c80000;
  color: black;
  font-size: 15px;
  border-radius: 5px;
  text-decoration: none;
  margin: 2px 10px 2px 0px;
  display: inline-block;
}

.action-btn-end:hover {
  color: gray;
}
.action-btn-mute {
  cursor: pointer;
  border: 1px solid black;
  padding: 5px 21px;
  background: #7f7f7f;
  color: black;
  font-size: 15px;
  border-radius: 5px;
  text-decoration: none;
  margin: 2px 10px 2px 0px;
  display: inline-block;
}
.form-side {
  margin-top: 5px;
  border: 1px solid #999999;
  margin-bottom: 15px;
  border-radius: 10px;
}
.form-side2 {
  border: 1px solid #999999;
  margin-bottom: 10px;
  border-radius: 5px;
  padding: 9px 25px 9px 25px;
  margin-right: 5px;

  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  -o-text-overflow: ellipsis;
}

.end-date {
  margin-top: 10px;
  color: brown;
}

.linkTop {
  margin-bottom: 10px;
}

.language {
  color: white;
}

.moreInfoB {
  position: absolute;
  left: 5px;
  bottom: 5px;
  border: 1px solid black;
  padding: 5px;
  color: black;
  background-color: white;
  border-radius: 10px;
  font-size: 15px;
}

.action-btn:hover {
  opacity: 0.5;
}

/* The Modal (background) */
.modal {
  display: none; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  padding-top: 100px; /* Location of the box */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0, 0, 0); /* Fallback color */
  background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */
}

/* Modal Content */
.modal-content {
  background-color: #fefefe;
  margin: auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

.myChart {
  border: solid;
}

/* The Close Button */
.close {
  color: #aaaaaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: #000;
  text-decoration: none;
  cursor: pointer;
}
</style>
