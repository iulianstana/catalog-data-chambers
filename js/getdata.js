var http = require("http");
var config = require("./config.js");

options = config.getEnvironment()['data_service']

function getJsonData(callback) {

    return http.get(options, function(response) {
        var body = '';
        response.on('data', function(d) {
            body += d;
        });
        response.on('end', function() {
            // Data reception is done, do whatever with it!
            var parsed = JSON.parse(body);
            //console.log(parsed);
            callback(parsed);
        });
    });
};

module.exports = getJsonData;
