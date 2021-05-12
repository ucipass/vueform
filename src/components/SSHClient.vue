<template>
<div v-if="visible" id="SSHClient" class="d-flex flex-column flex-grow-1 overflow-auto">


    <!-- NAV ROW -->
    <div id="top-navbar-row"  class="d-flex mt-3 ml-3 mr-3">
          <ul class="nav nav-tabs">
            <li class="nav-item">
              <a class="nav-link" :class="view.host ? 'active' : '' " href="#" @click="view.host=true;view.output=false;view.template=false;">Host View</a>
            </li>
            <li class="nav-item">
              <a class="nav-link " :class="view.output ? 'active' : '' " href="#" @click="view.host=false;view.output=true;view.template=false;">SSH Output View</a>
            </li>
            <li class="nav-item">
              <a class="nav-link " :class="view.template ? 'active' : '' " href="#" @click="view.host=false;view.output=false;view.template=true;">Template View</a>
            </li>
            <!-- MENU -->
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">Menu</a>
                <div class="dropdown-menu" aria-labelledby="dropdownMenuSave">
                  <button class="dropdown-item" @click="run_active" >Run Active</button>
                  <button class="dropdown-item" @click="run_all" >Run All</button>
                  <div class="dropdown-divider"></div>
                  <button class="dropdown-item" data-toggle="modal" data-target="#modal_add_new_host" >Add host manually</button>
                  <button class="dropdown-item" data-toggle="modal" data-target="#modal_add_new_host" >Add hosts copy/paste</button>
                  <button class="dropdown-item" data-toggle="modal" data-target="#modal_add_json_host" >Add hosts via YAML File</button>
                  <button class="dropdown-item" data-toggle="modal" data-target="#modal_add_json_host" >Add hosts via JSON File</button>
                  <button class="dropdown-item" data-toggle="modal" data-target="#modal_add_csv_hosts" >Add hosts via CSV File</button>
                  <div class="dropdown-divider"></div>
                  <button class="dropdown-item" @click="hosts_save_yaml" >Save as YAML</button>
                  <button class="dropdown-item" @click="hosts_save_json" >Save as JSON</button>
                  <button class="dropdown-item" @click="hosts_save_json" >Save as CSV</button>
                  <button class="dropdown-item" @click="hosts_save_json" >Save Output as [hostname].txt</button>
                  <button class="dropdown-item" @click="hosts_save_json" >Save All Outputs as output.zip</button>
                  <div class="dropdown-divider"></div>
                  <button class="dropdown-item" @click="host_delete_selected" >Delete selected host</button>
                  <button class="dropdown-item" @click="host_delete_all" >Delete all hosts</button>
                </div>                
            </li>
          </ul>
    </div >

    <!-- HOSTS VIEW -->
    <div id="bottom-main-row-host-view" v-if="view.host" class="d-flex flex-grow-1 m-3 overflow-auto">
            <table v-if="hosts.length" class="table">
              <thead>
                <tr>
                  <th scope="col">Hostname</th>
                  <th scope="col">IP</th>
                  <th scope="col">Port</th>
                  <th scope="col">Username</th>
                  <th scope="col">Command</th>
                  <th scope="col">Expect</th>
                  <th scope="col">Action</th>
                </tr>
              </thead>
              <tbody >
                <tr v-for="host in hosts" :key="host.hostname" >
                  <td>{{host.hostname}}</td>
                  <td>{{host.ip}}</td>
                  <td>{{host.port}}</td>
                  <td>{{host.username}}</td>
                  <td>{{host.command}}</td>
                  <td>{{host.expect}}</td>
                  <td>
                    <button class="btn-small btn-success mr-1" @click="run_active(host.hostname)">Run 
                      <span v-if="host.status == 'pending'" class="spinner-border spinner-border-sm" role="status" aria-hidden="true" > </span>
                    </button>
                    <button class="btn-small btn-primary mr-1" @click="modal_edit_host_fill(host.hostname)">Edit</button>
                    <button class="btn-small btn-danger" @click="select_index=hostnames.indexOf(host.hostname); host_delete_selected();" modal_edit_host_fill>Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>
    </div>    

    <!-- OUTPUT VIEW -->
    <div id="bottom-main-row-output-view" v-if="view.output" class="d-flex flex-grow-1 m-3 mh-100 ">
      <!-- HOST SELECTOR - LEFTSIDE -->
      <div id="left-main-column"   class="d-flex flex-column mr-3">
        <div class="d-flex flex-grow-1">
          <select width="20" autofocus multiple class="custom-select" id="hostname_select " @change="select_stream">
            <option :selected="hostnames[select_index] == host"    :id="'hostname_select_'+host" v-for="host in hostnames" :key="host"  >{{host}}</option>
          </select>         
        </div>
      </div>
      <!-- SSH OUTPUT TEXTAREA - RIGHTSIDE -->
      <div  id="right-main-column" class="d-flex flex-column flex-grow-1 overflow-auto">
        <div class="d-flex flex-column flex-fill">
            <label for="exampleFormControlTextarea1">SSH Output: {{hosts[select_index].hostname}} ({{hosts[select_index].ip}})</label>
            <textarea class="d-flex flex-grow-1 form-control terminal text-white bg-dark" id="TextAreaOutput"  :value="hosts[select_index] ? hosts[select_index].output : '' "  readonly></textarea>
        </div>
      </div>
    </div>

    <!-- SETTINGS VIEW -->
    <div id="bottom-main-row-template-view" v-if="view.template" class="d-flex flex-column flex-grow-1 m-3 mh-100 ">
      <h3 class="text-center" >Default Host Settings</h3>
        <Input ref="settings" :config="config_template"/>
    </div>

    <!-- MODALS -->
    <InputModal :ref="config_modal_add_new_host.id"  :config="config_modal_add_new_host" >
      <button type="button" class="btn btn-primary" @click="modal_add_new_host()" >Save</button>
    </InputModal>
    <InputModal :ref="config_modal_add_csv_hosts.id" :config="config_modal_add_csv_hosts" >
      <button type="button" class="btn btn-primary" @click="modal_add_csv_hosts()" >Save</button>
    </InputModal>
    <InputModal :ref="config_modal_edit_host.id"     :config="config_modal_edit_host" >
      <button type="button" class="btn btn-primary" @click="modal_edit_host()" >Save</button>
    </InputModal>

</div>
</template>

<!--  Javascript Section -->
<script>
import Input from './Input.vue'
import InputModal from './InputModal.vue'
import { io } from "socket.io-client";
import $ from 'jquery'
import Papa from 'papaparse'
import YAML from 'yaml'
import { saveAs } from 'file-saver';

export default {
  name: 'SSHClient',
  components: { InputModal, Input  },
  props: {
    visible: Boolean,
    config: Object
  },
  data () {
    return {
      view: { 
        host: true,
        output: false,
        template: false,
      },
      hosts: [],
      hostnames: [],
      host_tenplate: { hostname: "", ip: "", port: "22", username: "test", password: "test", command: "show version", expect: "user"},
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
      host_input_edit_rows : [
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
            "value" : "222"
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
    config_template: function() {
      let input_rows = [
          {
            "id": "port",
            "label": "TCP Port",
            "placeholder": "Enter port number. If left empty, default to 22.",
            "information": "Enter port number. If left empty, default to 22.",
            "value" : this.host_tenplate.port
          },
          {
            "id": "username",
            "label": "Username",
            "placeholder": "Enter Username...",
            "type": "text",
            "information": "SSH Username",
            "value": this.host_tenplate.username
          },
          {
            "id": "password",
            "label": "Password",
            "placeholder": "Enter password...",
            "type": "password",
            "information": "Command to be sent via SSH",
            "value": this.host_tenplate.password
          },
          {
            "id": "command",
            "label": "Command",
            "placeholder": "Enter command...",
            "type": "text",
            "information": "Command to be sent via SSH",
            "value": this.host_tenplate.command
          },
          {
            "id": "expect",
            "label": "Expect",
            "placeholder": "Enter regex to verify reply... (optional)",
            "type": "text",
            "information": "Regular expression has to match output from SSH session to mark this as successful, if left open SSH session termination is enough for success.",
            "value": this.host_tenplate.expect
          }
        ]
      return { id: "config_template", input_rows: input_rows }
    },
    config_modal_add_new_host: function() {
      return { id: "modal_add_new_host", input_rows: this.host_input_rows }
    },
    config_modal_add_csv_hosts: function() {
      return { id: "modal_add_csv_hosts", input_rows: this.host_csv_input_rows }
    },
    config_modal_edit_host: function() {
      return { id: "modal_edit_host", input_rows: this.host_input_edit_rows }
    }
  },
  methods: {
    test: function (data) { console.log("TEST:",data)  },
    refresh: function() {

    },
    nav_select(event){
      console.log("NAV",event)
    },
    hosts_save_json: function(){
      var blob = new Blob([JSON.stringify(this.hosts,2,null)], {type: "text/plain;charset=utf-8"});
      saveAs(blob, "hosts.json");
    },
    hosts_save_yaml: function(){
      var blob = new Blob([YAML.stringify(this.hosts       )], {type: "text/plain;charset=utf-8"});
      saveAs(blob, "hosts.yaml");
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
          host.status   = ""
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
    modal_edit_host: function(){
      $("#"+this.$refs.modal_edit_host.id).modal('toggle');
      console.log("EDIT HOSTS",this.$refs.modal_edit_host.values)
      let new_host = JSON.parse(JSON.stringify(this.$refs.modal_edit_host.values))
      let old_host = this.hosts[this.select_index]
      for (const key in new_host) {
        old_host[key] = new_host[key]
      }
    },
    modal_edit_host_fill: function (hostname){
      $("#"+this.$refs.modal_edit_host.id).modal('toggle');
      let index = this.hostnames.indexOf(hostname)
      this.select_index = index
      let host = this.hosts[index]
      for (const row of this.host_input_edit_rows) {
        row.value = host[row.id]
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
    run_active: function(hostname){
      if (hostname) {
        this.select_index = this.hostnames.indexOf(hostname) >= 0 ? this.hostnames.indexOf(hostname) : this.select_index
      }
      let hosts = [ this.hosts[this.select_index] ]
      let hostnames = this.hosts[this.select_index].hostname
      console.log("Socket.io sumbit",hostnames)
      for (const host of hosts) {
          host.status = "pending"
      }
      let json = Array.from( hosts)
      this.socket_send_status="Pending"
      this.socket.emit("data", json , (response) => {
        this.socket_send_reply_data = ((typeof response == "string") ? response : JSON.stringify(response, null, 2))
        this.socket_send_status="sent completed"
        console.log("JSON Reply",response?.status); // ok
      }); 
    },
    run_all: function(){
      let hosts = this.hosts
      let hostnames = this.hostnames
      console.log("Socket.io sumbit",hostnames)
      for (const host of hosts) {
          host.status = "pending"
      }
      let json = Array.from( hosts)
      this.socket_send_status="Pending"
      this.socket.emit("data", json , (response) => {
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
          host.status = "success"
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
      { hostname: "c3560-1", ip: "172.18.100.1"},
      { hostname: "c3560-2-really-long.hostname.com", ip: "172.18.2.1"},
      { hostname: "c3560-3", ip: "172.18.3.1"}
      // { hostname: "c3560-1a", ip: "172.18.100.1"},
      // { hostname: "c3560-2a", ip: "172.18.2.1"},
      // { hostname: "c3560-3a", ip: "172.18.3.1"},
      // { hostname: "c3560-1b", ip: "172.18.100.1"},
      // { hostname: "c3560-2b", ip: "172.18.2.1"},
      // { hostname: "c3560-3b", ip: "172.18.3.1"},
      // { hostname: "c3560-1c", ip: "172.18.100.1"},
      // { hostname: "c3560-2c", ip: "172.18.2.1"},
      // { hostname: "c3560-3v", ip: "172.18.3.1"}

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