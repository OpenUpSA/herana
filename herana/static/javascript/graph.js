var Graph = function() {
  var self = this;

  // Test data
  var test_data = [
    {"x": 5, "y": 7, "r": 0, "unit_id":"1", "level": "1", "status":"1", "institute": {"id": "1"}},
    {"x": 3, "y": 6, "r": 1, "unit_id":"3", "level": "1", "status":"2", "institute": {"id": "1"}},
    {"x": 6, "y": 1, "r": 2, "unit_id":"3", "level": "1", "status":"2", "institute": {"id": "1"}},
    {"x": 7, "y": 3, "r": 3, "unit_id":"4", "level": "1", "status":"2", "institute": {"id": "2"}},
    {"x": 2, "y": 5, "r": 4, "unit_id":"5", "level": "1", "status":"1", "institute": {"id": "2"}},
    {"x": 1, "y": 4, "r": 5, "unit_id":"1", "level": "2", "status":"1", "institute": {"id": "3"}},
    {"x": 7, "y": 6, "r": 3, "unit_id":"2", "level": "2", "status":"2", "institute": {"id": "2"}},
    {"x": 3, "y": 1, "r": 1, "unit_id":"3", "level": "2", "status":"2", "institute": {"id": "2"}},
  ]

  self.init = function() {
    // self.data = DATA;
    // self.results = self.data.results;
    // self.institutes = self.data.institutes;

    self.data = test_data;
    self.results = test_data;
    self.institutes = DATA.institutes;

    self.w = 700;
    self.h = 700;
    self.padding = 150;

    self.svg = d3.select("#graph")
      .append("svg")
      .attr("width", self.w)
      .attr("height", self.h);

    self.populateFilters()
    self.createScales();
    self.createAxes();
    self.drawAxes();

    self.attachData()
    self.filters = {
      institute: null
    }


    $('select[class=select-institute]').on('change', self.filterByInstitute);

  }

  self.populateFilters = function() {
    $.each(self.institutes, function(i, institute) {
      $('.select-institute').append($('<option>', {
        value: institute.id,
        text: institute.name
      }));
    });
  }


  self.filterByInstitute = function(e) {
    e.preventDefault();
    self.filters.institute = $(e.currentTarget).val() || null;
    self.filterAndDraw()
  }

  self.filterAndDraw = function() {
    var filters = self.filters;
    var results = self.data.results;

    if(self.filters.institute) {
      results = _.filter(results, function(result) {
        return result.institute.id == filters.institute
      });
    }
    self.results = results;
    self.attachData();
  }

  self.createScales = function() {
    var h = self.h,
        w = self.w,
        padding = self.padding;

    var hyp_length = function(x, y) {
      // Given the length of two side,
      // return the length of the hypotenuse
      // of a Right triangle.
      return Math.sqrt((x * x) + (y * y))
    }

    var getUnits = function () {
      var units = new Set();
      for (var i = 0; i < self.results.length; i++) {
        units.add(self.results[i].unit_id);
      }
      return units;
    }

    self.xScale = d3.scale.linear()
    .domain([0, 9])
    .range([padding, w-padding]);

    self.yScale = d3.scale.linear()
    .domain([0, 9])
    .range([h-padding, padding]);

    self.zScale = d3.scale.linear()
    .domain([0, 9])
    .range([0, hyp_length(self.xScale(9) - padding, self.yScale(0) - padding)]);

    self.rScale = d3.scale.linear()
    .domain([0, 4])
    .range([10, 30]);

    self.colorScale = d3.scale.category20()
    .domain(getUnits());

    self.discScale = d3.scale.linear()
    .domain([0, 4])
    .range([5, 15]);
  }

  self.createAxes = function () {
    self.xAxis = d3.svg.axis()
      .scale(self.xScale)
      .orient("bottom")
      .tickPadding(-4)
      .innerTickSize(0)
      .outerTickSize(0);

    self.yAxis = d3.svg.axis()
      .scale(self.yScale)
      .orient("left")
      .tickPadding(-4)
      .innerTickSize(0)
      .outerTickSize(0);

    self.zAxis = d3.svg.axis()
      .scale(self.zScale)
      .orient("bottom")
      .tickPadding(-4)
      .innerTickSize(0)
      .outerTickSize(0);
  }

  self.drawAxes = function () {
    var h = self.h,
        w = self.w,
        padding = self.padding,
        svg = self.svg;

    svg.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(0," + (h - self.yScale(4.5)) + ")")
      .call(self.xAxis)
      .selectAll("text")
      .attr("transform", "rotate(45)");

    svg.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(" + self.xScale(4.5) + ",0)")
      .call(self.yAxis)
      .selectAll("text")
      .attr("transform", "rotate(45)");

    // Draw gridlines
    svg.selectAll("line.horizontalGrid").data(self.yScale.ticks(9)).enter()
      .append("line")
      .attr({
        "class":"horizontalGrid grid",
        "x1" : padding,
        "x2" : w - padding,
        "y1" : function(d){ return self.yScale(d);},
        "y2" : function(d){ return self.yScale(d);},
      });

    svg.selectAll("line.verticalGrid").data(self.xScale.ticks(9)).enter()
      .append("line")
      .attr({
        "class":"verticalGrid grid",
        "y1" : padding,
        "y2" : h - padding,
        "x1" : function(d){ return self.xScale(d);},
        "x2" : function(d){ return self.xScale(d);},
      });

    var z_x = padding,
        z_y = h - padding;

    svg.append("g")
      .attr("class", "axis z-axis")
      .attr("transform",
            "translate(" + z_x + "," + z_y +") rotate(-45 0 0)")
      .call(self.zAxis)
      .selectAll("text")
      .attr("transform", "rotate(90)");

    self.svg.attr("transform", "rotate(-45, " + self.w/2 + ", " + self.h/2 + ")");
  }

  self.attachData = function () {
    var svg = self.svg,
        point = svg.selectAll("circle").data(self.results);

    point.exit()
      .transition().attr("r", 0).remove();

    point.enter()
      .append("circle")
      .attr("cx", function(d) {
          return self.xScale(d.x);
       })
       .attr("cy", function(d) {
          return self.yScale(d.y);
       })
       .attr("r", 0)
       .transition()
       .attr("r", function(d) {
          return self.rScale(d.r);
       })
       .attr("fill", function(d){
          return self.colorScale(d.unit_id);
       });

    var ongoing = svg.selectAll('circle.ongoing')
      .data(self.results.filter(
        function(d, i) {
          return d.status == '1';
        }));

    ongoing.exit().transition().attr("r", 0).remove();

    ongoing.enter()
      .append("circle")
      .attr("cx", function(d) {
          return self.xScale(d.x);
       })
       .attr("cy", function(d) {
          return self.yScale(d.y);
       })
       .attr("r", function(d) {
          return self.discScale(d.r);
       })
       .attr("fill", "#fff")
       .attr("class", "ongoing");
  }
}

var graph = new Graph();
graph.init()
