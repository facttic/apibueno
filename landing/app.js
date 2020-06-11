const express = require('express')
const app = express()
const port = 3000
const path = require('path')

// static assets 
app.use('/dist', express.static('dist'))
app.use('/js', express.static('js'))
app.use('/img', express.static('img'))
app.use('/favicon.ico', express.static('./favicon.ico'));
// routing 
app.get('/', (req, res) => res.sendFile(path.join(__dirname + '/index.html')))
app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))