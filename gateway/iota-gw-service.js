const IOTA = require('iota.lib.js')
const http = require('http')
const port = 3000
 
const iota = new IOTA({ provider: 'https://nodes.testnet.iota.org:443' })

// optional
iota.api.getNodeInfo((error, success) => {
	if (error) {
		console.log(error)
	} else {
		console.log(success)
	}
})

// grab target address from ENV!
const trytes = process.env.IOTAADDRESS;

if (trytes === undefined || trytes.length != 81) {
  console.log("ERROR please set IOTAADDRESS correctly.");
  process.exit(1);
}

const requestHandler = (request, response) => {
  if (!(request.url.startsWith('/tx') && request.method == 'POST')) {
    response.writeHead(404)
    response.end()
    return
  }

  // extract tag
  var tagFromUrl = ''
  var urlparts = request.url.split('/')
  if (urlparts.length >= 3) {
    tagFromUrl = urlparts[2]
  }

  var body = ''

  request.on('data', function (data) {
    body += data;

    if (body.length > 1e5) {
      request.connection.destroy()
      return
    }
  }).on('end', function () {
    console.log(body)
    // must be json
    try {
      x = JSON.parse(body)
      body = JSON.stringify(x)
    } catch (err){
      console.log(err);
      response.writeHead(406)
      response.end()
      return
    }

    const message = iota.utils.toTrytes(body)
  
    const transfers = [
     {
  	value: 0,
  	address: trytes,
  	message: message,
  	tag: iota.utils.toTrytes(tagFromUrl)
     }
    ]
  
    iota.api.sendTransfer(trytes, 3, 9, transfers, (error, success) => {
     if (error) {
  	console.log(error)
        response.writeHead(500)
        reponse.end(error)
     } else {
  	console.log(success)
        response.writeHead(200)
        response.end()
     }
    })
  });
}

const server = http.createServer(requestHandler)

server.listen(port, (err) => {
  if (err) {
    return console.log('ERROR ', err)
  }

  console.log(`server is listening on ${port}`)
})

