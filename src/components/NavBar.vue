<template>
  <div class="container-fulid w-100">
  <!-- NAVBAR -->
    <nav class="navbar navbar-expand navbar-dark bg-primary pb-0 ">
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

    <!-- <div class="m-2">
      <ul class="nav nav-tabs">
        <li class="nav-item">
          <button class="btn-primary-outline nav-link" :class="tab1 ? 'active' : '' " @click="tab1=!tab1" >Active</button>
        </li>
        <li class="nav-item">
          <button class="nav-link" :class="tab2 ? 'active' : '' " @click="tab2=!tab2" >Link</button>
        </li>
        <li class="nav-item">
          <button class="nav-link" :class="tab3 ? 'active' : '' " @click="tab3=!tab3" >Link</button>
        </li>
        <li class="nav-item">
          <button class="nav-link disabled" >Disabled</button>
        </li>
      </ul>
    </div> -->

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
      tab1: true,
      tab2: false,
      tab3: false

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
