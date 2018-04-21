var data = require('./data.js')
var d3KitTimeline = require('d3kit-timeline');

document.getElementById("name").innerHTML = data.name;

const colorScale = d3.scaleOrdinal(d3.schemeCategory10);
function color(d){
  return colorScale(d.name);
}
console.log(data.name);
var chart = new d3KitTimeline('#chart-timeline', {
  direction: 'down',
  initialWidth: 1000,
  margin: {left: 20, right: 20, top: 30, bottom: 20},
  textFn: d => d.name,
  layerGap: 40,
  dotColor: color,
  labelBgColor: color,
  linkColor: color,
  labella: {
    maxPos: 800,
    algorithm: 'simple'
  }
});
chart.data(data.timeline_data).visualize().resizeToFit();
