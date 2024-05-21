<template>
  <el-select
    v-model="value"
    popper-class="select-popper"
    :popper-append-to-body="true"
    @change="selectedIcon"
    placeholder="Icons"
  >
    <el-row v-for="(item, index) in icons" :key="index">
      <el-col v-if="index % 2 == 1" :span="12">
        <el-option
          :label="icons[index - 1].label"
          :value="icons[index - 1].value"
        >
          <el-link :underline="false" v-bind:icon="icons[index - 1].value">{{
            icons[index - 1].label
          }}</el-link>
        </el-option>
      </el-col>

      <el-col
        v-if="index % 2 == 1 || (index % 2 == 0 && index == icons.length - 1)"
        :span="12"
      >
        <el-option :label="icons[index].label" :value="icons[index].value">
          <el-link :underline="false" v-bind:icon="icons[index].value">{{
            icons[index].label
          }}</el-link>
        </el-option>
      </el-col>
    </el-row>
  </el-select>
</template>

<script>
import iconList from '@/store/iconList'

export default {
  props: ['index', 'iconShow'],
  name: 'SelectIcons',
  data() {
    return {
      icons: iconList.iconList,
      value: '',
    }
  },
  mounted() {
    this.value = this.iconShow
  },
  methods: {
    selectedIcon(iconName) {
      this.$emit('selected', iconName, this.index)
    },
  },
}
</script>

<style lang="scss" scoped>
//定位每一个图标
.select-popper .el-select-dropdown__item {
  opacity: 0.618;
  width: auto;
}
</style>
