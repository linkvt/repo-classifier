var SELECT_SVG = 'svg#vis-features';

if (!d3.select(SELECT_SVG).empty()) {
    var vis_margin = {
            top: 40,
            right: 200,
            bottom: 30,
            left: 120
        },
        vis_width = 1200 - vis_margin.left - vis_margin.right,
        vis_height = 600 - vis_margin.top - vis_margin.bottom;
    var vis_x = d3.scale.linear()
        .range([0, vis_width]);
    var vis_y = d3.scale.linear()
        .range([vis_height, 0]);
    var vis_xAxis = d3.svg.axis()
        .scale(vis_x)
        .orient("bottom");
    var vis_yAxis = d3.svg.axis()
        .scale(vis_y)
        .orient("left");
    var vis_color = d3.scale.category10();
    var vis_svg = d3.select("svg#vis-features");
    var vis_tip = d3.tip().attr('class', 'd3-tip').html(function (d) {
        return d.name.slice(19) + "<br>" + X_FEATURE + ": " + d[X_FEATURE] + "<br>" + Y_FEATURE + ': ' + d[Y_FEATURE];
    });

    var X_FEATURE = 'Number of branches';
    var Y_FEATURE = 'Size of repo';

    var features = [];
    var main_data;
    var updatePlot = function (x_max, y_max) {
        x_max = +d3.select('#x_max').property('value');
        y_max = +d3.select('#y_max').property('value');

        vis_x.domain([0, x_max]).nice();
        vis_y.domain([0, y_max]).nice();
        vis_svg.selectAll('.dot').remove();
        vis_svg.selectAll('g').remove();
        buildPlot();
    };

    var buildPlot = function () {
        data = main_data;
        vis_xAxis = d3.svg.axis()
            .scale(vis_x)
            .orient("bottom");
        vis_yAxis = d3.svg.axis()
            .scale(vis_y)
            .orient("left");

        vis_svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + vis_height + ")")
            .call(vis_xAxis)
            .append("text")
            .attr("class", "label")
            .attr("x", vis_width)
            .attr("y", -6)
            .style("text-anchor", "end")
            .text(X_FEATURE);
        vis_svg.append("g")
            .attr("class", "y axis")
            .call(vis_yAxis)
            .append("text")
            .attr("class", "label")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text(Y_FEATURE);
        vis_svg.selectAll(".dot")
            .data(data)
            .enter().append("circle")
            .attr("class", function (d, i) {
                return 'dot ' + d.category;
            })
            .attr("r", 5)
            .attr("cx", function (d) {
                return vis_x(d[X_FEATURE]) + Math.random() * 6;
            })
            .attr("cy", function (d) {
                return vis_y(d[Y_FEATURE]) + Math.random() * 6;
            })
            .style("fill", function (d, i) {
                return vis_color(d.category);
            })
            .on('mouseover', vis_tip.show)
            .on('mouseout', vis_tip.hide)
            .on('click', function (d) {
                window.open(d.name);
            });
        var legend = vis_svg.selectAll(".legend")
            .data(vis_color.domain())
            .enter().append("g")
            .attr("class", "legend")
            .attr("transform", function (d, i) {
                return "translate(50," + i * 20 + ")";
            });
        legend.append("rect")
            .attr("x", vis_width - 18)
            .attr("width", 18)
            .attr("height", 18)
            .style("fill", vis_color)
            .on('mouseover', function (d) {
                var box = d3.select(this);
                var deselected = +box.attr('deselected') == 1;
                if (!deselected) {
                    vis_svg.selectAll('.dot').style('opacity', 0);
                    vis_svg.selectAll('.' + d).style('opacity', 0.4);
                }
            })
            .on('mouseout', function (d, i) {
                vis_svg.selectAll('.dot').style('opacity', 0.4);
            })
            .on('click', function (d) {
                var box = d3.select(this);
                var deselected = +box.attr('deselected') == 1;
                if (!deselected) {
                    vis_svg.selectAll('.dot').style('opacity', 0.4);
                    vis_svg.selectAll('.' + d).style('visibility', 'hidden');
                    box.style('opacity', 0.3);
                    box.attr('deselected', 1);
                } else {
                    vis_svg.selectAll('.' + d).style('visibility', 'visible');
                    box.style('opacity', 1);
                    box.attr('deselected', 0);
                }
            });
        legend.append("text")
            .attr("x", vis_width - 24)
            .attr("y", 9)
            .attr("dy", ".35em")
            .style("text-anchor", "end")
            .text(function (d) {
                return d;
            });
        for (var i = 0; i < features.length; i++) {
            var feature = features[i];
            d3.select('#features').append('option').text(feature).attr();
        }
        var x_options = d3.select('#x_features').selectAll('option')
            .data(features);
        x_options.enter()
            .append('option')
            .text(function (d) {
                return d;
            });
        var y_options = d3.select('#y_features').selectAll('option')
            .data(features);
        y_options.enter()
            .append('option')
            .text(function (d) {
                return d;
            });
        d3.select('#x_features')
            .on('change', function () {
                var si = d3.select(this).property('selectedIndex'),
                    s = x_options.filter(function (d, i) {
                        return i === si
                    }),
                    data = s.datum();
                X_FEATURE = data;
                d3.select('#x_max').property('value', d3.max(main_data, function (d) {
                    return +d[X_FEATURE]
                }));
                updatePlot();
            });
        d3.select('#y_features')
            .on('change', function () {
                var si = d3.select(this).property('selectedIndex'),
                    s = x_options.filter(function (d, i) {
                        return i === si
                    }),
                    data = s.datum();
                Y_FEATURE = data;
                d3.select('#y_max').property('value', d3.max(main_data, function (d) {
                    return +d[Y_FEATURE]
                }));
                updatePlot();
            });
        d3.select('#x_max')
            .on('change', function () {
                updatePlot();
            });
        d3.select('#y_max')
            .on('change', function () {
                updatePlot();
            });
        d3.select('#x_features').property('value', X_FEATURE);
        d3.select('#y_features').property('value', Y_FEATURE);
    };

    vis_svg.attr("width", vis_width + vis_margin.left + vis_margin.right)
        .attr("height", vis_height + vis_margin.top + vis_margin.bottom)
        .append("g")
        .attr("transform", "translate(" + vis_margin.left + "," + vis_margin.top + ")")

    vis_svg.call(vis_tip);

    d3.csv("static/data/features.csv", function (error, data) {
        if (error) throw error;
        var repoToCategory = {};
        d3.csv("static/data/repositories.csv", function (error, repos) {
            repos.forEach(function (d) {
                repoToCategory[d.url] = d.category;
            });
            var repoToValues = {};
            data.forEach(function (d) {
                if (!repoToValues[d.repository]) {
                    repoToValues[d.repository] = {};
                }
                repoToValues[d.repository][d.name] = +d.value;
                if (features.indexOf(d.name) == -1) {
                    features.push(d.name);
                }
            });
            data = [];
            for (var repo in repoToValues) {
                var r = repoToValues[repo];
                r.name = repo;
                r.category = repoToCategory[repo];
                if (r['Active time in days'] < 0) {
                    r['Active time in days'] = 0;
                }
                data.push(r);
            }
            vis_x.domain(d3.extent(data, function (d) {
                return d[X_FEATURE];
            })).nice();
            vis_y.domain(d3.extent(data, function (d) {
                return d[Y_FEATURE];
            })).nice();

            main_data = data;
            buildPlot();
            var x_max = d3.max(main_data, function (d) {
                return +d[X_FEATURE]
            });
            var y_max = d3.max(main_data, function (d) {
                return +d[Y_FEATURE]
            });
            d3.select('#x_max').property('value', x_max);
            d3.select('#y_max').property('value', y_max);
        });
    });
}
