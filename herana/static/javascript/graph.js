var dataset = [
  {"x": 5, "y": 7, "r": 0, "unit_id":"1", "level": "1", "status":"1"},
  {"x": 3, "y": 6, "r": 1, "unit_id":"3", "level": "1", "status":"2"},
  {"x": 6, "y": 1, "r": 2, "unit_id":"3", "level": "1", "status":"2"},
  {"x": 7, "y": 3, "r": 3, "unit_id":"4", "level": "1", "status":"2"},
  {"x": 2, "y": 5, "r": 4, "unit_id":"5", "level": "1", "status":"1"},
]

var results = dataset;

function get_units(results) {
  var units = new Set();
  for (var i = 0; i < results.length; i++) {
    units.add(results[i].unit_id);
  }
  return units;
}

var units = get_units(results);

// Set the size of the graph
var w = 700;
var h = 700;
var padding = 150;


function hyp_length(x, y) {
  // Given the length of two side,
  // return the length of the hypotenuse
  // of a Right triangle.
  return Math.sqrt((x * x) + (y * y))
}

// Where the graph will be attached
var svg = d3.select("#graph")
  .append("svg")
  .attr("width", w)
  .attr("height", h);

// Set the scales
var xScale = d3.scale.linear()
  .domain([0, 9])
  .range([padding, w-padding]);

var yScale = d3.scale.linear()
  .domain([0, 9])
  .range([h-padding, padding]);

var zScale = d3.scale.linear()
  .domain([0, 9])
  .range([0, hyp_length(xScale(9) - padding, yScale(0) - padding)]);

var rScale = d3.scale.linear()
  .domain([0, 4])
  .range([10, 30])

var colorScale = d3.scale.category20()
  .domain(units);

var discScale = d3.scale.linear()
  .domain([0, 4])
  .range([5, 15])


// Create the axes
var xAxis = d3.svg.axis()
  .scale(xScale)
  .orient("bottom")
  .tickPadding(-4)
  .innerTickSize(0)
  .outerTickSize(0);

var yAxis = d3.svg.axis()
  .scale(yScale)
  .orient("left")
  .tickPadding(-4)
  .innerTickSize(0)
  .outerTickSize(0);

var zAxis = d3.svg.axis()
  .scale(zScale)
  .orient("bottom")
  .tickPadding(-4)
  .innerTickSize(0)
  .outerTickSize(0);


// Attach the data
var circle = svg.selectAll("circle").data(results);

circle.exit()
  .transition().attr("r", 0).remove();

circle.enter()
  .append("circle")
  .attr("cx", function(d) {
      return xScale(d.x);
   })
   .attr("cy", function(d) {
      return yScale(d.y);
   })
   .attr("r", 0)
   .transition()
   .attr("r", function(d) {
      return rScale(d.r);
   })
   .attr("fill", function(d){
      return colorScale(d.unit_id);
   });

// svg.data(results.filter(
//     function(d, i) {
//       return d.status == '1';
//     }))
//   .enter()
//   .append("circle")
//   .attr("cx", function(d) {
//       return xScale(d.x);
//    })
//    .attr("cy", function(d) {
//       return yScale(d.y);
//    })
//    .attr("r", function(d) {
//       return discScale(d.r);
//    })
//    .attr("fill", "#fff");

svg.append("g")
  .attr("class", "axis")
  .attr("transform", "translate(0," + (h - yScale(4.5)) + ")")
  .call(xAxis)
  .selectAll("text")
  .attr("transform", "rotate(45)");

svg.append("g")
  .attr("class", "axis")
  .attr("transform", "translate(" + xScale(4.5) + ",0)")
  .call(yAxis)
  .selectAll("text")
  .attr("transform", "rotate(45)");

svg.selectAll("line.horizontalGrid").data(yScale.ticks(9)).enter()
    .append("line")
        .attr(
        {
            "class":"horizontalGrid grid",
            "x1" : padding,
            "x2" : w - padding,
            "y1" : function(d){ return yScale(d);},
            "y2" : function(d){ return yScale(d);},
        });

svg.selectAll("line.verticalGrid").data(xScale.ticks(9)).enter()
    .append("line")
        .attr(
        {
            "class":"verticalGrid grid",
            "y1" : padding,
            "y2" : h - padding,
            "x1" : function(d){ return xScale(d);},
            "x2" : function(d){ return xScale(d);},
        });

var z_x = padding,
    z_y = h - padding;

svg.append("g")
  .attr("class", "axis z-axis")
  .attr("transform",
        "translate(" + z_x + "," + z_y +") rotate(-45 0 0)")
  .call(zAxis)
  .selectAll("text")
  .attr("transform", "rotate(90)");

svg.attr("transform", "rotate(-45, " + w/2 + ", " + h/2 + ")");
