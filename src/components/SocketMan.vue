<template>
<!-- SOCKET -->

    <div v-if="visible" id="SocketMan" class="m-3 d-flex flex-grow-1">
      <div class="d-flex flex-column mr-3">
        <div class="d-flex">
          <div class="dropdown">
            <button class="btn btn-outline-primary dropdown-toggle" type="button" id="dropdownMenuSave" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Save</button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuSave">
              <a class="dropdown-item" href="#">Save selected event</a>
              <a class="dropdown-item" href="#">Save all events zip</a>
            </div>                
          </div>
          <div class="dropdown">
            <button class="btn btn-outline-primary dropdown-toggle" type="button" id="dropdownMenuDelete" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Clear</button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuDelete">
              <a class="dropdown-item" href="#">Clear selected event</a>
              <a class="dropdown-item" href="#">Clear all events</a>
            </div>               
          </div>
       
        </div>
        <div class="d-flex flex-grow-1">
          <select width="20" multiple  class="form-control" id="exampleFormControlSelect1">
            <option  v-for="item in events" :key="item.name" @click="select_stream" >{{item.name}}</option>
          </select>         
        </div>
      </div>
      <div  class="d-flex flex-column flex-grow-1 m-1">
        <Input :config="socket_input">
          <template #header>
            <div>
              <div class="row m-1">
                <div class="col">
                  <p class="m-0">Status: {{socket_io_status}}</p>
                </div>
                <div class="col">
                  <p class="m-0">Request: {{socket_send_status}}</p>
                </div>
              </div>
              <hr>
            </div>
          </template>
          <template #footer="slotProps">
            <button type="button" class="btn btn-outline-primary " @click="submit(slotProps.footer)" data-toggle="modal" data-target="#modal_socketio_submit">Submit</button>
          </template>
        </Input>
        <label for="exampleFormControlTextarea1">Socket.io Event:</label>
        <textarea class="form-control h-100" id="TextAreaOutput"  :value="events.length ? events[select_index].data : ''"  readonly></textarea>
      </div>

      <!-- Modal -->
      <div class="modal fade" id="modal_socketio_submit" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-body">
              <p>Status: {{socket_send_status}}</p>
              <div class="form-group">
                <label for="exampleFormControlTextarea1">Reply data</label>
                <textarea class="form-control" id="exampleFormControlTextarea1" rows="8" readonly :value="socket_send_reply_data"></textarea>
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
  components: { Input  },
  props: {
    visible: Boolean,
    config: Object
  },
  data () {
    return {
      events: [ ],
      select_index: 0,
      socket: null,
      socket_io_status: "not connected",
      socket_send_status: "not sent",
      socket_send_reply_data: "",
      socket_input : {
        "id": "socket_input",
        "input_rows": [
          {
            "id": "socketio_url",
            "label": "Socket.io URL",
            "placeholder": "http(s)://localhost:[port]/socket.io",
            "information": "Leave empty for default: http(s)://localhost:[port]/socket.io",
            "value" : ""
          },
          {
            "id": "eventName",
            "label": "Event Name",
            "placeholder": "Event Name...",
            "information": "Socket.io event name identified by a string like 'ping', 'data'. etc.",
            "value" : "data"
          },
          {
            "id": "data",
            "label": "Socket Data",
            "placeholder": "Enter string or json",
            "type": "text",
            "information": "Currently only string is supported in this field"
          }
        ]
      }
    }
  },
  methods: {
    test: function (data) { console.log("TEST:",data)  },
    refresh: function() {

    },
    submit: function(json){
      console.log("Socket.io sumbit",json)
      this.socket_send_status="Pending"
      this.socket.emit(json.eventName, json.data , (response) => {
        // this.socket_send_reply_data = JSON.stringify(response)
        this.socket_send_reply_data = ((typeof response == "string") ? response : JSON.stringify(response, null, 2))
        this.socket_send_status="sent completed"
        console.log("JSON Reply",response?.status); // ok
      });      
    },
    socket_start(){

      this.socket = io("http://localhost:3000");
      let socket = this.socket
      // let streams = this.streams
      socket.on("connect", () => {
        this.socket_io_status="connected"
        console.log("Socket.io connected. Id:",socket.id); 
      });

      socket.onAny((event,data) => {
        let current_events = this.events
        let current_event = event
        let current_data = (typeof data == "string") ? data : JSON.stringify(data) + "\n"
        // console.log(`Incoming event: ${current_event}, data:`, current_data);

        let index = current_events.findIndex( (item) => item.name == current_event )
        if ( index <0 ) {
          current_events.push( { name: current_event, data: current_data} )
        } else{
          current_events[index].data += current_data
        }

      });

      socket.on('connect_error', () => {
        this.socket_io_status="connection error"
        console.log("Socket.io connection error")
      })    

    },
    select_stream: function (event) {
      console.log(event.target.value)
      this.select_index = this.events.findIndex( (item) => item.name == event.target.value )
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