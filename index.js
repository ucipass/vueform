// Test Express.js server to return the posted json to sender for testing
const express = require('express')
const app = express()
const port = 3000
const server = require('http').createServer(app);

let sockets = new Map()
const io = require('socket.io')(server, {
  cors: {
    origin: "http://localhost:8080",
    methods: ["GET", "POST"]
  }
});
io.on('connection', (socket)=>{
  let socketId = socket.id
  sockets.set(socketId,socket)
  console.log(`${socketId} connected`);
  socket.on('disconnect', (data)=>{
    console.log(`${socketId}(${socket.username}) disconnect event`);
    sockets.delete(socketId)
  })
  
})

var cors = require('cors')
app.use(cors())
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.post('/', (req, res) => {
  let json = JSON.parse(JSON.stringify(req.body))
  console.log(json)
  res.json(json)
})

server.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})

let timer = setInterval(()=>{
  // console.log(String(Date()))
  io.sockets.emit( "timer", String(Date()) );
},1000)