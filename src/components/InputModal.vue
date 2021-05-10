<template>
<div :id="this.config.id" class="modal" tabindex="-1" role="dialog">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Modal title</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <Input ref="input" :config="input_config"/>
      </div>
      <div class="modal-footer">
        <slot>
        <!-- FOOTER FALLBACK -->
        <!-- <button type="button" class="btn btn-outline-primary " @click="submit(values)">{{submit_text}}</button> -->          
        </slot>
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import Input from './Input.vue'
export default {
  name: 'InputModal',
  components: { Input  },  
  props: {
    config: Object,
  },
  computed: {
    values: function() {
      return this.$refs.input.values
    },
    buffers: function() {
      return this.$refs.input.buffers
    },
    id: function () {
      return this.config?.id ? this.config.id : this._uid
    },
    input_config: function() {
      return { 
                id: this.config?.id ? this.config.id + "_input" : this._uid + "_input",
                input_rows: this.config.input_rows
              }
    }
  },
  mounted: function () {
    console.log("Mounted: InputModal:", this.config?.id)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
