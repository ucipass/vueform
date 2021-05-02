<template>
  <div>

    <h1><slot name="testslot1"></slot></h1>
    <h1><slot name="testslot2"></slot></h1>
    <h1><slot name="testslot3" v-bind:config="user"></slot></h1>


  </div>

</template>

<script>
export default {
  name: 'Test',
  props: {
    config: Object,
  },
  data () {
    return {
      input_active: true,
      user:{
        firstname: "123",
        lastname: "1234"
      }
    }
  },
  methods: {
    refresh: function() {

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
