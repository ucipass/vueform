const express = require('express')
const app = express()
const port = 3000
var cors = require('cors')
app.use(cors())
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.post('/', (req, res) => {
  let json = JSON.parse(JSON.stringify(req.body))
  console.log(json)
  res.json(json)
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})