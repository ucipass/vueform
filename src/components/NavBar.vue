<template>
  <div class="container-fulid w-100">
  <!-- NAVBAR -->
    <nav class="navbar navbar-expand navbar-dark bg-primary pb-0 ">
      <div class="container-fluid">
        <ul class="navbar-nav">
          <li v-for=" item in status" :key="item.name" class="nav-item">
            <button 
              class="btn btn-outline-light rounded-0 mr-2" :class="item.active ? 'active' : '' "
              @click="navbar_handler(item.name)" 
              >{{item.name}}
            </button>
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
      navbar: {}      
    }
  },
  computed: {
    status: function(){
      let status = []
      for (const key in this.navbar) {
        if (Object.hasOwnProperty.call(this.navbar, key)) {
          status.push( {name: key, active: this.navbar[key]})
        }
      }      
      return status
    }
  },
  methods: {
    // management of navbar status comes from this.navbar
    navbar_handler: function (name){
      for (const key in this.navbar) {
        if (Object.hasOwnProperty.call(this.navbar, key)) {
          this.navbar[key] = false
        }
      }
      this.navbar[name] = true
    },
    //Initial navbar setting come from config prop
    refresh: function() {
      this.navbar = JSON.parse(JSON.stringify( this.config) )
     
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
