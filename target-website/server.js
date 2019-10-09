var port = 8080;
var http = require('http');          // core node.js http (no frameworks)
var url = require('url');            // core node.js url (no frameworks)
var app  = require('./lib/helpers'); // auth, token verification & render helpers
var c    = function(res){ /*  */ };

process.on('SIGINT', function() {
  console.log( "\nGracefully shutting down from SIGINT (Ctrl-C)" );
  process.exit(1);
});

http.createServer(function (req, res) {
  var path = url.parse(req.url).pathname;
  if( path === '/' || path === '/home' ) { app.home(res);           } // homepage
  else if( path === '/auth')    { app.handler(req, res);            } // authenticator
  else if( path === '/private') { app.validate(req, res, app.done); } // private content
  else if( path === '/logout')  { app.logout(req, res, app.done);   } // end session
  else                          { app.notFound(res);                } // 404 error
}).listen(port);

console.log("The server is running at " + port);