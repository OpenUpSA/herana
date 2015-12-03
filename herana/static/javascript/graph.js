var Graph = function() {
  var self = this;

  // Test data
  // var test_data = {
  //   'results':[
  //   {"x": 5, "y": 7, "r": 0, "unit_id":"1", "level": "1", "status":"1", "institute": {"id": "1"}},
  //   {"x": 3, "y": 6, "r": 1, "unit_id":"3", "level": "1", "status":"2", "institute": {"id": "1"}},
  //   {"x": 6, "y": 1, "r": 2, "unit_id":"3", "level": "1", "status":"2", "institute": {"id": "1"}},
  //   {"x": 7, "y": 3, "r": 3, "unit_id":"4", "level": "1", "status":"2", "institute": {"id": "2"}},
  //   {"x": 2, "y": 5, "r": 4, "unit_id":"5", "level": "1", "status":"1", "institute": {"id": "2"}},
  //   {"x": 1, "y": 4, "r": 5, "unit_id":"1", "level": "2", "status":"1", "institute": {"id": "3"}},
  //   {"x": 7, "y": 6, "r": 3, "unit_id":"2", "level": "2", "status":"2", "institute": {"id": "2"}},
  //   {"x": 3, "y": 1, "r": 1, "unit_id":"3", "level": "2", "status":"2", "institute": {"id": "2"}},
  //   ]
  // }


  self.init = function() {
    // self.data = DATA;
    // self.results = self.data.results;
    // self.institutes = self.data.institutes;

    self.data = test_data;
    self.results = self.data.results;
    self.institutes = self.data.institutes;

    self.w = 700;
    self.h = 700;
    self.padding = 150;

    self.selected_institute = null;
    self.org_level = 1;

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
      institute: null,
      org_level: null
    }

    $('select[class=select-institute]').on('change', self.filterByInstitute);
    $('select[class=select-org-level]').on('change', self.filterByOrgLevel);

  }

  self.populateFilters = function() {
    $.each(self.institutes, function(i, institute) {
      $('.select-institute').append($('<option>', {
        value: institute.id,
        text: institute.name
      }));
    });
  }

  self.populateOrgLevelsFilter = function () {
    var select = $('.select-org-level');

    select.find('option').remove().end();
    $.each([1,2,3], function(i, level) {
      select.append($('<option>', {
        value: level,
        text: self.selected_institute['org_level_' + level + '_name']
      }))
    });
    self.filters.org_level = select.first('option').val();
  }

  self.filterByInstitute = function(e) {
    e.preventDefault();
    self.filters.institute = $(e.currentTarget).val() || null;

    self.selected_institute = _.find(self.institutes, function(institute) {
        return institute.id == self.filters.institute
    });

    self.populateOrgLevelsFilter()
    self.filterAndDraw()
  }

  self.filterByOrgLevel = function(e) {
    e.preventDefault();
    self.filters.org_level = $(e.currentTarget).val() || null;

    self.filterAndDraw();
  }

  self.filterAndDraw = function() {
    var filters = self.filters;
    // All unfiltered results
    var results = self.data.results;

    if(self.filters.institute) {
      results = _.filter(results, function(result) {
        return result.institute.id == filters.institute
      });
    }

    if(self.filters.org_level) {
      results = _.filter(results, function(result) {
        return result['org_level_' + self.filters.org_level];
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

    var getLevelUnits = function () {
      // Return a set of unique unit names which exist for the current chosen level.
      var units = new Set();
      var org_level = 'org_level_' + self.org_level
      for (var i = 0; i < self.results.length; i++) {
        units.add(self.results[i][org_level].name);
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
    .domain(getLevelUnits());

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
          return self.xScale(d.score[0]);
       })
       .attr("cy", function(d) {
          return self.yScale(d.score[1]);
       })
       .attr("r", 0)
       .transition()
       .attr("r", function(d) {
          return self.rScale(d.duration);
       })
       .attr("fill", function(d){
          return self.colorScale(d['org_level_' + self.org_level].name);
       })
       .attr("z", function(d){
          // Display smaller circles above larger ones.
          return 100 / self.rScale(d.duration);
      });

    // var ongoing = svg.selectAll('circle.ongoing')
    //   .data(self.results.filter(
    //     function(d, i) {
    //       return d.status == '1';
    //     }));

    // ongoing.exit().transition().attr("r", 0).remove();

    // ongoing.enter()
    //   .append("circle")
    //   .attr("cx", function(d) {
    //       return self.xScale(d.score[0]);
    //    })
    //    .attr("cy", function(d) {
    //       return self.yScale(d.score[1]);
    //    })
    //    .attr("r", function(d) {
    //       return self.discScale(d.duration);
    //    })
    //    .attr("fill", "#fff")
    //    .attr("class", "ongoing");
  }
}

var graph = new Graph();
graph.init()
