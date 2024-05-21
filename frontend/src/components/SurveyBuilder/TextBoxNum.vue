<template>
  <div class="button-row">
    <button-base
      class="primary square"
      :icon="'fas fa-minus fa-me'"
      @buttonPress="decrement"
    />
    <p>{{ compQuery }}</p>
    <button-base
      class="primary square"
      :icon="'fas fa-plus fa-me'"
      @buttonPress="increment"
      style="margin-right: 6px"
    />
  </div>
</template>

<script>
import ButtonBase from '../../components/ButtonBase.vue'
export default {
  components: { ButtonBase },
  name: 'TextBoxNum',
  data() {
    return {
      query: this.value,
    }
  },
  props: {
    placeholder: String,
    initialValue: String,
    value: String,
  },
  methods: {
    /**
     * Update the text box number
     */
    update: async function () {
      await this.$emit('update', parseInt(this.query))
      this.query = this.value
    },
    /**
     * Increment the text box number
     */
    increment: async function () {
      await this.$emit('increment')
      this.query = this.value
    },
    /**
     * Decrement the text box number
     */
    decrement: async function () {
      await this.$emit('decrement')
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

<style scoped>
html:lang(ur) * {
  text-align: right;
}

p {
  /* padding: 0; */
  height: 48px;
  width: 50%;
  box-sizing: border-box;
  position: relative;
  left: 0;
  outline: none;
  background-color: #eff2f5;
  font-size: 16px;
  font-weight: bolder;
  text-align: center;

  padding: 8px;
  border: 2px solid #eff2f5;
  border-radius: 4px;
}

.button-row {
  padding: 8px 16px;
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  align-items: center;
}
</style>
