<template>
  <div id="app" class="min-vh-100 vh-100 p-0 d-flex flex-column ">
    <div class="d-flex">
        <NavBar :config="navbar_config" v-if="config.output || config.socket">
          <template #navbar_input v-if="config.input">
            <button 
              class="btn btn-outline-light rounded-0 mr-2"
              :class="visible.input ? 'active' : ''" 
              @click="visible_handler('input')" 
              >Input
            </button>
          </template>
          <template #navbar_output v-if="config.output">
            <button 
              class="btn btn-outline-light rounded-0 mr-2"
              :class="visible.output ? 'active' : ''" 
              @click="visible_handler('output')" 
              >Output
            </button>
          </template>
          <template #navbar_socket v-if="config.socket">
            <button 
              class="btn btn-outline-light rounded-0 mr-2"
              :class="visible.socket ? 'active' : ''" 
              @click="visible_handler('socket')" 
              >Socket
            </button>
          </template>
        </NavBar>
    </div>
    <div class="d-flex flex-fill">
      <Input ref="ref_input" v-if="config.input" v-show="visible.input" :config="config.input" :test123="'teet'">
        <template #footer="slotProps">
          <button type="button" class="btn btn-outline-primary " @click="submit(slotProps.footer)">Submit</button>
        </template>
      </Input>
      <Output ref="ref_output" v-if="config.output" :visible="visible.output" :config="config.output" :json="output_json"/>
      <Socket ref="ref_socket" v-if="config.socket" :visible="visible.socket" :config="config.socket"/>
    </div>





  </div>
</template>

<script>

import NavBar from './components/NavBar.vue'
import Input from './components/Input.vue'
import Output from './components/Output.vue'
import Socket from './components/Socket.vue'
import axios from 'axios';


export default {
  name: 'App',
  components: {
    NavBar,Input,Output,Socket
  },
  data () {
    return {
      config: {},
      navbar_config: { },
      output_json: null,
      socket_data: null,
      visible: {
        "input": true,
        "output": false,
        "socket": false
      }

    }
  },
  methods:{
    submit: async function (json){

      let url = this.config.input.submit_url

      try {
        let output = await axios.post(url,json)
        if (output.status == 200){
          this.output_json = output.data
          console.log("POST SUCCESSFUL TO",url,"output.data")
        }else{
          this.output_json = "Failed with code " + String(url) + " to " + url
          console.log(this.output_json)
        }

      } catch (error) {
          this.output_json = "Error to " + url + "\n" + String(error)  
          console.log(this.output_json)
      }
   
    },
    visible_handler: function (name){
      for (const key in this.visible) {
        if (Object.hasOwnProperty.call(this.visible, key)) {
          this.visible[key]= false
        }
      }
      this.visible[name]= true
    },
    getConfig: async function(){
      let output = await axios.get("config.json")
      if (output.status == 200 && typeof output.data == 'object'){
        this.config = output.data
      }else{
        console.log("POST FAILED WITH OTHER THAN 200")
        this.config = {}
      }

    },
    calc: function(val){
      return val*4
    }


  },
  mounted: function () {
    this.getConfig()

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

