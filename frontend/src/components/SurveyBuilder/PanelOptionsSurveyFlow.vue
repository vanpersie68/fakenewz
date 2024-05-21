<template>
  <div class="options">
    <div class="text-with-button">
      <h2>{{ $t('pOptionsFlow.showFlow') }}</h2>
      <toggle-base
        :toggled="flowView"
        @handleToggle="
          $store.commit('toggle', { parent: editorData, key: 'flowView' })
        "
      ></toggle-base>
    </div>
    <line-base class="dark" />
    <!-- <h3>Randomised sections</h3>
    <button-base class="purple standard" :icon="'fas fa-plus fa-me'" :title="'Add a randomised section'" style="margin: 0 auto 16px;"/>

    <line-base class="light" />

    <h2>Section 1:</h2>

    <ul>
      <li>
          <h4>Block 1: The block name (2Qs)</h4>
          <button-base class="destructive square" :icon="'fas fa-trash fa-lg'"/>
      </li>
      <li>Block 1</li>
      <li>Block 1</li>
    </ul>
    <line-base class="light" /> -->
  </div>
</template>

<script>
import LineBase from './LineBase.vue'
import TextBoxNum from './TextBoxNum.vue'
import ToggleBase from './ToggleBase.vue'
import store from '../../store/SurveyBuilder.js'
import { mapGetters } from 'vuex'
import ButtonBase from '../../components/ButtonBase.vue'

export default {
  name: 'PanelOptionsSurveyFlow',
  store: store,
  components: {
    LineBase,
    TextBoxNum,
    ToggleBase,
    ButtonBase,
  },
  computed: {
    ...mapGetters(['flowView', 'editorData']),
  },
}
</script>

<style scoped>
html:lang(ur) * {
  text-align: right;
}

h1,
h2 {
  color: black;
  padding: 0 16px;
  font-family: Arial, Helvetica, sans-serif;
  font-style: normal;
  text-align: left;
}

h1 {
  font-size: 16px;
  font-weight: bold;
  padding: 16px;
}

h2 {
  font-size: 16px;
  font-weight: bold;
}

.text-with-button {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
  align-content: center;
}

ul {
  padding: 0 8px;
}

li {
  display: flex;
  list-style-type: none;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  margin: 0 0 8px 0;
  border: 2px solid #eff2f5;
  /* border: 2px solid #F5E4FF; */
  /* background-color: #F5E4FF; */
  padding-left: 8px;
  border-radius: 8px;
}
</style>
