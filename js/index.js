var d3KitTimeline = require('d3kit-timeline');
var JSONData = require('./getdata.js')

function initChart() {
    const colorScale = d3.scaleOrdinal(d3.schemeCategory10);
    function color(d){
        return colorScale(d.name);
    }
    return new d3KitTimeline('#chart-timeline', {
        direction: 'down',
        initialWidth: 1000,
        margin: {left: 30, right: 30, top: 30, bottom: 20},
        textFn: d => d.name,
        layerGap: 40,
        dotColor: color,
        labelBgColor: color,
        linkColor: color,
        labella: {
            maxPos: 800,
            algorithm: 'simple'
        },
        textStyle: {
            'fill': '#eee',
        }
    });
}

function CapitalizeString(word) {
    return word.charAt(0).toUpperCase() + word.slice(1);
}

function showMembershipTimeline(timelineData) {
    var chart = initChart();
    timelineData(function(data) {
        person = data[0]
        var timeline_data = [];
        name = person['name']
        activity = person['acitivity']
        activity.forEach(function(item){
            var formation = item['formation']
            var since = new Date(item['since']['year'], item['since']['month']-1, 1)
            var until = new Date(item['until']['year'], item['until']['month']-1, 1)
            if (formation === 'independent') {
                timeline_data.push({time: since, name: CapitalizeString(formation)})
            }
            else {
                timeline_data.push({time: since, name: 'Joined ' + formation})
            }
            if (until < new Date()) {
                timeline_data.push({time: until, name: 'Left ' + formation})
            }
            else {
                until = new Date()
                timeline_data.push({time: until, name: 'Still ' + formation})
            }
        });
        chart.data(timeline_data).visualize().resizeToFit();
    });
}

showMembershipTimeline(JSONData)
