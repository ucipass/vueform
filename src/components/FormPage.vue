<template>
<div class="container">

    <!-- JUMBOTRON IF NOT INPUT CONFIG AVAILABLE -->
    <div v-if="!(inputs.length)" class="jumbotron float-center" >
      <p>Form configuration is not available</p>
    </div>

    <!-- INPUTS FOR LOOP   -->
    <div v-if="inputs.length" >
      <div class="d-flex" >
        <div class="d-flex flex-column justify-content-between">
            <div v-for="input in inputs" :key="input.id" class="m-1 d-flex justify-content-end">
                  <label class="m-1 float-right text-nowrap" :for="input.id">{{input.label}}</label>
                  <span class="m-1 float-right"  v-tooltip:left="input.information">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-info-circle" viewBox="0 0 16 16">
                      <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                      <path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>
                    </svg>                
                  </span>
            </div>
        </div>            
        <div class="d-flex flex-column justify-content-between w-100">
            <div v-for="input in inputs" :key="input.id" class=" m-1 ">
                    <input :type="input.type" class="form-control" :id="input.id" :placeholder="input.placeholder" v-model="values[input.id]">
            </div>
        </div>
      </div>
      <hr>
      <div class="d-flex justify-content-end">
        <slot name="footer" v-bind:default="values"></slot>
        <!-- <button type="button" class="btn btn-outline-primary " @click="submitFn">{{submit.text}}</button> -->
      </div>
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
      // inputs: [],
      values: {},
      submit: [],
      output: {},      
      input_active: true
    }
  },
  computed: {
    // a computed getter
    inputs: function () {
      if (this.config?.inputs) {
        let values = this.values
        let inputs =  this.config.inputs.filter( item => item.id )
        .map((item)=>{
          values[item.id] = item.value ? item.value : null
          return {
            id: item.id,
            label: item.label ? item.label : item.id,
            type: (item.type ? item.type : "text"),
            placeholder: item.placeholder ? item.placeholder : "",
            information: item.information ? item.information : "",
          }
        })
        return inputs
      }
      else{
        return []
      }
   }
  },
  methods:{
    refresh: async function(){
      // let config = await this.config
      // this.inputs = config.inputs
      // .filter( item => item.id )
      // .map((item)=>{
      //   return {
      //     id: item.id,
      //     label: item.label ? item.label : item.id,
      //     type: (item.type ? item.type : "text"),
      //     placeholder: item.placeholder ? item.placeholder : "",
      //     information: item.information ? item.information : "",
      //     value: ""
      //   } 
      // })      



      // if(! this.config?.inputs) {
      //   console.log("No config recevied from parent. Retreiving config.json from server...")
      //   axios.get("config.json")
      //   .then((output)=>{
      //     if (output.status == 200){
      //       let data = output.data
      //       this.inputs = JSON.parse(JSON.stringify(data.inputs))
      //       this.submit = data.submit
      //     }else{
      //       console.log("POST FAILED WITH OTHER THAN 200")
      //     }
      //   })
      //   .catch((error)=>{
      //     this.output = error
      //     console.log("POST FAILED")
      //     console.log(error)
      //   })
        
      // }
      // else{
      //   // filter invalid records and set default values if not provided
      //   console.log("CONFIG !!!!!!!",this.config)
      //   this.inputs = this.config.inputs
      //   .filter( item => item.id )
      //   .map((item)=>{
      //     return {
      //       id: item.id,
      //       label: item.label ? item.label : item.id,
      //       type: (item.type ? item.type : "text"),
      //       placeholder: item.placeholder ? item.placeholder : "",
      //       information: item.information ? item.information : "",
      //       value: ""
      //     } 
      //   })

      //   this.submit = {
      //       text: this.config.submit?.text ? this.config.submit.text : "Submit",
      //       url: this.config.submit?.url ? this.config.submit.url : window.location.href
      //   }
      // }
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
    this.refresh()
    console.log("Mounted: FormPage")
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
