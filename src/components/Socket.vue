<template>
  <div>

<!-- OUTPUT -->
  <div class="m-1">
    <label class="mb-0" for="TextAreaOutput.id">Socket</label>
    <textarea class="form-control" id="TextAreaOutput" rows="20" :value="data"></textarea>
  </div>

  </div>

</template>

<script>
export default {
  name: 'Socket',
  props: {
    config: Object,
    data: null
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