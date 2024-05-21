<template>
  <div>
    <textarea
      v-model="query"
      name="query"
      :placeholder="placeholder"
      @blur="submitInput"
    />
  </div>
</template>

<script>
export default {
  name: 'TextArea',
  data() {
    return {
      query: this.block == null ? '' : this.block.description,
    }
  },
  props: {
    placeholder: String,
    block: Object,
  },
  methods: {
    /**
     * Handle text area input
     */
    submitInput() {
      this.$emit('handleInput', this.query)
    },
  },
}
</script>

<style scoped>
html:lang(ur) * {
  text-align: right;
}

textarea {
  min-height: 36px;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  resize: vertical;
  position: relative;
  outline: none;
  background-color: white;
  font-size: 16px;

  padding: 8px;
  border: 2px solid #eff2f5;
  border-radius: 4px;
  font-family: Arial, Helvetica, sans-serif;
  font-style: normal;
}
</style>
