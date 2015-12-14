var Graph = function() {
  var self = this;

  self.init = function() {
    self.data = DATA;

    self.all_projects = self.data.projects;
    self.institute_projects = [];
    self.filtered_projects = [];

    self.institutes = self.data.institutes;

    self.resetFilters();

    self.w = 700;
    self.h = 700;
    self.svg_h = 900;
    self.padding = 150;
    self.stroke = 6;

    self.svg = d3.select("#graph")
      .append("svg")
      .attr("width", self.w)
      .attr("height", self.svg_h);
    self.svg.append("g").attr("class", "graph");
    self.svg.append("g").attr("class", "legend");

    self.updateInstitutes();
    self.units = [];

    self.createScales();
    self.createAxes();
    self.drawAxes();
    self.drawLegend();

    $('select[class=select-institute]').on('change', self.instituteChanged);
    $('select[class=select-org-level]').on('change', self.orgLevelChanged);
    $('select[class=select-status]').on('change', self.statusChanged);
    $('select[class=select-duration]').on('change', self.durationChanged);

    // Default to logged in user's institute.
    if (self.data.user_institute in self.institutes) {
      $('select[class=select-institute]').val(self.data.user_institute.id).change();
    }
  };

  self.resetFilters = function () {
    self.filters = {
      institute: null,
      org_level: "1",
      status: null,
      duration: null,
      units: {}
    };

    // Set status option to the default
    $('select[class=select-status]').val("");
  };

  self.getLevelUnits = function () {
    // Return a set of unique unit names,
    // which exist for the current chosen level,
    // for the current instutute.
    var org_level = 'org_level_' + self.filters.org_level;
    return _.uniq(
      _.map(
        _.filter(
          self.institute_projects, function(project) {
            return project[org_level];
          }),
        function(p) { return p[org_level].name; }));
  };

  self.updateInstitutes = function() {
    $.each(self.institutes, function(i, institute) {
      $('.select-institute').append($('<option>', {
        value: institute.id,
        text: institute.name
      }));
    });
  };

  self.updateOrgLevels = function() {
    var select = $('.select-org-level');

    select.find('option').remove();
    $.each([1,2,3], function(i, level) {
      var level_key = 'org_level_' + level + '_name'
      if (level_key in self.filters.institute) {
        select.append($('<option>', {
          value: level,
          text: self.filters.institute[level_key]
        }));
      }
    });
  };

  self.updateUnits = function () {
    self.units = self.getLevelUnits();
    self.filters.units = {};
    _.each(self.units, function(u) {
      self.filters.units[u] = true;
    });
  };

  self.instituteChanged = function() {
    var institute_id = $(this).val();
    self.resetFilters();

    self.filters.institute = _.find(self.institutes, function(institute) {
        return institute.id == institute_id;
    });

    self.institute_projects = _.filter(self.all_projects, function(project) {
        return project.institute.id == self.filters.institute.id;
    });

    self.updateOrgLevels();

    self.updateUnits();
    self.drawUnitLegend();

    self.filterAndDrawProjects();
  };

  self.orgLevelChanged = function() {
    self.filters.org_level = $(this).val() || null;
    self.updateUnits();
    self.drawUnitLegend();
    self.filterAndDrawProjects();
  };

  self.statusChanged = function() {
    self.filters.status = $(this).val() || null;
    self.filterAndDrawProjects();
  };

  self.durationChanged = function() {
    self.filters.duration = $(this).val() || null;
    self.filterAndDrawProjects();
  };

  self.unitChanged = function(d) {
    self.filters.units[d] = !self.filters.units[d];
    self.filterAndDrawProjects();
  };

  self.filterAndDrawProjects = function() {
    var filters = self.filters;

    // All unfiltered projects for currrent institute
    var projects = self.institute_projects;

    // org level
    if (self.filters.org_level) {
      projects = _.filter(projects, function(project) {
        return project['org_level_' + self.filters.org_level];
      });
    }

    // status
    if (self.filters.status) {
      projects = _.filter(projects, function(project) {
        return project.status == self.filters.status;
      });
    }

    // duration
    if (self.filters.duration) {
      projects = _.filter(projects, function(project) {
        return project.duration == self.filters.duration;
      });
    }

    // units
    projects = _.filter(projects, function(p) {
      var org = p['org_level_' + self.filters.org_level];
      return org && self.filters.units[org.name];
    });

    self.filtered_projects = _.sortBy(projects, 'duration').reverse();
    self.drawResults();
  };

  self.createScales = function() {
    var h = self.h,
        w = self.w,
        padding = self.padding;

    var hyp_length = function(x, y) {
      // Given the length of two side,
      // return the length of the hypotenuse
      // of a Right triangle.
      return Math.sqrt((x * x) + (y * y));
    };

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
    .range([5, 25]);

    self.colorScale = d3.scale.category20()
    .domain(self.units);

    self.discScale = d3.scale.linear()
    .domain([0, 4])
    .range([5, 15]);
  };

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
  };

  self.drawAxes = function () {
    var h = self.h,
        w = self.w,
        padding = self.padding,
        svg = self.svg.select(".graph");

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

    // Draw the labels
    svg.append("text")
      .attr("class", "x label")
      .attr("x", w - (padding - 20))
      .attr("y", h - self.yScale(4.5))
      .text("Strengthening the academic core")
      .attr("transform", "rotate(45,"+ (w - (padding - 20)) + "," + (h - self.yScale(4.5)) + ")");

    svg.append("text")
      .attr("class", "x label")
      .attr("text-anchor", "end")
      .attr("x", padding - 20)
      .attr("y", h - self.yScale(4.5))
      .text("Weakening the academic core")
      .attr("transform", "rotate(45,"+ ((padding - 20)) + "," + (h - self.yScale(4.5)) + ")");

    svg.append("text")
      .attr("class", "y label")
      .attr("text-anchor", "end")
      .attr("x", w - self.xScale(4.5))
      .attr("y", padding - 25)
      .attr("transform", "rotate(45,"+ ((w - self.xScale(4.5))) + "," + (padding - 20) + ")")
      .text("Strong articulation");

    svg.append("text")
      .attr("class", "y label")
      .attr("x", w - self.xScale(4.5))
      .attr("y", h - (padding - 20))
      .attr("transform", "rotate(45,"+ ((w - self.xScale(4.5))) + "," + (h - (padding - 20)) + ")")
      .text("Weak articulation");

    svg.append("text")
      .attr("class", "z label")
      .attr("text-anchor", "middle")
      .attr("x", w - (padding - 20))
      .attr("y", padding - 20)
      .text("Interconnected")
      .attr("transform", "rotate(45,"+ (w - (padding - 20)) + "," + (padding - 20) + ")");

    svg.append("text")
      .attr("class", "z label")
      .attr("text-anchor", "middle")
      .attr("x", padding - 20)
      .attr("y", h - (padding - 20))
      .text("Disconnected")
      .attr("transform", "rotate(45,"+ (padding - 20) + "," + (h - (padding - 20)) + ")");

    // Rotate the graph
    svg.attr("transform", "rotate(-45, " + self.w/2 + ", " + self.h/2 + ")");
  };

  self.drawLegend = function() {
    var svg = self.svg.select(".legend"),
        legendHeight = 260,
        legendWidth = 150,
        ongoing_x = 40,
        complete_x = 100,
        label_x = 140;

    svg.attr("transform", "translate(0, " + (self.svg_h - legendHeight - 1) + ")");

    svg.append("rect")
      .attr({
        x: 0,
        y: 0,
        width: legendWidth,
        height: legendHeight,
      });

    // titles
    var txt = svg.append("text")
      .attr("class", "label legend")
      .attr("text-anchor", "middle")
      .attr("x", legendWidth / 2)
      .attr("y", 10)
      .attr("text-ancher", "middle")
      .text("Duration of project (years)");

    svg.append("text")
      .attr("text-anchor", "middle")
      .attr("dy", legendHeight - 2)
      .attr("dx", ongoing_x)
      .text("Ongoing");
    svg.append("text")
      .attr("text-anchor", "middle")
      .attr("dy", legendHeight - 2)
      .attr("dx", complete_x)
      .text("Complete");

    // year labels
    var labels = ['0-1.99', '2-2.99', '3-3.99', '4-4.99', '5+'],
        years = [];

    for (var i = 0; i < labels.length; i++) {
      var y = i === 0 ? legendHeight - 10 : years[years.length-1].y;
      years.push({
        i: i,
        y: y - self.rScale(i) * 2 - 8,
        label: labels[i],
      });
    }

    // Ongoing circles
    svg.selectAll("circle.ongoing").data(years).enter()
      .append("circle")
      .attr({
        class: "ongoing",
        cx: ongoing_x,
        cy: function(d) { return d.y; },
        r: function(d) { return self.rScale(d.i) - self.stroke / 2; },
        fill: 'none',
        stroke: '#ccc',
        'stroke-width': self.stroke,
      });

    // Complete circles
    svg.selectAll("circle.complete").data(years).enter()
      .append("circle")
      .attr({
        class: "complete",
        cx: complete_x,
        cy: function(d) { return d.y; },
        r: function(d) { return self.rScale(d.i); },
        fill: '#ccc',
      });

    // year labels
    svg.selectAll(".years").data(years).enter()
      .append("text")
      .attr("class", "label")
      .attr("text-ancher", "middle")
      .attr("x", label_x)
      .attr("y", function(d) { return d.y + 5; })
      .text(function(d) { return d.label; });
  };

  self.drawUnitLegend = function () {
    // Set scale to current units
    self.colorScale = d3.scale.category20()
      .domain(self.units);

    $('#units').children().remove();
    var svg = d3.select("#units")
      .append("svg")
      .attr('class', 'unit-legend');

    var colorLegend = d3.legend.color()
      .scale(self.colorScale)
      .shape('circle')
      .on('cellclick', function(d) {
        self.unitChanged(d);
      });

    svg.call(colorLegend);
  };

  self.drawResults = function () {
    var svg = self.svg.select(".graph"),
        point = svg.selectAll("circle").data(self.filtered_projects, function(d) { return d.id; }).order();

    point.exit()
      .transition().attr("r", 0).remove();

    point.enter()
      .append("circle")
      .attr("cx", function(d) {
          return self.xScale(d.score['x']);
       })
       .attr("cy", function(d) {
          return self.yScale(d.score['y']);
       })
       .attr("r", 0)
       .transition()
       .attr("r", function(d) {
          var r = self.rScale(d.duration);
          // ensure outer edge of stroke is at where the edge of a filled circle would be
          if (d.status == '1') r -= self.stroke / 2;
          return r;
       })
       .attr("fill", function(d) {
          // no fill for ongoing
          return d.status == '1' ? 'none' : self.colorScale(d['org_level_' + self.filters.org_level].name);
       })
       .attr("stroke", function(d) {
          // stroke only for ongoing
          return d.status == '1' ? self.colorScale(d['org_level_' + self.filters.org_level].name) : 'none';
       })
       .attr("stroke-width", self.stroke);
       point.on("mouseover", self.showTooltip);
       point.on("mouseout", self.removeTooltip);
  };

  self.showTooltip = function (d) {
    $(this).popover({
    placement: 'auto top',
    container: '#graph',
    trigger: 'manual',
    html : true,
    content: function() {
      return "<span style='font-size: 11px; text-align: center;'>" + d.name + "</span>"; }
    });
    $(this).popover('show');
  };

  self.removeTooltip = function () {
    $('.popover').each(function() {
      $(this).remove();
    });
  };
};

var graph = new Graph();
graph.init();
