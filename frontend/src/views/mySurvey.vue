<template>
  <div>
    <div class="spinner" v-if="isLoading">
      <Spinner />
    </div>
    <div v-else class="main">
      <h1>{{ $t('g5.My Surveys') }}</h1>
      <el-input :placeholder="$t('g5.Search by title')" suffix-icon="el-icon-search"
        style="display: inline-block; width: 180px; margin-right: 12px" v-model="keyword">
      </el-input>
      <el-select :placeholder="$t('g5.Select by language')"
        style="display: inline-block; width: 180px; margin-right: 12px" v-model="shLang">
        <el-option v-for="item in optionsLang" :key="item" :label="item" :value="item">
        </el-option>
      </el-select>
      <el-select :placeholder="$t('g5.Select by Survey Status')"
        style="display: inline-block; width: 180px; margin-right: 12px" v-model="shStatus">
        <el-option v-for="item in optionsStatus" :key="item.value" :label="item.label" :value="item.value">
        </el-option>
      </el-select>
      <!-- List Table or Card Table -->
      <!-- <el-switch v-model="listType" :active-text="$t('g5.Card')" :inactive-text="$t('g5.List')">
      </el-switch> -->

      <div v-if="this.emails.length > 0">
          <br /><br />
          <el-alert
            title="You have an invitation email pending, please check it!"
            type="info"
            class="custom-alert"
            show-icon
            close-text=""
          ></el-alert>
      </div>

      <br /><br />
      <a @click="createSurvey" class="action-btn">{{ $t('g5.ms-create') }}</a>
      <label for="file-btn" class="action-btn">{{
        $t('g5.Import Survey')
      }}</label>
      <a @click="goToBin" class="action-btn">{{ $t('g5.ms-bin') }}</a>
      <a @click="batchDelete" class="action-btn">{{ $t('g5.Delete') }}</a>
      <!-- <input
        type="file"
        id="file-btn"
        style="visibility: hidden"
        v-on:change="handleFileUpload()"
        accept="application/json"
      /> -->
      <!-- <el-input
         placehodler="请输入调查名称"
         suffix-icon='el-icon-search'
         style="display: inline-block; width:180px"
         v-model='keyword' >
      </el-input > -->
      <br /><br />
      <!-- List Style table -->
      <!-- <table v-if="!listType" id="survey-table"> -->
      <table v-if="listType" id="survey-table">
        <!-- Survey dashboard -->
        <div class="language"></div>
        <tr>
          <th>
            <el-link :underline="false">
              {{ $t('home.card3Info1') }}
              <i class="el-icon-arrow-down"></i>
            </el-link>
          </th>
          <th class="survey_title" v-if="ifTitleOrder">
            <el-link :underline="false" @click="changeTitleOrder" :type="types[2]">
              {{ $t('g5.ms-title') }}
              <i class="el-icon-arrow-down"></i>
            </el-link>
          </th>
          <th v-if="!ifTitleOrder">
            <el-link :underline="false" @click="changeTitleOrder" :type="types[3]">
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
        <tr v-for="survey in pageSurveys" :key="survey.id">
          <td>
            <el-checkbox v-model="survey.checked" @change="changeStatus"></el-checkbox>
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
            <span v-if="survey.status === 0"><i class="fas fa-circle" style="color: #1947e5"></i>
              {{ $t('g5.Saved') }}
            </span>
            <span v-if="survey.status === 1"><i class="fas fa-circle" style="color: #18e200"></i>
              {{ $t('g5.Published') }}
            </span>
            <span v-if="survey.status === 2"><i class="fas fa-circle" style="color: grey"></i>
              {{ $t('g5.Finished') }}
            </span>
          </td>
          <td style="padding-right: 0">
            <a class="action-btn-edit" @click="editSurvey(survey.id)" v-if="survey.status === 0">{{ $t('g5.ms-edit')
            }}</a>
            <a class="action-btn" v-if="survey.status === 1" @click="showlinkDialogVisible(survey.code)">{{ $t('g5.Share')
            }}</a>
            <a class="action-btn" v-if="survey.status === 2">{{
              $t('g5.Share')
            }}</a>
            <a @click="getStatUrl(survey.id)" class="action-btn">{{
              $t('g5.ms-view-stats')
            }}</a>
            <a @click="getResponseExportUrl(survey.id)" class="action-btn">{{
              $t('g5.Export')
            }}</a>
            <a :href="getConfigurationExportUrl(survey.id)" class="action-btn">{{ $t('g5.ms-export-conf') }}</a>
            <span>
              <select class="action-btn" v-model="cloneLanguage">
                <option v-for="[key, value] in Object.entries(languageOptions)" :value="key" :id="key">
                  {{ value }}
                </option>
              </select>
              <a class="action-btn" @click="cloneSurvey(survey.id, survey.name)">{{ $t('g5.Clone') }}</a>
            </span>
            <a class="action-btn" @click="deleteSurvey(survey.id, survey.name)">{{ $t('g5.Delete') }}</a>
            <a class="action-btn" @click="collaborator(survey.id, survey.name)"
              v-if="survey.status === 0 && survey.researcher == userId"
              >{{ $t('g5.Add-collaborator') }}</a
            >
            <a
              class="action-btn"
              @click="removeCollaborator(survey.id, userId)"
              v-if="survey.status === 0 && survey.researcher != userId"
              >{{ $t('g5.Remove-collaborators') }}</a
            >

            <a class="action-btn-publish" @click="publishSurvey(survey.id)" v-if="survey.status === 0">{{ $t('g5.Publish')
            }}</a>
            <a class="action-btn-end" @click="endSurvey(survey.id)" v-else-if="survey.status === 1">{{ $t('g5.End Survey')
            }}</a>
            <a class="action-btn-mute" v-if="survey.status === 2">{{
              $t('g5.Finished')
            }}</a>
            <a class="action-btn" v-if="survey.status === 1" @click="settings(survey.id)">{{ $t('g5.Settings') }}</a>
          </td>
          <el-dialog :title="DialogTitle" :visible.sync="publishDialogVisible1" :append-to-body="true" width="30%" center>
            <el-form ref="form" label-width="20px" class="form-side">
              <el-form-item>
                <el-row>
                  <el-col :span="20">
                    {{ $t('g5.Please set the deadline of this survey') }}
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
                  <el-col :span="2" :offset="1">{{ $t('g5.days') }}</el-col>
                  <el-col :span="3" :offset="1">
                    <el-input v-model="hours" @change="showExpireTime"></el-input>
                  </el-col>
                  <el-col :span="2" :offset="1">{{ $t('g5.hours') }}</el-col>
                  <el-col :span="3" :offset="1">
                    <el-input v-model="minutes" @change="showExpireTime"></el-input>
                  </el-col>
                  <el-col :span="2" :offset="1">{{ $t('g5.mins') }}</el-col>
                </el-row>
                <el-row>
                  <div class="end-date">
                    {{ $t('g5.The end of the survey is approximately:') }}
                    {{ expireTimeString }}
                  </div>
                </el-row>
              </el-form-item>
            </el-form>
            <el-form ref="form" label-width="20px" class="form-side">
              <el-form-item>
                <el-row>
                  <el-col :span="20">
                    {{ $t('g5.Please set the duration of this survey') }}
                  </el-col>
                  <el-col :span="4">
                    <el-switch v-model="ifDuration"></el-switch>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="2"><i class="el-icon-time"></i></el-col>
                  <el-col :span="3" :offset="1">
                    <el-input v-model="durationHours" @change="showDurationExpireTime"></el-input>
                  </el-col>
                  <el-col :span="2" :offset="1">{{ $t('g5.hours') }}</el-col>
                  <el-col :span="3" :offset="1">
                    <el-input v-model="durationMinutes" @change="showDurationExpireTime"></el-input>
                  </el-col>
                  <el-col :span="2" :offset="1">{{ $t('g5.mins') }}</el-col>
                </el-row>
                <el-row> </el-row>
              </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
              <el-button type="primary" @click="nextPublish">{{
                $t('g5.Next')
              }}</el-button>
            </span>
          </el-dialog>
          <el-dialog :title="DialogTitle" :visible.sync="publishDialogVisible2" :append-to-body="true" width="30%" center>
            <el-form ref="form" label-width="20px" class="form-side">
              <el-form-item>
                <el-row>
                  <el-col :span="20">
                    {{ $t('g5.Please set the maximum number of respondents') }}
                  </el-col>
                  <el-col :span="4">
                    <el-switch v-model="ifVolume"></el-switch>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="3">
                    <el-input v-model="respondents"></el-input>
                  </el-col>
                  <el-col :span="5" :offset="1">{{
                    $t('g5.respondents')
                  }}</el-col>
                </el-row>
              </el-form-item>
            </el-form>
            <el-form ref="form" label-width="20px" class="form-side">
              <el-form-item>
                <el-row>
                  <el-col :span="18">
                    {{
                      $t(
                        'g5.Please select whether to allow the same user to answer multiple times ?'
                      )
                    }}
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
                    {{
                      $t('g5.Please select whether to capture the user gaze?')
                    }}
                  </el-col>
                  <el-col :span="4" :offset="2">
                    <el-switch v-model="ifCaptureGaze"></el-switch>
                  </el-col>
                </el-row>
              </el-form-item>
              <el-form-item v-if="ifCaptureGaze">
                <el-row>
                  <el-col :span="18">
                    {{
                      $t(
                        'g5.If the user does not agree to turn on the camera, select whether the survey can be answered'
                      )
                    }}
                  </el-col>
                  <el-col :span="4" :offset="2">
                    <el-switch v-model="ifAgreeAnswer"></el-switch>
                  </el-col>
                </el-row>
              </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
              <el-button type="primary" @click="previousPublish">{{
                $t('g5.Previous')
              }}</el-button>
              <el-button type="success" @click="finishSurvey(currentId)">{{
                $t('g5.Publish')
              }}</el-button>
            </span>
          </el-dialog>
        </tr>
      </table>
      <!-- Card Style table -->
      <div v-else>
        <el-row>
          <el-col :span="24" v-for="(survey, index) in pageSurveys" :key="survey.id" :style="{ padding: '10px' }">
            <el-card :body-style="{ padding: '0px', marginBottom: 10 }">
              <img :style="{ width: '100%' }" :src="cardImg" class="image" />
              <div style="padding: 14px">
                <span class="card-title">{{ survey.name }}</span>
                <div class="bottom clearfix card-btns">
                  <!-- <time class="time">{{ currentDate }}</time> -->
                  <!-- <el-button type="text" class="button">操作按钮</el-button> -->
                  <el-button type="text" class="action-btn-edit" @click="editSurvey(survey.id)"
                    v-if="survey.status === 0">{{ $t('g5.ms-edit') }}</el-button>
                  <el-button type="text" class="action-btn" v-if="survey.status === 1"
                    @click="showlinkDialogVisible(survey.code)">{{ $t('g5.Share') }}</el-button>
                  <el-button type="text" class="action-btn" v-if="survey.status === 2">{{ $t('g5.Share') }}</el-button>
                  <el-button type="text" @click="getStatUrl(survey.id)" class="action-btn">{{ $t('g5.ms-view-stats')
                  }}</el-button>
                  <el-button type="text" @click="getResponseExportUrl(survey.id)" class="action-btn">{{ $t('g5.Export')
                  }}</el-button>
                  <el-button type="text" :href="getConfigurationExportUrl(survey.id)" class="action-btn">{{
                    $t('g5.ms-export-conf') }}</el-button>
                  <span>
                    <select class="action-btn" v-model="cloneLanguage">
                      <option v-for="[key, value] in Object.entries(languageOptions)" :value="key" :id="key">
                        {{ value }}
                      </option>
                    </select>
                    <el-button type="text" class="action-btn" @click="cloneSurvey(survey.id, survey.name)">{{
                      $t('g5.Clone') }}</el-button>
                  </span>
                  <el-button type="text" class="action-btn" @click="deleteSurvey(survey.id, survey.name)">{{
                    $t('g5.Delete') }}</el-button>
                  <el-button type="text" class="action-btn" @click="collaborator(survey.id, survey.name)" v-if="survey.status === 0"
                    >{{ $t('g5.Add-collaborator') }}</el-button
                  >
                  <el-button type="text" class="action-btn-publish" @click="publishSurvey(survey.id)"
                    v-if="survey.status === 0">{{ $t('g5.Publish') }}</el-button>
                  <el-button type="text" class="action-btn-end" @click="endSurvey(survey.id)"
                    v-else-if="survey.status === 1">{{ $t('g5.End Survey') }}</el-button>
                  <el-button type="text" class="action-btn-mute" v-if="survey.status === 2">{{ $t('g5.Finished')
                  }}</el-button>
                  <el-button type="text" class="action-btn" v-if="survey.status === 1" @click="settings(survey.id)">{{
                    $t('g5.Settings') }}</el-button>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
      <el-dialog :title="DialogTitle" :visible.sync="linkDialogVisible" width="30%" center>
        <el-row class="linkTop">
          <el-col :offset="2">
            <i class="el-icon-link"></i>
            {{ $t('g5.Get the link or share on social') }}
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="18" :offset="1">
            <el-form class="form-side2">
              <el-link type="primary" @click="jumpToSurveyTaker">{{
                link
              }}</el-link>
            </el-form>
          </el-col>
          <el-col :span="2">
            <el-button type="info" v-clipboard:copy="link" v-clipboard:success="onCopy" v-clipboard:error="onError">
              {{ $t('g5.CopyLink') }}</el-button>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="8" :offset="8">
            <img :src="dataUrl" id="123123" />
          </el-col>
        </el-row>
        <span slot="footer" class="dialog-footer">
          <el-button @click="downloadQR">{{ $t('g5.DownloadQR') }}</el-button>
          <el-button type="primary" @click="linkDialogVisible = false">{{
            $t('g5.Finish')
          }}</el-button>
        </span>
      </el-dialog>
      <el-pagination @current-change="handleCurrentChange" :current-page="currentPage" :page-size="10"
        layout="total, prev, pager, next, jumper" :total="filterSurveys.length">
      </el-pagination>
    </div>
  </div>
</template>

<script>
import SurveyBuilder from './SurveyBuilder'
import Spinner from '../components/Spinner'
window.onclick = function (event) {
  var modal = document.getElementById('surveyModal')
  if (event.target == modal) {
    modal.style.display = 'none'
  }
}

import store from '../store/SurveyBuilder.js'
import SurveyServices from '../services/SurveyServices'
import pubsub from 'pubsub-js'

import QRCode from 'qrcode'

import axios from 'axios'
import cardImg from '@/assets/img/4181666746080_.pic.jpg'
export default {
  name: 'mySurvey',
  store: store,
  components: { SurveyBuilder, Spinner },
  data() {
    return {
      currentPage: 1,
      keyword: '',
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
      ifDuration: false,
      ifTime: false,
      ifVolume: false,
      ifMultiple: false,
      ifCaptureGaze: false,
      ifAgreeAnswer: false,
      order: 'time',
      ifTimeOrder: false,
      ifTitleOrder: false,
      types: ['primary', '', '', ''],
      currentId: 0,
      durationTime: 0,
      expireTime: ' ',
      expireTimeString: ' ',
      link: '',
      dataUrl: '',
      // Page Type:PC/Mobile
      listType: true,
      // Record the size of the screen
      screenWidth: null,
      // Flag for reload
      render: true,
      cardImg,
      // optionsLang: [],
      optionsStatus: [
        {
          label: this.$t('g5.Saved'),
          value: 0,
        },
        {
          label: this.$t('g5.Published'),
          value: 1,
        },
        {
          label: this.$t('g5.Finished'),
          value: 2,
        },
      ],
      shLang: '',
      shStatus: '',
      cloneLanguage: '',
      languageOptions: {
        en: 'English',
        ka: 'ಕನ್ನಡ ',
        ja: '日本語',
        ur: 'اردو',
        hi: 'हिन्दी',
        zh: '中文',
      },
      isLoading: false,
      emails: []
    }
  },
  watch: {
    link(n, o) {
      if (n) {
        QRCode.toDataURL(n)
          .then((url) => {
            console.log(url)
            this.dataUrl = url
          })
          .catch((err) => {
            console.error(err)
          })
      }
    },
    // screenWidth: {
    //   handler: function (val, oldVal) {
    //     // Mobile width<766
    //     console.log("The Screen width is:");
    //     console.log(val);
    //     if (val < 766) {
    //       // Card Table
    //       this.listType = false;
    //     } else {
    //       // List Table
    //       this.listType = true;
    //     }
    //   }
    // }
  },
  mounted() {
    // When initialization, get the screen width
    window.addEventListener('load', this.checkWidth)
    //If the window size hange, reload the page
    window.addEventListener('resize', this.checkWidth)
    window.addEventListener('resize', this.reload)
  },
  computed: {
    optionsLang() {
      return Array.from(new Set(this.showSurveys.map((e) => e.language)))
    },
    pageSurveys() {
      return this.filterSurveys.slice(
        (this.currentPage - 1) * 10,
        this.currentPage * 10
      )
    },

    filterSurveys() {
      let res = this.showSurveys
      console.log(this.showSurveys)
      if (this.keyword) {
        res = res.filter((i) => i.name.includes(this.keyword))
      }
      if (this.shLang) {
        res = res.filter((i) => i.language === this.shLang)
      }
      if (this.shStatus !== '') {
        res = res.filter((i) => i.status === this.shStatus)
      }

      // if ()
      return res
    },
  },
  methods: {
    downloadQR() {
      var base64 = this.dataUrl // imgSrc 就是base64哈
      var byteCharacters = atob(
        base64.replace(/^data:image\/(png|jpeg|jpg);base64,/, '')
      )
      var byteNumbers = new Array(byteCharacters.length)
      for (var i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i)
      }
      var byteArray = new Uint8Array(byteNumbers)
      var blob = new Blob([byteArray], {
        type: undefined,
      })
      var aLink = document.createElement('a')
      aLink.download = '图片名称.jpg' //这里写保存时的图片名称
      aLink.href = URL.createObjectURL(blob)
      aLink.click()
    },
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
        this.listType = false;
      }
      else {
        this.listType = true;
      }
    },
    changeStatus() {
      this.$forceUpdate()
    },
    handleCurrentChange(val) {
      this.currentPage = val
    },
    jumpToSurveyTaker() {
      window.open(this.link, '_blank')
      this.linkDialogVisible = false
    },
    async goToBin() {
      this.$router.push(`/bin`)
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
    collaborator(id, name){
        this.$router.push({
        name: 'invite',
        params: { id: id, name: name }
      });
    },
    removeCollaborator(surveyid, userId){
        const confirmed = confirm('Are you sure you want to remove yourself from collaboration?');
        if (confirmed){
            this.$axios
                .post('survey/collaborators/delete/', {survey_id: surveyid,
                                                       user_id: userId})
                .then(() => {
                    alert('Delete successfully.');
                    window.location.reload()
                })
                .catch((error) => {
                // Handle error
                alert('Failed, please try again.'+error)
                window.location.reload()
                });
        }else{
            alert('Operation canceled.');
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
        return this.$t('g5.Unset')
      }
      if (status === 2) return this.$t('g5.Expired')
      let nowTime = new Date()
      let expire = new Date(expireTime)
      let milliseconds = expire.getTime() - nowTime.getTime()
      if (milliseconds <= 0) {
        SurveyServices.patchSurvey(id, { status: 2 })
        return this.$t('g5.Expired')
      }
      let remainDays = Math.floor(milliseconds / (1000 * 60 * 60 * 24))
      milliseconds = milliseconds - remainDays * (1000 * 60 * 60 * 24)
      let remainHours = Math.floor(milliseconds / (1000 * 60 * 60))
      milliseconds = milliseconds - remainHours * (1000 * 60 * 60)
      let remainMinutes = Math.floor(milliseconds / (1000 * 60))
      return (
        remainDays +
        this.$t('g5.days') +
        remainHours +
        this.$t('g5.hours') +
        remainMinutes +
        this.$t('g5.mins')
      )
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
      if (status === 0 && time === null) return this.$t('g5.Unpublished')
      if (time === null) return this.$t('g5.Unlimited')
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
      if (status === 0) return this.$t('g5.Unpublished')
      if (required === -1) return this.$t('g5.Unlimited')
      return current + '/' + required
    },
    async publishSurvey(id) {
      this.days = 0
      this.hours = 0
      this.minutes = 0
      this.respondents = 0
      this.ifTime = false
      this.ifVolume = false
      this.ifDuration = false
      this.ifMultiple = false
      this.durationMinutes = 0
      this.durationHours = 0
      this.ifCaptureGaze = false
      this.ifAgreeAnswer = false
      this.expireTimeString = ''
      const data = await SurveyServices.getSurvey(id)
      this.DialogTitle = data.name
      this.publishDialogVisible1 = true
      this.currentId = id
    },
    async settings(id) {
      this.ifAgreeAnswer = false
      const data = await SurveyServices.getSurvey(id)
      console.log(data)
      this.expireTimeString = ''
      this.DialogTitle = data.name
      this.publishDialogVisible1 = true
      this.currentId = id
      this.days = 0
      this.hours = 0
      this.minutes = 0
      if (data.expire_time === null) {
        this.ifTime = false
      } else {
        this.ifTime = true
        this.ComputeTime(data.expire_time)
      }
      if (data.duration === -1) {
        this.ifDuration = false
        this.durationMinutes = 0
        this.durationHours = 0
      } else {
        this.ifDuration = true
        let durationTime = data.duration / 60000
        console.log(durationTime)
        this.durationHours = Math.floor(durationTime / 60)
        this.durationMinutes = durationTime - this.durationHours * 60
      }
      if (data.required_submission === -1) {
        this.ifVolume = false
        this.respondents = 0
      } else {
        this.ifVolume = true
        this.respondents = data.required_submission
      }
      this.ifMultiple = data.is_repeat_answer
      this.ifCaptureGaze = data.if_capture_gaze
      this.ifAgreeAnswer = data.camera
    },
    ComputeTime(str) {
      var reg = /^(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)/
      var s = str.match(reg)
      var newDate = this.getZeroTimeZone()
      var result = ''
      if (s) {
        result = new Date(s[1], s[2] - 1, s[3], s[4], s[5], s[6])
      }
      console.log(result)
      var minutes = Math.floor((result.getTime() - newDate.getTime()) / 60000)
      this.days = Math.floor(minutes / (60 * 24))
      minutes = minutes - this.days * (60 * 24)
      this.hours = Math.floor(minutes / 60)
      this.minutes = minutes - this.hours * 60
      this.showExpireTime()
    },
    getZeroTimeZone() {
      var d = new Date()
      var len = d.getTime()
      var offset = d.getTimezoneOffset() * 60000
      var utcTime = len + offset
      return new Date(utcTime)
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
      const data = await SurveyServices.getSurvey(id)
      //111
      //this.$router.push(`/surveytaker/ + ${code}`)
      this.link = process.env.VUE_APP_WEBSITE +'surveytaker/' + code
      if (this.ifVolume && data.current_submission >= this.respondents) {
        this.$confirm(
          this.$t(
            'g5.Such setting will make the survey end directly, whether to continue?'
          ),
          this.$t('g5.reminder'),
          {
            confirmButtonText: this.$t('g5.Confirm'),
            cancelButtonText: this.$t('g5.Cancel'),
            type: 'warning',
          }
        )
          .then(async () => {
            await this.patchSurveyInfo(id, 2)
          })
          .catch(() => { })
      } else {
        await this.patchSurveyInfo(id, 1)
      }
    },
    async patchSurveyInfo(id, status) {
      if (!this.ifCaptureGaze) this.ifAgreeAnswer = false
      const data = await SurveyServices.getSurvey(id)
      this.publishDialogVisible2 = false
      this.linkDialogVisible = true
      let nowDate = new Date()
      await SurveyServices.patchSurvey(id, {
        status: status,
        is_repeat_answer: this.ifMultiple,
        if_capture_gaze: this.ifCaptureGaze,
        camera: this.ifAgreeAnswer,
      })
      if (data.publish_time === null) {
        await SurveyServices.patchSurvey(id, { publish_time: nowDate })
      }
      await SurveyServices.patchSurvey(id, {
        status: 1,
        publish_time: nowDate,
        is_repeat_answer: this.ifMultiple,
        if_capture_gaze: this.ifCaptureGaze,
        camera: this.ifAgreeAnswer,
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
      } else {
        await SurveyServices.patchSurvey(id, { expire_time: null })
      }
      if (this.ifVolume) {
        await SurveyServices.patchSurvey(id, {
          required_submission: this.respondents,
        })
      } else {
        await SurveyServices.patchSurvey(id, { required_submission: -1 })
      }
      if (this.ifDuration) {
        await SurveyServices.patchSurvey(id, { duration: this.durationTime })
      } else {
        await SurveyServices.patchSurvey(id, { duration: -1 })
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
      console.log(
        1000 * 60 * 60 * 24 * Number(this.days) +
        1000 * 60 * 60 * Number(this.hours) +
        1000 * 60 * Number(this.minutes),
        nowDate.getTime()
      )
      this.expireTime.setTime(
        nowDate.getTime() +
        1000 * 60 * 60 * 24 * Number(this.days) +
        1000 * 60 * 60 * Number(this.hours) +
        1000 * 60 * Number(this.minutes)
      )
      this.expireTimeString =
        this.expireTime.getFullYear() +
        '-' +
        (this.expireTime.getUTCMonth() + 1) +
        '-' +
        this.expireTime.getDate() +
        ' ' +
        this.expireTime.getHours() +
        ':' +
        this.expireTime.getMinutes()
    },
    async endSurvey(id) {
      this.$confirm(
        this.$t('g5.Do you want to end the release of this survey early?'),
        this.$t('g5.reminder'),
        {
          confirmButtonText: this.$t('g5.Confirm'),
          cancelButtonText: this.$t('g5.Cancel'),
          type: 'warning',
        }
      )
        .then(async () => {
          this.$message({
            type: 'success',
            message: this.$t('g5.Successful end!'),
          })
          await SurveyServices.patchSurvey(id, { status: 2 })
          await this.getSurveys()
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: this.$t('g5.Cancel end!'),
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
        message: this.$t('g5.Copy Successfully!'),
      })
    },
    onError(e) {
      this.$message({
        type: 'info',
        message: this.$t('g5.Sorry!Copy Failed!'),
      })
    },
    editSurvey(id) {
      this.$router.push(`build-survey/${id}`)
      window.location.reload()
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
            message: this.$t('g5.Survey has been imported!'),
            type: 'success',
          })
          this.getSurveys()
        })
        .catch((reason) => {
          this.$message.error(
            this.$t('g5.Cannot import survey! Please check format!')
          )
          this.getSurveys()
        })
    },
    async createSurvey() {
      const response = await SurveyServices.addSurvey({
        name: this.$t('g5.Survey Title'),
        language: this.$t('g5.language'),
        consentText: 'qwerty',
        time_limit_minutes: '60',
        status: 0,
        researcher: this.userId,
      })

      this.$router.push(`build-survey/${response.id}`)
    },
    batchDelete() {
      this.showSurveys
        .filter((i) => i.checked)
        .forEach((i) => {
          SurveyServices.patchSurvey(i.id, { deleted: 1 }).then(() => {
            let index = this.surveys.indexOf(
              this.surveys.filter((e) => e.id == i.id)[0]
            )
            this.surveys.splice(index, 1)
            let showIndex = this.showSurveys.indexOf(
              this.showSurveys.filter((e) => e.id == i.id)[0]
            )
            this.showSurveys.splice(showIndex, 1)
          })
        })
    },
    async deleteSurvey(id, name) {
      this.$confirm(
        'Are you sure to delete survey: ' + name + ' ?',
        'Reminder',
        {
          confirmButtonText: this.$t('g5.Confirm'),
          cancelButtonText: this.$t('g5.Cancel'),
          type: 'warning',
        }
      )
        .then(async () => {
          try {
            await SurveyServices.patchSurvey(id, { deleted: 1 })
            this.$message({
              type: 'success',
              message: 'Successfully delete!',
            })
            let index = this.surveys.indexOf(
              this.surveys.filter((e) => e.id == id)[0]
            )
            this.surveys.splice(index, 1)
            await this.getSurveys()
          } catch (err) {
            this.$message({
              type: 'error',
              message: 'Delete Failed!',
            })
          }
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: 'cancel delete',
          })
        })
    },
    async cloneSurvey(id, name) {
      if (this.cloneLanguage === '') {
        const clonedSurvey = this.pageSurveys.filter(
          (survey) => survey.id === id
        )
        const languageKey = Object.keys(this.languageOptions).find(
          (key) => this.languageOptions[key] === clonedSurvey[0].language
        )
        this.cloneLanguage = languageKey
        console.log('cloneLanguage', this.cloneLanguage)
      }
      this.$confirm(
        'Are you sure to clone survey: ' + name + ' ?',
        'Reminder',
        {
          confirmButtonText: 'Confirm',
          cancelButtonText: 'Cancel',
          type: 'warning',
        }
      )
        .then(async () => {
          this.isLoading = true
          try {
            await SurveyServices.cloneSurvey(
              id,
              this.userId,
              this.cloneLanguage
            )
            this.$message({
              type: 'success',
              message: 'Successfully clone!',
            })
            await this.getSurveys()
          } catch (err) {
            this.$message({
              type: 'error',
              message: 'Clone Failed!',
            })
          } finally {
            this.isLoading = false
          }
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: 'Cancel clone',
          })
        })
    },
    async getSurveys() {
      await this.$axios
        .get('/api/surveys/researcher/' + this.userId)
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
          this.$alert(
            "No submissions yet, can't export responses",
            this.$t('g5.reminder'),
            {
              confirmButtonText: this.$t('g5.Confirm'),
            }
          )
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
          this.$alert(
            "No submissions yet, can't view statistics",
            this.$t('g5.reminder'),
            {
              confirmButtonText: this.$t('g5.Confirm'),
            }
          )
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

    await this.$axios
    .get('emailInfo/get_emails/' + this.userId)
    .then((response) => {
        this.emails = response.data
    })
    .catch((error) => {
        // Handle error
    });
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
  /* min-width: 100px; */
  text-align: left;
}

#survey-table th {
  text-align: left;
  font-weight: 500;
  font-size: 15px;
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
  display: none;
  /* Hidden by default */
  position: fixed;
  /* Stay in place */
  z-index: 1;
  /* Sit on top */
  padding-top: 100px;
  /* Location of the box */
  left: 0;
  top: 0;
  width: 100%;
  /* Full width */
  height: 100%;
  /* Full height */
  overflow: auto;
  /* Enable scroll if needed */
  background-color: rgb(0, 0, 0);
  /* Fallback color */
  background-color: rgba(0, 0, 0, 0.4);
  /* Black w/ opacity */
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
.card-title {
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  display: block;
  font-size: 24px;
  font-weight: 600;
  text-align: center;
  margin-bottom: 2rem;
}

.card-btns {
  height: 155px;
  overflow-y: auto;
}

.custom-alert {
  color: red; /* Set the text color to red */
}

.spinner {
  position: absolute;
  top: 40%;
  left: 50%;
}
</style>
