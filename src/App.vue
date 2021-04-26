<template>
  <div id="app" >
    <FormPage :config="config" />
  </div>
</template>

<script>

import FormPage from './components/FormPage.vue'
// import axios from 'axios';

export default {
  name: 'App',
  components: {
    FormPage,
  },
  data () {
    return {
      config:null
   
    }
  },
  mounted: function () {
    console.log("Mounted: App")
  }
}
</script>

<style>
#app {
  /* font-family: Avenir, Helvetica, Arial, sans-serif; */
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  /* color: #2c3e50; */
  /* margin-top: 60px; */
}
</style>
