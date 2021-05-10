<template>

    <div v-if="visible" id="SSHClient" class="m-3 d-flex flex-grow-1">
      <div class="d-flex flex-column mr-3">
        <div class="d-flex">
          
          <!-- LEFT HAND SIDE -->
          <div class="dropdown">
            <button class="btn btn-outline-primary dropdown-toggle" type="button" id="dropdownMenuSave" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Add</button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuSave">
              <button class="dropdown-item" data-toggle="modal" data-target="#modal_add_new_host" >Add host manually</button>
              <button class="dropdown-item" data-toggle="modal" data-target="#modal_add_csv_hosts" >Add hosts via CSV File</button>
              <button class="dropdown-item" data-toggle="modal" data-target="#modal_add_json_host" >Add hosts via JSON File</button>
            </div>                
          </div>

          <div class="dropdown">
            <button class="btn btn-outline-primary dropdown-toggle" type="button" id="dropdownMenuDelete" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Delete</button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuDelete">
              <button class="dropdown-item" @click="host_delete_selected" >Delete selected host</button>
              <button class="dropdown-item" @click="host_delete_all" >Delete all hosts</button>
            </div>               
          </div>

          <div class="dropdown">
            <button class="btn btn-outline-primary dropdown-toggle" type="button" id="dropdownMenuSave" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Save</button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuSave">
              <a class="dropdown-item" href="#">Save configuration as CSV</a>
              <a class="dropdown-item" href="#">Save configuration as JSON</a>
            </div>                
          </div>
          
        </div>
        <div class="d-flex flex-grow-1">
          <select width="20" autofocus multiple class="custom-select" id="hostname_select">
            <option :selected="hostnames[select_index] == host"    :id="'hostname_select_'+host" v-for="host in hostnames" :key="host" @click="select_stream" >{{host}}</option>
          </select>         
        </div>
      </div>

      <!-- RIGHT HAND SIDE -->
      <div  class="d-flex flex-column flex-grow-1">
      <table v-if="hosts.length" class="table">
        <thead>
          <tr>
            <th scope="col">Hostname</th>
            <th scope="col">IP</th>
            <th scope="col">Port</th>
            <th scope="col">Username</th>
            <th scope="col">Command</th>
            <th scope="col">Expect</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{{hosts[select_index].hostname}}</td>
            <td>{{hosts[select_index].ip}}</td>
            <td>{{hosts[select_index].port}}</td>
            <td>{{hosts[select_index].username}}</td>
            <td>{{hosts[select_index].command}}</td>
            <td>{{hosts[select_index].expect}}</td>
          </tr>
        </tbody>
      </table>        
        <button type="button" class="btn btn-outline-primary " @click="submit()" >Submit</button>
        <label for="exampleFormControlTextarea1">SSH Output:</label>
        <textarea class="form-control h-100 terminal text-white bg-dark" id="TextAreaOutput"  :value="hosts[select_index] ? hosts[select_index].output : '' "  readonly></textarea>
      </div>

      <!-- MODAL -->
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

      <InputModal :ref="config_modal_add_new_host.id" :config="config_modal_add_new_host" ><button type="button" class="btn btn-primary" @click="modal_add_new_host()" >Save</button></InputModal>
      <InputModal :ref="config_modal_add_csv_hosts.id" :config="config_modal_add_csv_hosts" ><button type="button" class="btn btn-primary" @click="modal_add_csv_hosts()" >Save</button></InputModal>

    </div>        

</template>

<script>
// import Input from './Input.vue'
import InputModal from './InputModal.vue'
import { io } from "socket.io-client";
import $ from 'jquery'
import Papa from 'papaparse'

export default {
  name: 'SSHClient',
  components: { InputModal  },
  props: {
    visible: Boolean,
    config: Object
  },
  data () {
    return {
      hosts: [],
      hostnames: [],
      host_tenplate: { hostname: "", ip: "", port: "22", username: "test", password: "test", command: "show run", expect: "user"},
      select_value: "",
      select_index: 0,
      host_input_rows : [
          {
            "id": "hostname",
            "label": "Hostname",
            "placeholder": "Enter hostname...",
            "information": "This name needs to be unique and will be used for file naming too.",
            "value" : ""
          },
          {
            "id": "ip",
            "label": "IP address",
            "placeholder": "Enter IP address...",
            "information": "IPv4 only...",
            "value" : ""
          },
          {
            "id": "port",
            "label": "TCP Port",
            "placeholder": "Enter port number. If left empty, default to 22.",
            "information": "Enter port number. If left empty, default to 22.",
            "value" : "22"
          },
          {
            "id": "username",
            "label": "Username",
            "placeholder": "Enter Username...",
            "type": "text",
            "information": "SSH Username",
            "value": ""
          },
          {
            "id": "password",
            "label": "Password",
            "placeholder": "Enter password...",
            "type": "password",
            "information": "Command to be sent via SSH",
            "value": ""
          },
          {
            "id": "command",
            "label": "Command",
            "placeholder": "Enter command...",
            "type": "text",
            "information": "Command to be sent via SSH",
            "value": ""
          },
          {
            "id": "expect",
            "label": "Expect",
            "placeholder": "Enter regex to verify reply... (optional)",
            "type": "text",
            "information": "Regular expression has to match output from SSH session to mark this as successful, if left open SSH session termination is enough for success."
          }
        ],
      host_csv_input_rows : [
          {
            "id": "csvfile",
            "label": "CSV File",
            "placeholder": "Add CSV File...",
            "type": "file",
            "information": "CSV fields are hostname,ip (mandatory) - username,password,port,command,expect (optional)",
            "value" : ""
          }
        ],
      events: [ ],
      socket: null,
      socket_io_status: "not connected",
      socket_send_status: "not sent",
      socket_send_reply_data: "",
    }
  },
  computed: {
    socket_input: function() {
      return {
        id: "socket_input",
        input_rows: this.host_input_rows
      }
    },
    current_host: function() {
      if ( this.hostnames[0] && this.hosts[0]) {
        return this.hosts[this.select_index] ? this.hosts[this.select_index] : []
      }else{
        return []
      }
    },
    config_modal_add_new_host: function() {
      return { id: "modal_add_new_host", input_rows: this.host_input_rows }
    },
    config_modal_add_csv_hosts: function() {
      return { id: "modal_add_csv_hosts", input_rows: this.host_csv_input_rows }
    }


  },
  methods: {
    test: function (data) { console.log("TEST:",data)  },
    refresh: function() {

    },
    add_hosts: function(hosts){
      for (let index = 0; index < hosts.length; index++) {
        let host = JSON.parse(JSON.stringify(hosts[index])) ;
        if ( host?.hostname && host?.ip){
          host.port     = host.port     ? host.port     : this.host_tenplate.port
          host.username = host.username ? host.username : this.host_tenplate.username
          host.password = host.password ? host.password : this.host_tenplate.password
          host.command  = host.command  ? host.command  : this.host_tenplate.command
          host.expect   = host.expect   ? host.expect   : this.host_tenplate.expect
          host.output   = ""
        }else{
          console.log(`invalid host '${host.hostname}' `)
          return;
        }

        let host_index = this.hostnames.indexOf(host.hostname)
        if ( host_index < 0 ){
          console.log(`adding new host: ${host.hostname}`)
          this.hostnames.push(host.hostname)
          this.hosts.push(host)
        }else{
          console.log(`overwriting existing host: ${host.hostname}`)
          Array.prototype.insert   
          this.hosts.splice    ( host_index,1)
          this.hostnames.splice( host_index,1)
          this.hosts.splice    ( host_index,0,host)
          this.hostnames.splice( host_index,0,host.hostname)
        }
      }

},
    host_delete_selected: function (){
      let old_select_index = this.select_index
      this.select_index = this.select_index ? this.select_index -1 : this.select_index // move index back unless it is 0
      this.hosts.splice(      old_select_index,1)
      this.hostnames.splice(  old_select_index,1)
    },
    host_delete_all: function (){
      this.select_index = 0
      this.hosts = []
      this.hostnames = []
    },
    modal_add_new_host: function(){
      let host = this.$refs.modal_add_new_host.values
      this.add_hosts( [host])
      $(this.$refs.modal_add_new_host.id).modal('hide');
    },
    modal_add_csv_hosts: function(){
      let file = this.$refs.modal_add_csv_hosts.buffers.csvfile
      let hosts = Papa.parse(file, {header: true});
      $('#'+this.config_modal_add_csv_hosts.id).modal('hide')
      this.add_hosts(hosts.data)
      this.select_index = 0
    },
    submit: function(){
      console.log("Socket.io sumbit",this.hostnames)
      let json = Array.from( this.hosts)
      this.socket_send_status="Pending"
      this.socket.emit("data", json , (response) => {
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
        let hostname = data.hostname
        let output = data.output
        let host_index = this.hostnames.indexOf(hostname)
        if ( event == "data" && typeof data == "object" && host_index >= 0 ) {
          console.log(`Incoming event: ${event} for hostname: ${hostname}`);
          let host = this.hosts[host_index]
          host.output += output
        }else{
          console.log(`Incoming event "${event}" is invalid!`);
        }
     
      });

      socket.on('connect_error', () => {
        this.socket_io_status="connection error"
        console.log("Socket.io connection error")
      })    

    },
    select_stream: function (event) {
      this.select_index = this.hostnames.findIndex( (item) => item == event.target.value )
    }
  },
  mounted: function () {
    this.refresh()
    let new_hosts = [
      // { hostname: "c3560-1", ip: "172.18.100.1"},
      // { hostname: "c3560-2", ip: "172.18.2.1"},
      // { hostname: "c3560-3", ip: "172.18.3.1"}

    ]
    this.add_hosts ( new_hosts)
    if (! this.socket) {
      this.socket_start()
    }

    console.log("Mounted: SSHClient")
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.terminal {
    padding: 8px;
    font-family: courier new;
}
</style>