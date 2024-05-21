<template>
  <!-- <button v-if="icon" class="btn" @click="buttonPress" @blur="buttonUnfocus">
      <i class="fas fa-phone fa-me"></i>
      fas fa-phone fa-sm
    </button> -->
  <button
    style="width: auto"
    v-if="icon != null"
    class="btn"
    @click="buttonPress"
    @blur="buttonUnfocus"
    @mousedown="mousedown"
    :class="title != null ? 'withText' : ''"
  >
    <i :class="icon" :title="hover"> {{ title }}</i>
  </button>
  <button
    v-else
    class="btn"
    @click="buttonPress"
    @blur="buttonUnfocus"
    @mousedown="mousedown"
  >
    {{ title }}
  </button>
</template>

<script>
export default {
  name: 'ButtonBase',
  props: {
    title: String,
    icon: String,
    hover: String,
  },
  methods: {
    /**
     * Handle button being clicked
     */
    buttonPress(data) {
      this.$emit('buttonPress', data)
    },
    /**
     * Handle button being unfocused
     */
    buttonUnfocus() {
      this.$emit('buttonUnfocus')
    },
    /**
     * Handle button press down by mouse
     */
    mousedown() {
      this.$emit('mousedown')
    },
  },
}
</script>

<style scoped>
/*

Class naming conventions:

class="{primary / secondary / tertiary / alternate} {standard / min / square}"

*/

.btn {
  font-family: Arial, Helvetica, sans-serif;
  font-style: normal;
  font-weight: bold;
  display: flex;
  align-items: center;
  text-align: center;
  border-radius: 8px;
  margin: 8px;
  font-size: 16px;
  border-width: 2px;
  border-style: solid;
  align-self: center;
  cursor: pointer;
}

.btn:focus {
  outline: 0;
  border-radius: 8px;
}

.withText {
  gap: 16px;
}

/* Sized styling */

.standard {
  height: 48px;
  padding: 13px 26px;
}

.min {
  padding: 0px 6px;
  min-height: 32px;
}

.square {
  margin: 8px;
  min-width: 48px;
  min-height: 48px;
  height: 48px;
  width: 48px;
  justify-content: space-around;
}

/* Primary color styling */

.primary {
  border-color: #e4f2ff;
  background-color: #e4f2ff;
  color: #1947e5;
}

.primary:focus {
  outline: 0;
  border-radius: 8px;
  border: 2px solid #1947e5;
  box-shadow: 0 0 4px 0px #1947e5;
}

.primary:active,
.primary.selected {
  background-color: #1947e5;
  color: white;
  border: 2px solid #1947e5;
}

.primary:hover,
.primary:active.hover {
  border: 2px solid #1947e5;
}

.primary.selected:hover {
  background-color: #002dc8;
  border: 2px solid #002dc8;
}

/* Secondary color styling */

.secondary {
  border-color: #eff2f5;
  background-color: #eff2f5;
  color: #566370;
}

.secondary:focus {
  border: 2px solid #566370;
  box-shadow: 0 0 4px 0px #566370;
}

.secondary:active {
  background-color: #566370;
  color: white;
  border: 2px solid #566370;
}

.secondary:hover,
.secondary:active.hover {
  border: 2px solid #566370;
}

/* Tertiary color styling */

.tertiary {
  border-color: #566370;
  background-color: white;
  color: #566370;
}

.tertiary:focus {
  box-shadow: 0 0 4px 0px #566370;
}

.tertiary:active,
.tertiary:active:hover {
  background-color: #566370;
  color: white;
  border: 2px solid #566370;
}

.tertiary:hover {
  background-color: #d7e0e5;
}

/* Alternate color styling - only used on light grey backgrounds */

.alternate {
  border-color: white;
  background-color: #566370;
  color: white;
}

.alternate:focus {
  box-shadow: 0 0 4px 0px white;
}

.alternate:active,
.alternate:active:hover {
  color: #566370;
  background-color: #eff2f5;
  border: 2px solid #eff2f5;
}

.alternate:hover {
  color: #566370;
  background-color: white;
}

/* Alternate color styling - only used on light grey backgrounds */

.destructive {
  border-color: #ffe4e4;
  background-color: #ffe4e4;
  color: #e51919;
}

.destructive:focus {
  outline: 0;
  border-radius: 8px;
  border: 2px solid #e51919;
  box-shadow: 0 0 4px 0px #e51919;
}

.destructive:active,
.destructive.selected {
  background-color: #e51919;
  color: white;
  border: 2px solid #e51919;
}

.destructive:hover,
.destructive:active.hover {
  border: 2px solid #e51919;
}

.destructive.selected:hover {
  background-color: #c80000;
  border: 2px solid #c80000;
}

/* Purple color styling - only used on light grey backgrounds */

.purple {
  border-color: #f5e4ff;
  background-color: #f5e4ff;
  color: #9719e5;
}

.purple:focus {
  outline: 0;
  border-radius: 8px;
  border: 2px solid #9719e5;
  box-shadow: 0 0 4px 0px #9719e5;
}

.purple:active,
.purple.selected {
  background-color: #9719e5;
  color: white;
  border: 2px solid #9719e5;
}

.purple:hover,
.purple:active.hover {
  border: 2px solid #9719e5;
}

.purple.selected:hover {
  background-color: #7000c8;
  border: 2px solid #7000c8;
}

/* Color specific styling */

.red {
  color: red;
}
</style>
