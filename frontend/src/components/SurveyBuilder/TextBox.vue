<template>
  <div>
    <input
      type="text"
      v-model="compQuery"
      name="query"
      :placeholder="placeholder"
      @input="input"
      :class="styleClass"
    />
  </div>
</template>

<script>
export default {
  name: 'TextBox',
  data() {
    this.compQuery = this.value
    return {
      query: this.value,
    }
  },
  props: {
    placeholder: String,
    value: String,
    styleClass: String,
  },
  methods: {
    /**
     * Handle and save textbox input
     */
    input: async function () {
      await this.$emit('input', this.query)
      this.query = this.value
    },
  },
  computed: {
    compQuery: {
      get() {
        return this.query
      },
      set(newValue) {
        this.query = newValue
      },
    },
  },
}
</script>

<style scoped></style>
