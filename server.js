// Test Express.js server to return the posted json to sender for testing
const express = require('express')
const app = express()
const port = 3000
const server = require('http').createServer(app);


//************** RETURN ANY SOCKET.IO JSON OBJECT TO SENDER ****************/
const io = require('socket.io')(server, {
  cors: {
    origin: "http://localhost:8080",
    methods: ["GET", "POST"]
  }
});

let sockets = new Map()

io.on('connect', (socket)=>{
  let socketId = socket.id
  sockets.set(socketId,socket)
  console.log(`${socketId} connected`);
  socket.on('disconnect', (data)=>{
    console.log(`${socketId}(${socket.username}) disconnect event`);
    sockets.delete(socketId)
  })
  socket.onAny((event,data,callbackFn) => {
    let json = { eventName: event, data: data}
    console.log(`Received event: ${event}, data:`, data);
    callbackFn(json)
  });

  
})

//************** RETURN ANY POST JSON OBJECT TO SENDER ****************/
var cors = require('cors')
app.use(cors())
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.post('/', (req, res) => {
  let json = JSON.parse(JSON.stringify(req.body))
  console.log(json)
  res.json(json)
})

app.post('/*', (req, res) => {
  let json = JSON.parse(JSON.stringify(req.body))
  console.log(json)
  res.json(json)
})

server.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})

//************** SEND TEST SOCKET.IO EVENT EEVERY SECOND ****************/
let timer = setInterval(()=>{
  let date_string = String(Date()) + "\n"

  io.sockets.emit( "data" , "data event: " + date_string );
  io.sockets.emit( "CurrentTime" , "CurrentTime event: " + date_string );
  io.sockets.emit( "CurrentTimeObject" , { name: "current", data: "current:" + date_string   } );

},1000)