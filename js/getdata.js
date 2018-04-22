var http = require("http");
var querystring = require('querystring');
var config = require("./config.js");

options = config.getEnvironment()['data_service']

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

var name = getParameterByName('name');
document.getElementById("name").innerHTML = name;

function getJsonData(callback) {
    options.path = options.path + window.location.search;
    return http.get(options, function(response) {
        var body = '';
        response.on('data', function(d) {
            body += d;
        });
        response.on('end', function() {
            // Data reception is done, do whatever with it!
            var parsed = JSON.parse(body);
            callback(parsed);
        });
    });
};

module.exports = getJsonData;
