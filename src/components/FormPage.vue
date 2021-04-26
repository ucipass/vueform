<template>
<div class="container">

  <nav class="navbar navbar-expand-lg navbar-dark bg-dark pb-0">
    <div class="container-fluid">
      <ul class="navbar-nav">
        <li class="nav-item">
          <button 
            class="btn btn-outline-light rounded-0" 
            :class="input_active ? 'active' : ''" 
            @click="input_active = true" 
            >Input
          </button>
        </li>
        <li class="nav-item">
          <button 
            class="btn btn-outline-light rounded-0" 
            :class="input_active ? '' : 'active'" 
            @click="input_active = false" 
            >Output
          </button>
        </li>
      </ul>
    </div>
  </nav>

  <div v-if="input_active">
    <div v-if="!(inputs.length)" class="jumbotron float-center" >
      <p>Form configuration is not available</p>
    </div>
    <div v-if="inputs.length">
      <div v-for="input in inputs" :key="input.id" class="mb-1">
        <label class="mb-0" :for="input.id">{{input.label}}</label>
        <input :type="input.type" class="form-control" :id="input.id" :placeholder="input.placeholder" v-model="input.value">
      </div>
      <div class="mb-1">
        <button type="button" class="btn btn-outline-primary" @click="submitFn">{{submit.text}}</button>
      </div>
    </div>    
  </div>

  <div v-if="!input_active" class="mb-1">
    <label class="mb-0" for="TextAreaOutput.id">output</label>
    <textarea class="form-control" id="TextAreaOutput" rows="20" :value="JSON.stringify(output, null, 2)"></textarea>
  </div>

</div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'FormPage',
  props: {
    config: Object,
  },
  data () {
    return {
      inputs: [],
      submit: [],
      output: {},      
      input_active: true
    }
  },
  methods:{
    refresh: function(){
      if(! this.config?.inputs) {
        console.log("No config recevied from parent. Retreiving config.json from server...")
        axios.get("config.json")
        .then((output)=>{
          if (output.status == 200){
            let data = output.data
            this.inputs = JSON.parse(JSON.stringify(data.inputs))
            this.submit = data.submit
          }else{
            console.log("POST FAILED WITH OTHER THAN 200")
          }
        })
        .catch((error)=>{
          this.output = error
          console.log("POST FAILED")
          console.log(error)
        })
        
      }
      else{
        // filter invalid records and set default values if not provided
        console.log("CONFIG !!!!!!!",this.config)
        this.inputs = this.config.inputs
        .filter( item => item.id )
        .map((item)=>{
          return {
            id: item.id,
            label: item.label ? item.label : item.id,
            type: (item.type ? item.type : "text"),
            placeholder: item.placeholder ? item.placeholder : "",
            value: ""
          } 
        })

        this.submit = {
            text: this.config.submit?.text ? this.config.submit.text : "Submit",
            url: this.config.submit?.url ? this.config.submit.url : window.location.href
        }
      }
    },
    submitFn: function(){
      let json = {}
      this.inputs.forEach(item => {
        json[item.id]=item.value
      });
      axios.post(this.submit.url,json)
      .then((output)=>{
        if (output.status == 200){
          this.output = output.data
          console.log("POST SUCCESSFUL TO",this.submit.url)
          console.log(JSON.stringify(output))
        }else{
          this.output = {status: output.status}
          console.log("POST FAILED WITH OTHER THAN 200 TO", this.submit.url)
          console.log(output)
        }
        
      })
      .catch((error)=>{
        this.output = error
        console.log("POST FAILED TO",this.submit.url)
        console.log(error)
      })
      
    }
  },
  mounted: function () {
    // eventBus.$on('loginEvent', () => {
    //     this.loggedIn = true
    // })
    // eventBus.$on('logoutEvent', () => {
    //     this.loggedIn = false
    // })
    this.refresh()
    console.log("Mounted: FormPage")
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
