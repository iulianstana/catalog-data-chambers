var path = require('path'),
    express = require('express');

var app = express();

app.get('/', function(req, res) {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/build/bundle.js', function(req, res) {
  res.sendFile(path.join(__dirname, '/build/bundle.js'));
});

app.listen(80, '0.0.0.0', function(err) {
  if (err) {
    console.log(err);
    return;
  }

  console.log('Listening at localhost:80');
});
