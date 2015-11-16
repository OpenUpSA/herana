var dataset = [
  [5, 7, 3], [3, 6, 3], [3, 3, 4], [6, 9, 5], [1, 2, 6],
  [4, 1, 5], [4, 4, 4], [2, 7, 3], [8, 1, 3], [2, 8, 4]
];

var w = 500;
var h = 500;
var padding = 30;

var svg = d3.select("#main-content")
  .append("svg")
  .attr("width", w)
  .attr("height", h);

var xScale = d3.scale.linear()
  .domain([0, 9])
  .range([padding, w - padding]);

var yScale = d3.scale.linear()
  .domain([0, 9])
  .range([h - padding, padding]);

var zScale = d3.scale.linear()
  .domain([0, 9])
  .range([padding, 700 - padding])

var xAxis = d3.svg.axis()
  .scale(xScale)
  .orient("bottom");

var yAxis = d3.svg.axis()
  .scale(yScale)
  .orient("left");

var zAxis = d3.svg.axis()
  .scale(zScale)
  .orient("bottom")
  .tickPadding(-3)
  .innerTickSize(0)
  .outerTickSize(0);

svg.selectAll("circle")
  .data(dataset)
  .enter()
  .append("circle")
  .attr("cx", function(d) {
      return xScale(d[0]);
   })
   .attr("cy", function(d) {
      return yScale(d[1]);
   })
   .attr("r", function(d) {
      return d[2];
   });

svg.append("g")
  .attr("class", "axis")
  .attr("transform", "translate(0," + (h - yScale(4.5)) + ")")
  .call(xAxis);

svg.append("g")
  .attr("class", "axis")
  .attr("transform", "translate(" + xScale(4.5) + ",0)")
  .call(yAxis);

svg.append("g")
  .attr("class", "axis")
  // .attr("transform", "translate(0," + (h - yScale(9)) + ") rotate(-45, " + w/2 + ", " + 0 + ")")
  .attr("transform", "translate(0, 500) rotate(-45)")
  .call(zAxis);

// svg.append('line')
//   .attr("class", "axis")
//   .attr('x1',xScale(0))
//   .attr('x2',xScale(9))
//   .attr('y1',h - yScale(9))
//   .attr('y2',yScale(9))

svg.attr("transform", "rotate(-45, " + w/2 + ", " + h/2 + ")")
