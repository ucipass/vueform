<template>
  <div id="app" class="min-vh-100 vh-100 p-0 d-flex flex-column ">
    <div class="d-flex">
        <NavBar ref="navbar" :config="navbar_config" >
        </NavBar>
    </div>
    <div class="d-flex flex-fill">
      <PostMan   ref="postman"   v-if="config.input  && false"   :visible="$refs.navbar.navbar.PostMan"    :config="config.input" />
      <SocketMan ref="socketman" v-if="config.socket && false"   :visible="$refs.navbar.navbar.SocketMan"  :config="config.socket"/>
      <SSHClient ref="socketman" v-if="config.socket"   :visible="$refs.navbar.navbar.SSHClient"  :config="config.socket"/>
    </div>

  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'
import PostMan from './components/PostMan.vue'
import SocketMan from './components/SocketMan.vue'
import SSHClient from './components/SSHClient.vue'
import axios from 'axios';

export default {
  name: 'App',
  components: { NavBar,PostMan,SocketMan,SSHClient },
  data () {
    return {
      config: {},
      navbar_config: {
        // "PostMan": false,
        // "SocketMan": false,
        "SSHClient": true,
        "Settings": false
      }
    }
  },
  methods:{
  },
  mounted: async function () {
      try {
        let output = await axios.get("config.json")
        this.config = output.data
      } catch (error) {
        console.log("Error: Unable to fetch config.json from server!!")
        this.config = {}        
      }
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

