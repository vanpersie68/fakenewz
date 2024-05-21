<template>
  <div>
    <label class="switch">
      <input type="checkbox" @click="handleToggle" v-model="toggleValue" />
      <span class="slider"></span>
    </label>
  </div>
</template>

<script>
export default {
  name: 'ToggleBase',
  props: {
    toggled: Boolean,
  },
  methods: {
    /**
     * Pass toggle state to parent component
     */
    handleToggle() {
      this.$emit('handleToggle')
    },
  },
  computed: {
    toggleValue: {
      get: function () {
        return this.toggled == true
      },
      set: function () {},
    },
  },
}
</script>

<style scoped>
.switch {
  position: relative;
  display: inline-block;
  width: 56px;
  height: 32px;
  margin: 8px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #566370;
  -webkit-transition: 0.4s;
  transition: 0.4s;
  border-radius: 34px;
}

.slider:before {
  position: absolute;
  content: '';
  height: 24px;
  width: 24px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: 0.2s;
  transition: 0.2s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #1947e5;
}

input:checked + .slider:before {
  -webkit-transform: translateX(24px);
  -ms-transform: translateX(24px);
  transform: translateX(24px);
}
</style>
