<template>
  <div id="app" class="container">
    <NavBar :config="navbar_config">
      <template #navbar_input>
        <button 
          class="btn btn-outline-light rounded-0 mr-2"
          :class="visible.input ? 'active' : ''" 
          @click="visible_handler('input')" 
          >Input
        </button>
      </template>
      <template #navbar_output>
        <button 
          class="btn btn-outline-light rounded-0 mr-2"
          :class="visible.output ? 'active' : ''" 
          @click="visible_handler('output')" 
          >Output
        </button>
      </template>
      <template #navbar_socket>
        <button 
          class="btn btn-outline-light rounded-0 mr-2"
          :class="visible.socket ? 'active' : ''" 
          @click="visible_handler('socket')" 
          >Socket
        </button>
      </template>
    </NavBar>
    <FormPage v-if="visible.input" :config="input_config">
      <template #footer="slotProps">
        <button type="button" class="btn btn-outline-primary " @click="submit(slotProps)">Submit</button>
      </template>
    </FormPage>
    <Output v-if="visible.output" :config="output_config" :output="output_text"/>
    <Socket v-if="visible.socket" :data="socket_data" />
  </div>
</template>

<script>

import NavBar from './components/NavBar.vue'
import Output from './components/Output.vue'
import Socket from './components/Socket.vue'
import FormPage from './components/FormPage.vue'
import axios from 'axios';
import { io } from "socket.io-client";

export default {
  name: 'App',
  components: {
    NavBar,FormPage,Output,Socket
  },
  data () {
    return {
      navbar_config: { },
      input_config: { },
      output_config: { },
      output_text: null,
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
      console.log(json)
      let url = this.input_config.submit.url

      try {
        let output = await axios.post(url,json)
        if (output.status == 200){
          this.output_text = output.data
          console.log("POST SUCCESSFUL TO",url)
        }else{
          this.output_text = "Failed with code " + String(url) + " to " + url
          console.log(this.output_text)
        }

      } catch (error) {
          this.output_text = "Error to" + url + "\n" + String(error)  
          console.log(this.output_text)
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
      if (output.status == 200){
        this.input_config = JSON.parse(JSON.stringify(output.data))
      }else{
        console.log("POST FAILED WITH OTHER THAN 200")
        this.input_config = null
      }

    },
    calc: function(val){
      return val*4
    }


  },
  mounted: function () {
    this.getConfig()
    let socket = io("http://localhost:3000");
    socket.on("connect", () => {
      console.log("Connect Succcess"); 
    });

    socket.on("timer", (data) => {
      this.socket_data = data
    });

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
