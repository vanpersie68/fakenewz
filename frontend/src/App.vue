<script>
import TheNavBar2 from './components/TheNavBar2'
import TheFooter from './components/TheFooter'
import TheNavBar from './components/TheNavBar'

export default {
  components: {
    TheFooter,
    TheNavBar,
    TheNavBar2,
  },
}
</script>

<template>
  <body>
    <div id="app">
      <TheNavBar2 v-if="$route.name === 'surveytaker'"></TheNavBar2>
      <TheNavBar
        v-if="$route.name !== 'surveytaker' && $route.name !== 'Success'"
      ></TheNavBar>
      <div id="router-wrapper"><router-view /></div>
      <the-footer
        v-if="
          $route.name !== 'Survey Builder' &&
          $route.name !== 'surveytaker' &&
          $route.name !== 'Success'
        "
      />
    </div>
  </body>
</template>

<style scoped>
#app {
  font-family: sans-serif;
  display: flex;
  height: 100vh;
  max-height: 100vh;
  flex-direction: column;
}

#router-wrapper {
  flex: 2;
}
</style>
<style>
.el-dialog__body {
  word-break: normal;
}
h1,
h2 {
  font-weight: 300;
}
</style>
