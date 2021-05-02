<template>
  <div>
  <!-- NAVBAR -->
    <nav class="navbar navbar-expand navbar-dark bg-dark pb-0">
      <div class="container-fluid">
        <ul class="navbar-nav">
          <li class="nav-item">
            <slot name="navbar_input" class="btn btn-outline-light rounded-0"></slot>
          </li>
          <li class="nav-item">
            <slot name="navbar_output" class="btn btn-outline-light rounded-0"></slot>
          </li>
          <li class="nav-item">
            <slot name="navbar_socket" class="btn btn-outline-light rounded-0"></slot>
          </li>
        </ul>
      </div>
    </nav>    

  </div>

</template>

<script>
export default {
  name: 'NavBar',
  props: {
    config: Object,
  },
  data () {
    return {
      input_active: true,

    }
  },
  methods: {
    log: function(msg){
      console.log(msg)
    },
    refresh: function() {

    }
  },
  mounted: function () {
    this.refresh()
    console.log("Mounted: NavBar")
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
