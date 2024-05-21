f<template>
  <div
    class="question"
    :class="isActiveQuestion ? 'active' : ''"
    @click="handleQuestionClick"
    id="builder"
  >
    <div class="question-header">
      <div class="question-titles">
        <h1>
          Q{{ question.order }}
          <span class="required" v-if="question.required">*</span>
        </h1>
        <input
          type="text"
          v-model="question.title"
          @blur="updateQuestionTitle"
          class="question-title h2-tb"
          :style="
            $i18n.locale === 'ur' ? 'text-align: right;' : 'text-align: left;'
          "
        />
      </div>
      <div class="opt-container">
        <div
          class="popup"
          :style="$i18n.locale === 'ur' ? 'left: 0px;' : 'right: 0px;'"
          :class="questionOptions ? 'show below' : ''"
        >
          <h3>{{ $t('builderQuestion.questionOptions') }}</h3>
          <line-base class="dark" />
          <ul>
            <li>
              <button-base
                class="secondary min"
                :icon="'fas fa-clone fa-me'"
                :title="$t('builderQuestion.duplicateQuestion')"
                @mousedown="
                  $store.commit('duplicateQuestion', {
                    block: block,
                    question: question,
                  })
                "
              />
            </li>
            <line-base class="dark" />
            <li>
              <button-base
                class="secondary min red"
                :title="$t('builderQuestion.deleteQuestion')"
                :icon="'fas fa-trash fa-me'"
                @mousedown="deleteQuestionFunc"
              />
            </li>
          </ul>
        </div>
        <button-base
          class="secondary square"
          :icon="'fas fa-ellipsis-h fa-lg'"
          @buttonPress="pressQuestionOptions"
          @buttonUnfocus="unfocusQuestionOptions"
        />
      </div>
    </div>

    <line-base class="light"></line-base>

    <h2 class="subtitle">
      {{ $t('builderQuestion.questionType') }}: {{ $t('builderBlock.'+question.type.toString().replace(/\s/g, "")) }}
    </h2>
    <line-base class="light"></line-base>

    <!-- NEWS POST QUESTION -->
    <question-content-articles
      v-if="question.type === 'News post'"
      :data="question"
    />

    <!-- TEXT ENTRY QUESTION -->
    <div v-if="question.type === 'Text entry'" class="question-content">
      <el-button
        type="primary"
        style="cursor: pointer"
        :onclick="
          'document.getElementById(\'question_' + question.id + '\').click()'
        "
      >
        {{ $t('builderBlock.uploadImage') }}
      </el-button>
      <el-button
        type="info"
        style="cursor: pointer"
        @click="cleanPhoto(question)"
      >
        {{ $t('g5.cancel') }}
      </el-button>
      <input
        :id="'question_' + question.id"
        @change="uploadPhoto($event, question)"
        type="file"
        style="display: none"
        accept=".jpg,.jpeg,.png,.JPG,.JPEG"
      />
      <div style="width: 100%; text-align: center">
        <br />
        <img :src="question.image" alt="" style="width: 500px" />
      </div>
      <br />
      <h2>{{ $t('builderQuestion.textEntryPlaceholder') }}</h2>
      <input
        type="text"
        v-model="question.query"
        @blur="inputTextboxQuestion"
      />
    </div>

    <!-- BUTTON ROW QUESTION -->
    <div v-if="question.type === 'Button row'" class="question-content">
      <el-button
        type="primary"
        style="cursor: pointer"
        :onclick="
          'document.getElementById(\'question_' + question.id + '\').click()'
        "
      >
        {{ $t('builderBlock.uploadImage') }}
      </el-button>
      <el-button
        type="info"
        style="cursor: pointer"
        @click="cleanPhoto(question)"
      >
        {{ $t('g5.cancel') }}
      </el-button>
      <input
        :id="'question_' + question.id"
        @change="uploadPhoto($event, question)"
        type="file"
        style="display: none"
        accept=".jpg,.jpeg,.png,.JPG,.JPEG"
      />
      <div style="width: 100%; text-align: center">
        <br />
        <img :src="question.image" alt="" style="width: 500px" />
      </div>
      <h2>{{ $t('builderQuestion.buttonContent') }}</h2>
      <div
        v-for="button in question.buttons"
        :key="question.buttons.indexOf(button)"
        class="question-titles"
      >
        <h1>{{ question.buttons.indexOf(button) + 1 }}.</h1>
        <input
          type="text"
          v-model="question.buttons[question.buttons.indexOf(button)].text"
          @blur="
            (input) =>
              inputTextboxButton(
                question.buttons[question.buttons.indexOf(button)]
              )
          "
        />
        <h2>{{ $t('builderQuestion.JumpBlock') }}</h2>
        <el-select
          v-model="
            question.buttons[question.buttons.indexOf(button)].jumpBlockId
          "
          placeholder=""
          @focus="getBlockList()"
          size="medium"
          filterable="true"
          @change="
            (input) =>
              inputTextboxButton(
                question.buttons[question.buttons.indexOf(button)]
              )
          "
        >
          <el-option
            v-for="item in jumpList"
            :key="item.id"
            :label="item.title"
            :value="item.id"
          >
          </el-option>
        </el-select>
      </div>
    </div>

    <!-- MULTIPLE CHOICE QUESTION -->
    <div v-if="question.type === 'Multiple choice'" class="question-content">
      <el-button
        type="primary"
        style="cursor: pointer"
        :onclick="
          'document.getElementById(\'question_' + question.id + '\').click()'
        "
      >
        {{ $t('builderBlock.uploadImage') }}
      </el-button>
      <el-button
        type="info"
        style="cursor: pointer"
        @click="cleanPhoto(question)"
      >
        {{ $t('g5.cancel') }}
      </el-button>
      <input
        :id="'question_' + question.id"
        @change="uploadPhoto($event, question)"
        type="file"
        style="display: none"
        accept=".jpg,.jpeg,.png,.JPG,.JPEG"
      />
      <div style="width: 100%; text-align: center">
        <br />
        <img :src="question.image" alt="" style="width: 500px" />
      </div>
      <h2>{{ $t('builderQuestion.multipleChoiceOptions') }}</h2>
      {{ choicesSort(question) }}
      <div
        v-for="choice in question.choices"
        :key="question.choices.indexOf(choice)"
        class="question-titles"
      >
        <h1>{{ question.choices.indexOf(choice) + 1 }}.</h1>
        <input
          type="text"
          style="width: 100%"
          v-model="question.choices[question.choices.indexOf(choice)].text"
          @blur="
            (input) =>
              inputTextboxMultichoice(
                question.choices[question.choices.indexOf(choice)]
              )
          "
        />
      </div>
      <div v-if="question.otherInput" class="question-titles">
        <h1>{{ question.choices.length + 1 }}.</h1>
        <input
          type="text"
          style="width: 100%"
          disabled
          :value="$t('builderQuestion.other')"
        />
      </div>
    </div>
    <div v-if="question.type === 'Matrix table'" class="question-content">
      <h2>{{ $t('builderQuestion.MatrixTableOptions') }}</h2>
      {{ choicesSort(question) }}
      <el-table
        ref="singleTable"
        :data="tableConfig"
        highlight-current-row
        style="width: 100%"
      >
        <el-table-column property="name"> </el-table-column>
        <el-table-column
          v-for="column in columnConfig"
          :key="column.value"
          :property="column.value"
          :label="column.label"
        >
          <template slot-scope="scope">
            <div>
              <!-- {{matrixChecked[scope.row.name + column.label]}} -->
              <el-checkbox
                :key="matrixChecked[scope.row.name + column.label]"
                :checked="matrixChecked[scope.row.name + column.label]"
                @change="
                  handleMatrixChange(scope.row.name, column.label, $event)
                "
              ></el-checkbox>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div
      v-if="question.type === 'Sliders'"
      class="question-content"
      @mousedown="sliderMousedown"
    >
      <h2>{{$t('pOptionsSliders.Sliders Options')}}</h2>
      {{ choicesSort(question) }}
      <el-table
        ref="singleTable"
        :data="tableConfig"
        :span-method="slidersSpanMethod"
        highlight-current-row
        style="width: 100%"
      >
        <el-table-column property="name"> </el-table-column>
        <el-table-column
          v-for="column in columnConfig"
          :key="column.value"
          :property="column.value"
          :label="column.label"
        >
          <template slot-scope="scope">
            <div style="height: 50px">
              <el-slider
                v-model="scope.row.sliderVal"
                :step="question.typedata.grid"
                :min="question.typedata.min"
                :max="question.typedata.max"
                :marks="marks"
                @change="sliderChange($event, scope)"
              ></el-slider>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div v-if="question.type === 'Groups'" class="question-content">
      <h2>{{$t('builderQuestion.Groups Options')}}</h2>
      {{ choicesSort(question) }}
      <div class="group-wrapper">
        <Container
          class="group-left"
          :should-animate-drop="(src, payload) => true"
          :get-child-payload="(itemIndex) => getChildPayload(itemIndex, 'root')"
          @drop="groupsDropFa($event)"
          :should-accept-drop="(src, payload) => true"
        >
          <p>{{ $t("surveyTaker.Items")}}</p>
          <Draggable
            v-for="item in tableConfig"
            :key="item.name"
            class="question-titles"
          >
            <div class="ques-item">{{ item.name }}</div>
          </Draggable>
        </Container>
        <div class="group-right">
          <Container
            v-for="(group, inx) in columnConfig"
            :key="group.value"
            class="group-item"
            @drop="groupsDrop(group, $event)"
            :should-accept-drop="(src, payload) => true"
            :should-animate-drop="(src, payload) => false"
            :get-child-payload="
              (itemIndex) => getChildPayloadChil(itemIndex, inx, 'chil')
            "
          >
            <p style="text-align: center">{{ group.label }}</p>

            <Draggable v-for="(item, i) in group.children" :key="item.name">
              <div class="ques-item">
                <span class="ques-item-idx">{{ i + 1 }}</span>
                {{ item.name }}
              </div>
            </Draggable>
          </Container>
        </div>
      </div>
    </div>

    <div v-if="question.type === 'Rank order'" class="question-content">
      <h2>{{ $t('builderQuestion.RankOrderOptions') }}</h2>
      {{ choicesSort(question) }}
      <Container @drop="onDrop(question, $event)">
        <Draggable
          v-for="choice in question.choices"
          :key="question.choices[question.choices.indexOf(choice)].id"
          class="question-titles"
        >
          <!-- <h1>{{ question.choices.indexOf(choice) + 1 }}.</h1> -->
          <input
            type="text"
            style="width: 100%"
            v-model="question.choices[question.choices.indexOf(choice)].text"
            @blur="
              (input) =>
                inputTextboxRankOrder(
                  question.choices[question.choices.indexOf(choice)]
                )
            "
          />
        </Draggable>
      </Container>

      <div v-if="question.otherInput" class="question-titles">
        <h1>{{ question.choices.length + 1 }}.</h1>
        <input
          type="text"
          style="width: 100%"
          disabled
          :value="$t('builderQuestion.other')"
        />
      </div>
    </div>

    <!-- Drag and Drop -->
    <div v-if="question.type === 'Drag and Drop'" class="question-content">
      <h2>{{ $t('builderQuestion.DnDChips') }}</h2>
      <div
        v-for="choice in question.choices"
        :key="question.choices.indexOf(choice) + ' Chip'"
        class="question-titles"
      >
        <h1>{{ question.choices.indexOf(choice) + 1 }}.</h1>

        <input
          type="text"
          style="width: 100%"
          v-model="question.choices[question.choices.indexOf(choice)].text"
          @unfocus="
            (input) =>
              $store.commit('updateValue', {
                parent: question.choices[question.choices.indexOf(choice)],
                key: 'text',
                value: input,
              })
          "
        />
      </div>

      <line-base class="light" />

      <h2>{{ $t('builderQuestion.DnDCategories') }}</h2>
      <div
        v-for="category in question.categories"
        :key="question.categories.indexOf(category)"
        class="question-titles"
      >
        <h1>{{ question.categories.indexOf(category) + 1 }}.</h1>

        <input
          type="text"
          style="width: 100%"
          v-model="
            question.categories[question.categories.indexOf(category)].text
          "
          @unfocus="
            (input) =>
              $store.commit('updateValue', {
                parent:
                  question.categories[question.categories.indexOf(category)],
                key: 'text',
                value: input,
              })
          "
        />
      </div>
    </div>

    <!-- NUMBER SCALE QUESTION -->
    <div v-if="question.type === 'Number scale'" class="question-content">
      <el-button
        type="primary"
        style="cursor: pointer"
        :onclick="
          'document.getElementById(\'question_' + question.id + '\').click()'
        "
      >
        {{ $t('builderBlock.uploadImage') }}
      </el-button>
      <el-button
        type="info"
        style="cursor: pointer"
        @click="cleanPhoto(question)"
      >
        {{ $t('g5.cancel') }}
      </el-button>
      <input
        :id="'question_' + question.id"
        @change="uploadPhoto($event, question)"
        type="file"
        style="display: none"
        accept=".jpg,.jpeg,.png,.JPG,.JPEG"
      />
      <div style="width: 100%; text-align: center">
        <br />
        <img :src="question.image" alt="" style="width: 500px" />
      </div>
      <div v-if="question.minTitleOn">
        <h2>{{ $t('builderQuestion.minTitle') }}</h2>

        <input
          type="text"
          v-model="question.minTitle"
          @blur="inputMinLabelNumberScale"
        />
      </div>
      <div v-if="question.midTitleOn">
        <h2>{{ $t('builderQuestion.midTitle') }}</h2>

        <input
          type="text"
          v-model="question.midTitle"
          @blur="inputMidLabelNumberScale"
        />
      </div>
      <div v-if="question.maxTitleOn">
        <h2>{{ $t('builderQuestion.maxTitle') }}</h2>

        <input
          type="text"
          v-model="question.maxTitle"
          @blur="inputMaxLabelNumberScale"
        />
      </div>
      <line-base
        class="light"
        v-if="question.minTitleOn || question.midTitleOn || question.maxTitleOn"
      />

      <h2 style="text-align: center">
        {{ $t('builderQuestion.livePreview') }}
      </h2>
      <div class="scale-labels" style="overflow: hidden">
        <p>{{ question.minTitleOn ? question.minTitle : '' }}</p>
        <p>{{ question.midTitleOn ? question.midTitle : '' }}</p>
        <p>{{ question.maxTitleOn ? question.maxTitle : '' }}</p>
      </div>
      <div class="scale-blocks" style="overflow-y: hidden">
        <div v-for="b in getScaleList()" :key="b" class="scale-block">
          <h1>{{ b }}</h1>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SurveyServices from '../../services/SurveyServices'

import ButtonBase from '../../components/ButtonBase.vue'
import LineBase from './LineBase.vue'
import TextBox from './TextBox.vue'
import QuestionContentArticles from './QuestionContentArticles.vue'
import { Container, Draggable } from 'vue-smooth-dnd'

import store from '../../store/SurveyBuilder.js'
import { mapGetters } from 'vuex'
import i18n from '@/i18n'

export default {
  name: 'BuilderQuestion',
  store: store,
  components: {
    ButtonBase,
    LineBase,
    TextBox,
    QuestionContentArticles,
    Container,
    Draggable,
  },
  props: {
    block: Object,
    blockOrder: Number,
    currentQuestion: Number,
    question: Object,
  },
  data: function () {
    return {
      questionOptions: false,
      jumpList: [],
      currentRow: null,
      matrixChecked: {},
    }
  },
  mounted() {
    this.getBlockList()
  },
  methods: {
    log(...a) {
      console.log(...a)
    },
    handleMatrixChange(s, c, e) {
      if (!this.question.multipleAnswers) {
        for (let k in this.matrixChecked) {
          if (k.includes(s)) {
            this.$set(this.matrixChecked, k, false)
          }
        }
      }
      this.$set(this.matrixChecked, s + c, e)
    },
    getChildPayload(itemIndex, type) {
      return { ...this.tableConfig[itemIndex - 1], type }
    },
    getChildPayloadChil(itemIndex, inx, type) {
      return {
        ...this.columnConfig[inx].children[itemIndex - 1],
        type,
        delIdx: itemIndex - 1,
      }
    },
    groupsDrop(group, e) {
      console.log(group, e)
      // if()
      if (e.payload.type === 'root') {
        if (e.addedIndex === null) return
        this.columnConfig[
          this.columnConfig.findIndex((el) => el.value === group.value)
        ].children.splice(e.addedIndex - 1, 0, e.payload)
        this.columnConfig = this.columnConfig
        // this.tableConfig.splice(this.tableConfig.findIndex(el => el.name === e.payload.name),1)
        // this.tableConfig = this.tableConfig
      } else {
        if (e.removedIndex !== null) {
          this.columnConfig[
            this.columnConfig.findIndex((el) => el.value === group.value)
          ].children.splice(e.removedIndex - 1, 1)
        }
        if (e.addedIndex !== null) {
          this.columnConfig[
            this.columnConfig.findIndex((el) => el.value === group.value)
          ].children.splice(e.addedIndex - 1, 0, e.payload)
        }
        this.columnConfig = this.columnConfig
      }
    },
    groupsDropFa(e) {
      console.log(e)
    },
    sliderMousedown(e) {
      e.stopPropagation()
    },
    sliderChange(e, s) {
      console.log(e, s)
    },
    slidersSpanMethod({ row, column, rowIndex, columnIndex }) {
      if (columnIndex === 0) {
        // return [0, 0];
      } else if (columnIndex === 1) {
        return [1, 500]
      }
    },
    setCurrent(row) {
      this.$refs.singleTable.setCurrentRow(row)
    },
    handleCurrentChange(val) {
      this.currentRow = val
    },
    onDrop(q, v) {
      let ch = [...q.choices]
      const obj = ch.splice(v.removedIndex, 1)
      ch.splice(v.addedIndex, 0, obj[0])
      console.log(ch, v)
      ch = ch.map((e, i) => {
        e.order = i + 1
        return e
      })
      ch.forEach((el) => {
        console.log(el)
        SurveyServices.patchRankOrderQuestion(this.question.typedata.id, {
          id: el.id,
          order: el.order,
          title: el.text,
        })
      })
      this.$set(this.question, 'choices', ch)
    },
    choicesSort(questionData) {
      let temp
      for (let i = 1; i < questionData.choices.length; i++) {
        for (let j = 0; j < questionData.choices.length - i; j++) {
          if (
            questionData.choices[j].order > questionData.choices[j + 1].order
          ) {
            temp = questionData.choices[j + 1]
            questionData.choices[j + 1] = questionData.choices[j]
            questionData.choices[j] = temp
          }
        }
      }
    },
    /**
     * Update and save question title
     */
    async updateQuestionTitle() {
      await SurveyServices.patchQuestion(this.question.id, {
        name: this.question.title,
      })
    },
    /**
     * Handle question being clicked
     */
    handleQuestionClick() {
      store.commit('handleQuestionClick', {
        questionOrder: this.question.order,
        blockOrder: this.blockOrder,
      })
    },
    /**
     * Delete a question from a block
     */
    deleteQuestionFunc() {
      store.commit('deleteQuestion', {
        block: this.block,
        question: this.question,
      })
    },
    /**
     * Display popup for question options
     */
    pressQuestionOptions() {
      this.questionOptions = !this.questionOptions
    },
    /**
     * Hide popup for question options
     */
    unfocusQuestionOptions() {
      this.questionOptions = false
    },
    /**
     * Save text entry question query
     */
    async inputTextboxQuestion() {
      await SurveyServices.patchQuestionType(this.question.id, {
        query: this.question.query,
      })
    },
    /**
     * Save min label number scale query
     */
    async inputMinLabelNumberScale() {
      store.commit('updateValue', {
        parent: this.question,
        key: 'minTitle',
        value: this.question.minTitle,
      })

      await SurveyServices.patchQuestionType(this.question.id, {
        minTitle: this.question.minTitle,
      })
    },
    /**
     * Save max label number scale query
     */
    async inputMaxLabelNumberScale() {
      store.commit('updateValue', {
        parent: this.question,
        key: 'maxTitle',
        value: this.question.maxTitle,
      })

      await SurveyServices.patchQuestionType(this.question.id, {
        maxTitle: this.question.maxTitle,
      })
    },
    /**
     * Save mid label number scale query
     */
    async inputMidLabelNumberScale() {
      store.commit('updateValue', {
        parent: this.question,
        key: 'midTitle',
        value: this.question.midTitle,
      })

      await SurveyServices.patchQuestionType(this.question.id, {
        middleTitle: this.question.midTitle,
      })
    },
    /**
     * Save multiple choice option text
     */
    async inputTextboxMultichoice(choice) {
      await SurveyServices.patchMultiChoiceQuestion(this.question.typedata.id, {
        id: choice.id,
        title:
          this.question.choices[this.question.choices.indexOf(choice)].text,
      })
    },
    async inputTextboxRankOrder(choice) {
      await SurveyServices.patchRankOrderQuestion(this.question.typedata.id, {
        id: choice.id,
        title:
          this.question.choices[this.question.choices.indexOf(choice)].text,
      })
    },
    /**
     * Save button text in button
     */
    async inputTextboxButton(button) {
      await SurveyServices.patchButtonRowQuestion(this.question.typedata.id, {
        id: button.id,
        buttonText:
          this.question.buttons[this.question.buttons.indexOf(button)].text,
        jumpBlockId:
          this.question.buttons[this.question.buttons.indexOf(button)]
            .jumpBlockId,
      })
    },
    async inputTerminatesButton(button) {
      store.commit('toggle', {
        parent: button,
        key: 'terminates',
      })

      console.log('Terminates: ', button.terminates)
      await SurveyServices.patchButtonRowQuestion(this.question.typedata.id, {
        id: button.id,
        goToEnd: button.terminates,
      })
    },
    /**
     * Create list for number scale
     * @returns number scale list
     */
    getScaleList() {
      let list = []
      for (
        let i = this.question.minNum;
        i <= this.question.maxNum;
        i += this.question.interval
      ) {
        list.push(i)
      }
      return list
    },
    getBlockList() {
      let blockList = [
        {
          id: 0,
          title: this.$t('builderQuestion.doNothing'),
        },
        {
          id: -1,
          title: this.$t('builderQuestion.endSurvey'),
        },
      ]
      let randomBlock = []
      this.$store.state.survey.randomSections.forEach(function (element) {
        for (let i = element.startWith; i <= element.endWith; i++) {
          randomBlock.push(i)
        }
      })
      let order = this.block.order
      this.$store.state.survey.editorData.blocks.forEach(function (element) {
        if (!randomBlock.includes(element.order) && element.order > order) {
          blockList.push({ id: element.id, title: element.title })
        }
      })
      this.jumpList = blockList
    },
    async uploadPhoto(e, question) {
      var file = e.target.files[0]
      var reader = new FileReader()
      reader.readAsDataURL(file)
      reader.onload = (e) => {
        var imgcode = e.target.result
        question.image = imgcode
        SurveyServices.patchQuestionImage(this.question.id, {
          image: imgcode,
        }).then(() => {
          this.$forceUpdate()
        })
      }
      this.$forceUpdate()
    },
    async cleanPhoto(question) {
      question.image = ''
      SurveyServices.patchQuestionImage(this.question.id, {
        image: '',
      })
    },
  },

  computed: {
    marks() {
      const obj = {}
      let min = this.question.typedata.min
      const max = this.question.typedata.max
      const grid = this.question.typedata.grid
      while (min <= max) {
        obj[min] = { label: min }
        min += grid
      }
      return obj
    },
    /**
     * Check if current question is selected
     * @returns true if is selected and false otherwise
     */
    isActiveQuestion: function () {
      if (this.currentQuestion == this.question.order) {
        return true
      }

      return false
    },
    columnConfig: {
      get() {
        return this.question.typedata.columnConfig
          ? JSON.parse(this.question.typedata.columnConfig)
          : []
      },
      set(val) {
        return (this.question.typedata.columnConfig = JSON.stringify(val))
      },
    },
    tableConfig: {
      get() {
        let data = this.question.typedata.tableConfig
          ? JSON.parse(this.question.typedata.tableConfig)
          : []
        data = data.filter(
          (el) =>
            !this.columnConfig.some(
              (el2) =>
                el2.children && el2.children.some((el3) => el3.name === el.name)
            )
        )
        return data
      },
      set(val) {
        return (this.question.typedata.tableConfig = JSON.stringify(val))
      },
    },
  },
}
</script>

<style scoped lang="scss">
@import './src/assets/textbox.scss';

html:lang(ur) * {
  text-align: right;
}

.custom-checkbox {
  display: inline-block;
  min-height: 36px;
  max-height: 36px;
  max-width: 36px;
  min-width: 36px;
  border-radius: 4px;
  text-align: center;
  font-size: 1em;
  border: 2px solid black;
  background: white;
  margin-right: 8px;
  padding: 0;
  color: green;
}

.scale-blocks,
.scale-labels {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  overflow: scroll;
}

.scale-block {
  text-align: center;
  background-color: #eff2f5;
  border-radius: 8px;
  margin: 2px;
  flex-grow: 1;
  justify-content: center;
  display: flex;
}

.subtitle {
  text-align: left;
  color: #566370;
}

.question {
  display: flex;
  flex-direction: column;
  background-color: white;
  margin: 8px;
  border-radius: 8px;
  border-width: 2px;
  border-style: solid;
  padding: 8px;
  border-color: #eff2f5;
}

.question:hover {
  border-color: #566370;
}

.active,
.question.active:hover {
  border-color: #1947e5;
}

h1,
h2 {
  color: black;
  padding: 0 0 0 8px;
  font-family: Arial, Helvetica, sans-serif;
  font-style: normal;
  font-weight: bold;
  text-align: left;
  margin-right: 8px;
}

h1 {
  font-size: 24px;
}

h2 {
  font-size: 16px;
}

.required {
  color: red;
}

.question-header {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}

.question-titles {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  white-space: nowrap;
}

.question-title {
  width: calc(100% - 100px);
  margin-right: 8px;
}

.button-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.question-titles:hover > *[contenteditable='true'],
.question-titles:focus > *[contenteditable='true'] {
  border: 2px solid #566370;
}

.question-titles > *[contenteditable='true'] {
  padding: 8px;
  border: 2px solid #eff2f5;
  border-radius: 4px;
}

/* Popup styling */
.opt-container {
  position: relative;
  display: flex;
  justify-content: right;
}

.popup {
  position: absolute;

  z-index: 2;
  display: none;

  width: 300px;
  margin: 0 auto;
  border: 2px solid #566370;
  border-radius: 8px;
  padding: 0 8px;
  background-color: #eff2f5;
}

.below {
  top: 62px;
}

.show {
  display: block;
}

.popup ul,
.popup ul li {
  list-style-type: none;
  margin: 0;
  padding: 0;
  align-items: center;
}

.popup ul li button {
  width: 100%;
  margin: 8px auto;
}

.popup h3 {
  text-align: left;
  padding: 0 8px;
}
.group-wrapper {
  display: flex;
}
.group-wrapper p {
  text-align: center;
}
.group-left {
  border: 1px solid #ccc;
  width: 300px;
  height: 100%;
  margin-right: 50px;
  border-radius: 5px;
  min-height: 314px;
}
.group-right {
  flex: 1;
}
.group-item {
  border: 1px solid #ccc;
  // display: flex;
  height: 150px;
  overflow-y: auto;
  margin-bottom: 12px;
  border-radius: 5px;
}
.group-item p {
  text-align: center;
  width: 100%;
}
.ques-item {
  padding: 6px 24px;
}
.ques-item-idx {
  background: #444;
  display: inline-block;
  color: #fff;
  height: 24px;
  border-radius: 12px;
  min-width: 28px;
  text-align: center;
  line-height: 24px;
  margin-right: 12px;
}
/* End of popup styling */
</style>
<style>
.el-slider__marks .el-slider__marks-text:last-of-type {
  width: 30px;
}
</style>
