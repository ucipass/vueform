<template>
<div v-if="visible" id="PostMan" class="m-3 d-flex flex-grow-1">
    <div class="d-flex flex-column">
      <Input  :visible="true" :config="config">
        <template #footer="slotProps">
          <button type="button" class="btn btn-outline-primary " @click="submit(slotProps.footer)">Submit</button>
        </template>      
      </Input>
    </div>
    <div  class="d-flex flex-column flex-grow-1">
      <Output  :visible="true" :data="output_text"/>
    </div>
</div>
</template>

<script>
import axios from 'axios';
import Input from './Input.vue'
import Output from './Output.vue'
export default {
  name: 'PostMan',
  components: { Input,Output  },
  props: {
    visible: Boolean,
    config: Object
  },
  data () {
    return {
      submit_text: this.config?.submit_text ? this.config.submit_text : "Submit" ,
      submit_url: this.config?.submit_url ? this.config.submit_url : "/" ,
      output_text: ""
    }
  },
  computed: {
    // a computed getter
  },
  methods:{
    refresh: async function(){
    },
    submit: async function (json){
      let url = this.submit_url
      try {
        let output = await axios.post(url,json)
        if (output.status == 200){
          this.output_text = JSON.stringify(output.data,null,2)
          console.log("POST SUCCESSFUL TO",url,json )
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
    console.log("Mounted: Input:", this.config?.id)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
