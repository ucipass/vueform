<template>
  <div>

<!-- OUTPUT -->
  <div class="m-1">
    <label class="mb-0" for="TextAreaOutput.id">output</label>
    <textarea class="form-control" id="TextAreaOutput" rows="20" :value="JSON.stringify(output, null, 2)"></textarea>
  </div>

  </div>

</template>

<script>
export default {
  name: 'Output',
  props: {
    config: Object,
    output: null
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