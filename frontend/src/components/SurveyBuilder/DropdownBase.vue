/* USAGE:

<dropdown-base :options="['option 1', 'option 2', 'option 3']" />

*/

<template>
  <div class="custom-select">
    <div class="selected" :class="{ open: open }" @click="open = !open">
      <div class="text">
        {{ $t('builderBlock.'+currentType.toString().replace(/\s/g, "")) }}
      </div>

      <i v-if="!open" class="fas fa-chevron-down fa-lg icon"></i>
      <i v-else class="fas fa-chevron-up fa-lg icon"></i>
    </div>
    <div class="items" :class="{ selectHide: !open }">
      <div
        v-for="(option, i) of options"
        :key="i"
        @click="handleSelection(options, i)"
       >
        <i v-if="icons != null && isHab(icons[i])" :class="icons[i] + ' fa-me icon'"></i>
          <svg-icon v-else :icon-class="icons[i]" />
        {{ $t('builderBlock.'+option.toString().replace(/\s/g, "")) }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DropdownBase',
  props: {
    options: Array,
    icons: Array,
    currentType: String,
  },
  data() {
    return {
      selected:
        this.currentType != null
          ? this.currentType
          : this.options != null && this.options.length > 0
          ? this.options[0]
          : null,
      open: false,
    }
  },
  methods: {
  isHab(name){
  if(name){
  return name.indexOf('fa')==0
  }else {
   return false
  }

  },
    /**
     * Handle dropdown option being selected
     */
    handleSelection(options, i) {
      this.selected = options[i]
      this.open = false
      this.$emit('input', options[i])
    },
  },
}
</script>

<style scoped>
/* Text styling */
.selected,
.items {
  font-family: Arial, Helvetica, sans-serif;
  font-style: normal;
  font-size: 16px;
}

.selected {
  font-weight: bold;
}

.items {
  font-weight: normal;
}

/* Other styling */
.custom-select {
  position: relative;
  width: calc(100% - 16px);
  text-align: left;
  outline: none;
  height: 40px;
  line-height: 40px;
  margin: 16px 8px;
  z-index: 10;
}

.selected {
  background-color: #eff2f5;
  border-radius: 6px;
  border: 2px solid #eff2f5;
  color: #566370;
  padding-left: 1em;
  cursor: pointer;
  user-select: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 0 0 8px;
}

.text,
.custom-select .items div {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}

.icon {
  text-align: center;
  width: 40px;
}

.selected:hover {
  background-color: #e4f2ff;
  border: 2px solid #e4f2ff;
}

.custom-select .selected.open {
  border-radius: 6px 6px 0px 0px;
  border: 2px solid #1947e5;
  background-color: #e4f2ff;
}

.custom-select .items {
  color: #eff2f5;
  border-radius: 0px 0px 6px 6px;
  overflow: hidden;
  background-color: #eff2f5;
  left: 0;
  right: 0;
  z-index: 0;
  border: 2px solid #1947e5;
  border-top: 1px solid #eff2f5;
}

.custom-select .items div {
  color: #566370;
  padding: 0 8px;
  cursor: pointer;
  border: 2px solid #eff2f5;
  user-select: none;
}

.custom-select .items div:hover {
  background-color: #1947e5;
  color: white;
}

.selectHide {
  display: none;
}
</style>
