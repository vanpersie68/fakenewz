<template>
  <div class="tool-bar">
    <p
      :class="currentPage === 'editor' ? 'tab current' : 'tab'"
      @click="handleTabClick('editor')"
    >
      {{ $t('toolBar.surveyEditor') }}
    </p>
    <p
      :class="currentPage === 'flow' ? 'tab current' : 'tab'"
      @click="handleTabClick('flow')"
    >
      {{ $t('toolBar.flowEditor') }}
    </p>
    <p
      :class="currentPage === 'settings' ? 'tab current' : 'tab'"
      @click="handleTabClick('settings')"
    >
      {{ $t('toolBar.surveySettings') }}
    </p>
    <p
      :class="currentPage === 'preview' ? 'tab current' : 'tab'"
      @click="handleTabClick('preview')"
    >
      {{ $t('toolBar.surveyPreview') }}
    </p>
  </div>
</template>

<script>
import store from '../../store/SurveyBuilder'

export default {
  name: 'TheToolBar',
  store: store,
  computed: {
    currentPage() {
      return store.getters['currentPage']
    },
  },
  methods: {
    /**
     * Handle user changing tabs in tool bar
     * @param {string} page - page selected by user
     */
    handleTabClick(page) {
      // If current page is reselected, change nothing
      if (page === this.currentPage) {
        return
      }

      console.log(page)
      // If new page is not a page, default to editor
      if (!['editor', 'flow', 'settings', 'preview'].includes(page)) {
        page = 'editor'
        console.log(page)
      }
      console.log(page)

      store.commit('handleTabClick', page)
    },
  },
}
</script>

<style scoped>
html:lang(ur) * {
  text-align: right;
}

.tool-bar {
  margin-top: 0px;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  height: 56px;
  background-color: white;
  border-bottom: 1px solid #566370;

  position: sticky;
  /* top: 56px; */
  z-index: 100;
}

.tab {
  color: #566370;
  padding: 16px;

  font-family: Arial, Helvetica, sans-serif;
  font-style: normal;
  font-weight: bold;
  font-size: 16px;
  line-height: 22px;

  cursor: pointer;
}

.current,
.current:active {
  color: #1947e5;
}

.tab:hover,
.tab:focus,
.tab:active {
  text-decoration: underline;
}
</style>
