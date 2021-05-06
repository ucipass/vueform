<template>
<div class="container mt-3 mb-3 p-0">

    <div v-if="inputs.length" >

    <!-- HEADER -->
    <div v-if="config.header_text">
      <slot name="header" v-bind:header="values">
        <!-- HEADER FALLBACK -->
        <h2>{{config.header_text}}</h2>
      </slot>
    </div>

    <!-- INPUTS FOR LOOP   -->
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

      <!-- FOOTER -->
      
      <div class="d-flex justify-content-end m-1">
        <slot name="footer" v-bind:footer="values">
        <!-- FOOTER FALLBACK -->
        <!-- <button type="button" class="btn btn-outline-primary " @click="submit(values)">{{submit_text}}</button> -->          
        </slot>

      </div>
    </div>    

    <!-- JUMBOTRON IF NO INPUT CONFIG AVAILABLE -->
    <div v-else class="jumbotron float-center" >
      <p>Form configuration is not available</p>
    </div>
 
</div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'Input',
  props: {
    config: Object,
    test123: String
  },
  data () {
    return {
      // inputs: [],
      values: {},
      submit_text: this.config?.submit_text ? this.config.submit_text : "Submit" ,
      submit_url: this.config?.submit_url ? this.config.submit_url : "/" ,
      output: {},      
      input_active: true
    }
  },
  computed: {
    // a computed getter
    
    inputs: function () {
      if (this.config?.input_rows) {
        let values = this.values
        let inputs =  this.config.input_rows.filter( item => item.id )
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

    },
    submit: async function (json){
      console.log(json)
      let url = this.submit_url

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
          this.output_text = "Error to " + url + "\n" + String(error)  
          console.log(this.output_text)
      }
   
    }
  },
  mounted: function () {
    this.refresh()
    this.$emit("1","2")
    console.log("Mounted: Input:", this.config?.id)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
