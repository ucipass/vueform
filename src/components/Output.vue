<template>
  <div v-if=" typeof visible == 'undefined' ? true : visible" class="m-3 d-flex flex-fill">

<!-- OUTPUT -->
    <!-- <label class="mb-0" for="TextAreaOutput.id">output</label> -->
    <textarea class="form-control" id="TextAreaOutput" rows="20" style="resize:none" :value="data" readonly></textarea>

  </div>
</template>

<script>
export default {
  name: 'Output',
  props: {
    config: Object,
    visible: Boolean,
    json: null,
    data: String
  },
  data () {
    return {
      input_active: true,

    }
  },
  methods: {
    refresh: function() {

    }
  },
  mounted: function () {
    this.refresh()
    console.log("Mounted: Output")
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>