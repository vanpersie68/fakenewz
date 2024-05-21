<template>
  <!-- Not Flow view - normal edit view -->
  <div v-if="!flowView" class="work-space">
    <div class="survey-title">
      <h1 id="title" contenteditable="true" @focusout="handleTitleInput">
        {{ surveyTitle }}
      </h1>
      <el-button id="preview_btn" type="primary" @click="showPreview()">{{
        $t('workSpace.preview')
      }}</el-button>
      <el-button id="save_btn" type="success" @click="saveSurvey">{{
        $t('workSpace.save')
      }}</el-button>
    </div>

    <line-base class="light"></line-base>
    <button-base class="tertiary min" :icon="'fas fa-plus fa-sm'" :title="$t('workSpace.addNewBlock')"
      @buttonPress="$store.commit('insertNewBlock', { order: 1 })"></button-base>

    <line-base class="light"></line-base>
    <div class="block-segment" v-for="block in sortedBlocks" :key="block.order"
      :class="{ 'matched-block': block.id === lockmun }">
      <h3 v-if="block.id === lockmun" class="typing-indicator" style="text-align: center;">
        Other people is typing! 
      </h3>
      <builder-block :block="block" />
      <line-base class="light"></line-base>
      <button-base class="tertiary min" :icon="'fas fa-plus fa-sm'" :title="$t('workSpace.addNewBlock')"
        @buttonPress="$store.commit('insertNewBlock', { order: block.order + 1 })"
        :disabled="block.id === lockmun"></button-base>
      <line-base class="light"></line-base>
    </div>


  </div>

  <!-- Flow view -->
  <div v-else class="work-space">
    <div class="survey-title">
      <h1>{{ surveyTitle }}</h1>
      <el-button id="preview_btn" type="primary" @click="showPreview()">{{
        $t('workSpace.preview')
      }}</el-button>
      <el-button id="save_btn" type="success">{{
        $t('workSpace.save')
      }}</el-button>
    </div>
    <line-base class="light"></line-base>

    <the-flow-editor />
  </div>
</template>

<script>
import SurveyServices from '../../services/SurveyServices'
import BuilderBlock from './BuilderBlock.vue'
import ButtonBase from '../../components/ButtonBase.vue'
import LineBase from './LineBase.vue'
import store from '../../store/SurveyBuilder'

import { mapGetters } from 'vuex'
import TheFlowEditor from './TheFlowEditor.vue'

export default {
  name: 'TheWorkSpace',
  store: store,
  components: {
    LineBase,
    ButtonBase,
    BuilderBlock,
    TheFlowEditor,
  },
  data() {
    return {
      lockmun: null,
      settimeoutobj: null
    }
  },
  computed: {
    ...mapGetters(['surveyTitle', 'editorData', 'sortedBlocks', 'flowView']),
    lockSocket() {
      return store.state.locksocket;
    }
  },
  watch: {
    lockSocket: {
      handler(newSocket) {
        console.log('触发watch');
        if (newSocket) {
          newSocket.onmessage = (event) => {
            // 处理从后端接收到的消息
            console.log('后端传来广播Received message:', JSON.parse(event.data));
            this.lockmun = Number(JSON.parse(event.data).locknum)
          };
        }
      },
      immediate: true // 在组件加载时立即执行一次逻辑
    },
    lockmun(newvalue) {
      if (newvalue != 9999) {
        if (this.settimeoutobj) {
          clearTimeout(this.settimeoutobj)
        }
        this.settimeoutobj = setTimeout(() => {
          this.lockmun = 9999
        }, 2400000);
      }
    }
  },
  methods: {
    /**
     * Update survey title and send to backend
     * @param e - event
     */

    async handleTitleInput(e) {
      var title = e.target.innerHTML
        .replaceAll('<br>', '')
        .replaceAll('&amp', '')
        .replaceAll('&lt', '')
        .replaceAll('&gt', '')
        .replaceAll('nbsp', '')
        .replaceAll(';', '')
      console.log(title)
      store.commit('updateSurveyTitle', title)

      // Really shouldn't hardcode which survey it is
      await SurveyServices.patchSurvey(store.state.survey.id, {
        name: title,
      })
    },

    showPreview() {
      let id = store.state.survey.id
      window.open(`/preview/${id}`, '_blank')
    },

    saveSurvey() {
      this.$message({
        message: 'Save successfully',
        type: 'success',
      })
    },
  },
}
</script>

<style scoped>
html:lang(ur) * {
  text-align: right;
}

.work-space {
  background-color: #eff2f5;
  width: 100%;
  min-height: calc(100vh - 56px);
  overflow: scroll;

  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  padding: 16px;
  align-items: center;
}

.button-row {
  padding: 8px 8px 0px 8px;
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.matched-block {
  position: relative!important ;
  opacity: 0.3 !important;
  pointer-events: none;
}

/* .matched-block::before {
  content: "lock";
} */

#title {
  color: black;
  padding: 0 8px;
  font-family: Arial, Helvetica, sans-serif;
  font-style: normal;
  font-weight: bold;
  font-size: 24px;
  text-align: left;
  max-width: 800px;
  display: flex;
  -webkit-user-modify: read-write-plaintext-only;
  -moz-user-modify: read-write-plaintext-only;
}

.survey-title:hover>*[contenteditable='true'],
.survey-title:focus>*[contenteditable='true'] {
  background-color: white;
  outline: 0;
}

.survey-title>*[contenteditable='true'] {
  padding: 8px;
  border: 2px solid white;
  border-radius: 4px;
}

.text-with-button {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
  align-content: center;
}

.survey-title {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.typing-indicator {
  color: red;
  position: absolute;
  top: 100px;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 999999999999;
}


.block-segment {
  display: flex;
  flex-direction: column;
  justify-content: center;
  max-width: 816px;
  /* min-width: 816px; */
  margin: 0 auto;
}

.el-button--primary {
  background: #204cdc !important;
  border-color: #204cdc !important;
  color: #e7f2fe;
}

.el-button--primary:hover {
  background: #5976d5 !important;
  border-color: #5976d5 !important;
  color: #ffffff !important;
}

/*PC device*/
@media only screen and (min-width: 992px) {
  #preview_btn {
    position: absolute;
    right: 2%;
    top: 100px;
    width: 5%;
    font-size: small;
    z-index: 1;
  }
  #save_btn {
    position: absolute;
    right: 2%;
    top: 160px;
    width: 5%;
    font-size: small;
    z-index: 1;
  }
}

/*mobile*/
@media only screen and (max-width: 767px) {
  #preview_btn {
    position: absolute;
    right: 2%;
    top: 3rem;
    /*width: 5%;*/
    font-size: small;
    z-index: 1;
    margin-right: 5rem;
    /*margin-bottom: 15rem;*/
  }
  #save_btn {
    position: absolute;
    right: 2%;
    top: 3rem;
    /*width: 5%;*/
    font-size: small;
    z-index: 1;
  }
}
</style>
