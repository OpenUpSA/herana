var Graph = function() {
  var self = this;

  // Test data

  var test_data = {"institutes": [{"org_level_1_name": "College", "org_level_3_name": "Department", "org_level_2_name": "School or Institute or Centre ", "id": 9, "name": "Makerere University"}, {"org_level_1_name": "Test", "org_level_3_name": "", "org_level_2_name": "", "id": 8, "name": "Test"}, {"org_level_1_name": "Faculty", "org_level_3_name": "", "org_level_2_name": "Department", "id": 10, "name": "University of Fort Hare"}, {"org_level_1_name": "College", "org_level_3_name": "Department", "org_level_2_name": "School, Institute or Centre", "id": 5, "name": "University of Ghana"}, {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}], "projects": [{"status": 1, "duration": 0, "score": [3.0, 4.75], "name": "National Programme on Sustainable Consumption and Production for Mauritius", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 10, "org_level_1": {"name": "Faculty of Engineering"}, "org_level_2": {"name": "Department of Civil Engineering (CE)"}}, {"status": 1, "duration": 0, "score": [2.5, 3.25], "name": "Development of value-added product from breadfruit", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 19, "org_level_1": {"name": "Faculty of Agriculture"}, "org_level_2": {"name": "Department of Agricultural Production & Systems (APS)"}}, {"status": 1, "duration": 0, "score": [4.0, 5.0], "name": "Green Economy Fiscal Policy Scoping Study", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 4, "org_level_1": {"name": "Faculty of Social Studies & Humanities"}, "org_level_2": {"name": "Department of Economics & Statistics"}}, {"status": 1, "duration": 2, "score": [5.25, 5.25], "name": "National Dialogue Session and Building Institutional Capacity of Mauritian and Seychelles Press", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 9, "org_level_1": {"name": "Faculty of Social Studies & Humanities"}, "org_level_2": {"name": "Department of Social Studies"}}, {"status": 2, "duration": 3, "score": [2.75, 5.5], "name": "Development of a seaweed industry in Mauritius and Rodrigues: Potential of local seaweeds as alternative feed ingredients in pig diets", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 8, "org_level_1": {"name": "Faculty of Agriculture"}, "org_level_2": {"name": "Department of Agricultural Production & Systems (APS)"}}, {"status": 1, "duration": 4, "score": [5.0, 4.25], "name": "Maurice Ile Durable project", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 11, "org_level_1": {"name": "Faculty of Engineering"}, "org_level_2": {"name": "Department of Mechanical and Production Engineering (MPE)"}}, {"status": 1, "duration": 1, "score": [7.5, 4.25], "name": "EMBEDDING WORK-BASED LEARNING AT THE UNIVERSITY", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 12, "org_level_1": {"name": "Centre for Innovative and Lifelong Learning (CILL)"}, "org_level_2": null}, {"status": 1, "duration": 0, "score": [3.0, 4.0], "name": "Workshop on solar dehydration of fruits and vegetables for SMEs", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 13, "org_level_1": {"name": "Faculty of Agriculture"}, "org_level_2": {"name": "Department of Agriculture and Food Science (AFS)"}}, {"status": 1, "duration": 0, "score": [0.0, 4.5], "name": "Training Programme for National Women Entrepreneur Council, Mauritius", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 14, "org_level_1": {"name": "Faculty of Engineering"}, "org_level_2": {"name": "Department of Applied Sustainability and Enterprise Development (DASED)"}}, {"status": 1, "duration": 1, "score": [3.0, 4.0], "name": "Setting-up of a Bio-based Industry in Mauritius", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 17, "org_level_1": {"name": "ANDI Centre for BioMaterials and Biomedical Research"}, "org_level_2": {"name": "Department of Chemistry"}}, {"status": 1, "duration": 0, "score": [6.0, 2.75], "name": "IAEA-UNESCO Project on Submarine Groundwater Discharge in Coastal Zones in Mauritius", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 15, "org_level_1": {"name": "Faculty of Science"}, "org_level_2": {"name": "Department of Chemistry"}}, {"status": 1, "duration": 2, "score": [5.0, 4.5], "name": "Developing Education, Skills and Capacity in Forensic Awareness and Forensic Science in the Southern African Development Community and Caribbean", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 16, "org_level_1": {"name": "Faculty of Science"}, "org_level_2": {"name": "Department of Chemistry"}}, {"status": 1, "duration": 0, "score": [1.25, 2.75], "name": "Action Plan to fight against Gender Based Violence in Rodrigues ", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 18, "org_level_1": {"name": "Faculty of Social Studies & Humanities"}, "org_level_2": {"name": "Department of Social Studies"}}, {"status": 2, "duration": 4, "score": [1.5, 4.5], "name": "Provision of Continuous Medical Education (CME) through the Medical Update Group", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 20, "org_level_1": {"name": "SSR Resource Centre"}, "org_level_2": {"name": "Department of Medicine"}}, {"status": 2, "duration": 3, "score": [3.25, 5.25], "name": "Diagnostic Test for Preeclampsia in Mauritius: Inositol Phosphoglycan-P type", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 21, "org_level_1": {"name": "Faculty of Science"}, "org_level_2": {"name": "Department of Medicine"}}, {"status": 2, "duration": 4, "score": [5.5, 3.75], "name": "Towards effective control of Buruli ulcer in Ghana-Stop BU", "institute": {"org_level_1_name": "College", "org_level_3_name": "Department", "org_level_2_name": "School, Institute or Centre", "id": 5, "name": "University of Ghana"}, "org_level_3": null, "id": 22, "org_level_1": {"name": "College of Health Sciences"}, "org_level_2": {"name": "Noguchi Memorial Institute for Medical Research"}}, {"status": 2, "duration": 1, "score": [1.5, 1.5], "name": "Beyond Domestic Violence Laws: Women's Experiences and Perceptions of Protection Services in Ghana", "institute": {"org_level_1_name": "College", "org_level_3_name": "Department", "org_level_2_name": "School, Institute or Centre", "id": 5, "name": "University of Ghana"}, "org_level_3": null, "id": 23, "org_level_1": {"name": "College of Humanities"}, "org_level_2": {"name": "Centre for Gender Studies and Advocacy"}}, {"status": 1, "duration": 0, "score": [2.0, 3.5], "name": "Inventory of hazardous wastes generated in Mauritius and recommendations on solutions for recycling and disposal", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 24, "org_level_1": {"name": "Faculty of Science"}, "org_level_2": {"name": "Department of Chemistry"}}, {"status": 1, "duration": 0, "score": [1.25, 4.0], "name": "Sustainable Management of Persistent Organic Pollutants (POPs) in Mauritius - Responsible Care Programme", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 3, "org_level_1": {"name": "Faculty of Science"}, "org_level_2": {"name": "Department of Chemistry"}}, {"status": 1, "duration": 1, "score": [4.5, 6.25], "name": "Clinical trial on  the effects of black tea consumption on Ischaemic heart diseases among the Mauritian population", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 25, "org_level_1": {"name": "Faculty of Science"}, "org_level_2": {"name": "Department of Biosciences"}}, {"status": 1, "duration": 0, "score": [3.0, 3.75], "name": "Sensory Integration and Multi-Sensory Stimulation ", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 26, "org_level_1": {"name": "Faculty of Science"}, "org_level_2": {"name": "Department of Health Sciences"}}, {"status": 1, "duration": 0, "score": [0.75, 3.25], "name": "Sustainable Waste Management Practices at Petit Verger Prison, Mauritius", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 27, "org_level_1": {"name": "Faculty of Engineering"}, "org_level_2": {"name": "Department of Chemical & Environmental Engineering (CEE)"}}, {"status": 1, "duration": 1, "score": [5.5, 3.75], "name": "SIDECAP Project (Staff Innovation in Distributed Education in Caribbean, African, and Pacific countries)", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 28, "org_level_1": {"name": "Centre for Innovative and Lifelong Learning (CILL)"}, "org_level_2": null}, {"status": 1, "duration": 0, "score": [2.0, 3.0], "name": "Unionisation in Mauritius", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 29, "org_level_1": {"name": "Faculty of Law & Management"}, "org_level_2": {"name": "Department of Management"}}, {"status": 1, "duration": 0, "score": [2.75, 3.5], "name": "Young Ambassadors for Chemistry (YAC): Developing Education Skills of the Secondary School Teachers and Public Awareness", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 30, "org_level_1": {"name": "Faculty of Science"}, "org_level_2": {"name": "Department of Chemistry"}}, {"status": 1, "duration": 1, "score": [2.0, 3.5], "name": "Mercury action plan for Mauritius", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 31, "org_level_1": {"name": "Faculty of Engineering"}, "org_level_2": {"name": "Department of Chemical & Environmental Engineering (CEE)"}}, {"status": 2, "duration": 4, "score": [6.75, 5.25], "name": "Setting up of a monolingual dictionary for Mauritian Creole ", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 32, "org_level_1": {"name": "Faculty of Social Studies & Humanities"}, "org_level_2": {"name": "Department of French Studies"}}, {"status": 2, "duration": 0, "score": [5.0, 3.25], "name": "ESEFA SAP ERP (The Enterprise Systems for Africa)", "institute": {"org_level_1_name": "Faculty or Centre", "org_level_3_name": "", "org_level_2_name": "Department", "id": 6, "name": "University of Mauritius"}, "org_level_3": null, "id": 35, "org_level_1": {"name": "Faculty of Engineering"}, "org_level_2": {"name": "Department of Mechanical and Production Engineering (MPE)"}}]}

  self.init = function() {
    // self.data = DATA;

    self.data = test_data;

    self.all_projects = self.institute_projects = self.data.projects;
    // self.institute_projects = null
    self.filtered_projects = null

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
  }

  self.getLevelUnits = function () {
    // Return a set of unique unit names,
    // which exist for the current chosen level,
    // for current instututes.

    var units = [],
        org_level = 'org_level_' + self.filters.org_level;

    var projects = _.filter(self.institute_projects, function(project) {
      return project[org_level]
    });

    _.each(projects, function(project){
      units.push(project[org_level].name);
    });
    return _.uniq(units);
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
    var instutute_id = $(this).val();
    self.resetFilters()

    // TODO: UPdate this code to store object in filters
    self.filters.institute = _.find(self.institutes, function(institute) {
        return institute.id == instutute_id;
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
