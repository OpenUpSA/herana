var Graph = function() {
  var self = this;

  self.init = function() {
    self.data = DATA;

    self.all_projects = self.data.projects;
    self.institute_projects = []
    self.filtered_projects = []

    self.institutes = self.data.institutes;

    self.resetFilters()

    self.w = 700;
    self.h = 700;
    self.padding = 150;
    self.stroke = 6;

    self.svg = d3.select("#graph")
      .append("svg")
      .attr("width", self.w)
      .attr("height", self.h)
      .append("g");

    self.updateInstitutes()
    self.units = self.getLevelUnits()

    self.createScales();
    self.createAxes();
    self.drawAxes();

    $('select[class=select-institute]').on('change', self.instituteChanged);
    $('select[class=select-org-level]').on('change', self.orgLevelChanged);
    $('select[class=select-status]').on('change', self.statusChanged);
    $('.units').on('click', 'input[type=checkbox]', self.unitChanged);
  }

  self.resetFilters = function () {
    self.filters = {
      institute: null,
      org_level: "1",
      // map from unit name to true/false
      units: {},
    }

    // Set status select option to the default
    $('select[class=select-status]').val("");
  }

  self.getLevelUnits = function () {
    // Return a set of unique unit names,
    // which exist for the current chosen level,
    // for current instututes.
    var org_level = 'org_level_' + self.filters.org_level
    return _.uniq(
      _.map(
        _.filter(
          self.institute_projects, function(project) {
            return project[org_level]
          }),
        function(p) { return p[org_level].name; }));
  }

  self.updateInstitutes = function() {
    $.each(self.institutes, function(i, institute) {
      $('.select-institute').append($('<option>', {
        value: institute.id,
        text: institute.name
      }));
    });
  }

  self.updateOrgLevels = function() {
    var select = $('.select-org-level');

    select.find('option').remove();
    $.each([1,2,3], function(i, level) {
      select.append($('<option>', {
        value: level,
        text: self.filters.institute['org_level_' + level + '_name']
      }))
    });
  }

  self.updateUnits = function () {
    self.units = self.getLevelUnits()
    self.filters.units = {};
    _.each(self.units, function(u) {
      self.filters.units[u] = true;
    })

    $('.units').children().remove();
    $.each(self.units, function(i, unit) {
      $('.units')
        .append($('<li class="checkbox"><label><input type="checkbox" checked value="' + unit + '"> ' + unit + '</label>'));
      });
  }

  self.instituteChanged = function() {
    var institute_id = $(this).val();
    self.resetFilters()

    self.filters.institute = _.find(self.institutes, function(institute) {
        return institute.id == institute_id;
    });

    self.institute_projects = _.filter(self.all_projects, function(project) {
        return project.institute.id == self.filters.institute.id
    });

    self.updateOrgLevels()
    self.updateUnits()
    self.filterAndDrawProjects()
  }

  self.orgLevelChanged = function() {
    self.filters.org_level = $(this).val() || null;
    self.updateUnits()
    self.filterAndDrawProjects();
  };

  self.statusChanged = function() {
    self.filters.status = $(this).val() || null;
    self.filterAndDrawProjects();
  };

  self.unitChanged = function(e) {
    var $chk = $(this);
    self.filters.units[$chk.val()] = $chk.prop('checked');
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

    // units
    projects = _.filter(projects, function(p) {
      var org = p['org_level_' + self.filters.org_level];
      return org && self.filters.units[org.name];
    });

    self.projects = projects;
    self.drawResults()
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
    .domain(self.units);

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
      .attr("y", padding - 20)
      .text("Strong articulation")
      .attr("transform", "rotate(45,"+ ((w - self.xScale(4.5))) + "," + (padding - 20) + ")");

    svg.append("text")
      .attr("class", "y label")
      .attr("x", w - self.xScale(4.5))
      .attr("y", h - (padding - 20))
      .text("Weak articulation")
      .attr("transform", "rotate(45,"+ ((w - self.xScale(4.5))) + "," + (h - (padding - 20)) + ")");

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
    self.svg.attr("transform", "rotate(-45, " + self.w/2 + ", " + self.h/2 + ")");
  }

  self.drawResults = function () {
    var svg = self.svg,
        point = svg.selectAll("circle").data(self.projects, function(d) { return d.id });

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
       .attr("stroke-width", self.stroke)
       .attr("z", function(d){
          // Display smaller circles above larger ones.
          return 100 / self.rScale(d.duration);
      });
  }
}

var graph = new Graph();
graph.init()
