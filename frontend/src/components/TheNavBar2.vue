<template>
  <nav>
    <p id="title">{{ $t('fakenewz Survey Platform') }}</p>
    <lang-drop-down />
  </nav>
</template>

<script>
import LangDropDown from './LangDropDown.vue'
import ButtonBase from '../components/ButtonBase.vue'
export default {
  name: 'TheNavBar2',
  components: {
    LangDropDown,
    ButtonBase,
  },
}
</script>

<style scoped>
nav {
  margin-top: 0px;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  max-height: 56px;
  min-height: 56px;
  background-color: #566370;

  position: sticky;
  top: 0;
  z-index: 100;
}

#title {
  flex-grow: 2;
  margin-left: 20px;
  color: #fff;
}
</style>
