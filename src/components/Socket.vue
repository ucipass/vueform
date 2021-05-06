<template>
<!-- SOCKET -->

    <div v-if="visible" class="m-3 d-flex flex-grow-1">
      <div class="d-flex flex-column mr-3">
        <div class="d-flex">
          <div class="dropdown">
            <button class="btn btn-outline-primary dropdown-toggle" type="button" id="dropdownMenuSave" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Save</button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuSave">
              <a class="dropdown-item" href="#">Save selected</a>
              <a class="dropdown-item" href="#">Save all as zip</a>
            </div>                
          </div>
          <div class="dropdown">
            <button class="btn btn-outline-primary dropdown-toggle" type="button" id="dropdownMenuDelete" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Delete</button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuDelete">
              <a class="dropdown-item" href="#">Delete selected</a>
              <a class="dropdown-item" href="#">Delete all as zip</a>
            </div>               
          </div>
       
        </div>
        <div class="d-flex flex-grow-1">
          <select width="20" multiple  class="form-control" id="exampleFormControlSelect1">
            <option  v-for="item in streams" :key="item.name" @click="select_stream" >{{item.name}}</option>
          </select>         
        </div>
      </div>
      <div  v-if="true" class="d-flex flex-column flex-grow-1 m-1">
        <Input :config="config.input_config">
          <template #footer="slotProps">
            <button type="button" class="btn btn-outline-primary " @click="submit(slotProps.footer)" data-toggle="modal" data-target="#modal_socketio_submit">Submit</button>
          </template>
        </Input>
        <label for="exampleFormControlTextarea1">Socket.io Event:</label>
        <textarea class="form-control text-nowrap h-100" id="TextAreaOutput"  :value="streams[select_index].data"  readonly></textarea>

      </div>

      <!-- Modal -->
      <div class="modal fade" id="modal_socketio_submit" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-body">
              <p>Status: Pending</p>
              <div class="form-group">
                <label for="exampleFormControlTextarea1">Reply data</label>
                <textarea class="form-control" id="exampleFormControlTextarea1" rows="3" readonly></textarea>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            </div>
          </div>
        </div>
      </div>

    </div>        



</template>

<script>
import Input from './Input.vue'
import { io } from "socket.io-client";

export default {

  name: 'Socket',
  components: {
    Input
  },
  props: {
    visible: Boolean,
    config: Object
  },
  data () {
    return {
      input_active: true,
      data: "",
      streams: 
        [
          { name: "default", data: "" }
        ],
      select_index: 0,
      socket: null
    }
  },
  methods: {
    test: function (data) { console.log("TEST:",data)  },
    refresh: function() {

    },
    submit: function(json){
      console.log("Socket.io sumbit",json)
    },
    socket_start(){

      let socket = io("http://localhost:3000");
      let streams = this.streams
      socket.on("connect", () => {
        console.log("Socket.io connected. Id:",socket.id); 
      });

      socket.on("data", (data) => {
        if( typeof data == "string"){
          this.streams[0].data +=  data
        }
        else if ( data.name && data.data ) {
          let index = streams.findIndex( (item) => item.name == data.name )
          if ( index == -1 ) {
            streams.push( { name: data.name, data : data.data}  )
            console.log("new",streams)
          }else{
            streams[index].data += data.data 
            console.log("existing",index,streams[index].data)
          }
        }
        else {
            console.log(123)
        }
      });

      socket.on('connect_error', () => {
        console.log("Socket.io connection error")
      })    

    },
    select_stream: function (event) {
      console.log(event.target.value)
      this.select_index = this.streams.findIndex( (item) => item.name == event.target.value )
    }
  },
  mounted: function () {
    this.refresh()
    if (! this.socket) {
      this.socket_start()
    }

    console.log("Mounted: Socket")
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>