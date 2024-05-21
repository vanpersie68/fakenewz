<template>
  <hr class="line" />
</template>

<script>
export default {
  name: 'LineBase',
}
</script>

<style scoped>
/* 

Class naming conventions: 

class="{light / dark}"

*/

.line {
  width: 100%;
  text-align: center;
  margin-block-start: 0;
  margin-block-end: 0;
  margin-inline-start: 0;
  margin-inline-end: 0;
  margin-top: 8px;
  margin-bottom: 8px;
  border-width: 0;

  border-top-style: solid;
  border-top-width: 1px;
}

/* Additional classes - to be passed in */

.light {
  border-top-color: #eff2f5;
}

.dark {
  border-top-color: #566370;
}
</style>
