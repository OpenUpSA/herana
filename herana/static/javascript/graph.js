// var dataset = [
//   [5, 7, 3], [3, 6, 3], [3, 3, 4], [6, 9, 5], [1, 2, 6],
//   [4, 1, 5], [4, 4, 4], [2, 7, 3], [8, 1, 3], [2, 8, 4]
// ];

var dataset = [
  {"x": 5, "y": 7, "r": 3, "unit":"economics", "level": "department", "status":"ongoing"},
  {"x": 3, "y": 6, "r": 3, "unit":"law", "level": "department", "status":"complete"},
  {"x": 3, "y": 3, "r": 4, "unit":"science", "level": "department", "status":"ongoing"},
]

var results = RESULTS;

units = ["economics", "science", "law", "arts", "finance", "engineering", "psychology"]
levels = ["department", "school", "faculty"]

// Set the size of the graph
var w = 700;
var h = 700;
var padding = 150;


function iso_side(h) {
  // Given the length of the hypotenuse,
  // return the length of the equal sides
  // of a Right Isosceles triangle.
  return Math.sqrt((h * h) / 2)
}

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

var unitScale = d3.scale.category20()
  .domain(units);

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
svg.selectAll("circle")
  .data(results)
  .enter()
  .append("circle")
  .attr("cx", function(d) {
      return xScale(d.x);
   })
   .attr("cy", function(d) {
      return yScale(d.y);
   })
   .attr("r", function(d) {
      return d.r;
   })
   .attr("fill", function(d){
      return unitScale(d.unit);
   });

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
  .attr("transform", "rotate(90)")

svg.attr("transform", "rotate(-45, " + w/2 + ", " + h/2 + ")")
