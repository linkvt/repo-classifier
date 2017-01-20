if (!d3.select('#histogram').empty()) {
    var load = function (feature, x_max, n) {

        d3.select('#histogram').selectAll('rect').remove();
        d3.csv("static/data/features.csv", function (error, data) {
            if (error) throw error;
            var features = [];
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
                ;
                var feature_values = {};
                for (var i = 0; i < data.length; i++) {
                    if (!(data[i].category in feature_values)) {
                        feature_values[data[i].category] = [];
                    }
                    feature_values[data[i].category].push(data[i][feature]);
                }
                build(feature_values, x_max, n);
                buildSelect(features);
            });
        });
    }
    var buildSelect = function (features) {
        var select = d3.select('#features');

        select.selectAll('option')
            .data(features)
            .enter()
            .append('option')
            .attr('value', function (d) {
                return d;
            })
            .text(function (d) {
                return d;
            });
        select.on('change', function () {
            var feature = d3.selectAll('option')
                .filter(function (d, i) {
                    return this.selected;
                }).text();
            load(feature, null, +d3.select('#n').property('value'));
        });
    };
    var getSelectedFeature = function () {
        return d3.selectAll('option')
            .filter(function (d, i) {
                return this.selected;
            }).text();
    }
    var build = function (feature_values, x_max, n) {
        var MAX = x_max ? x_max : d3.max(d3.values(feature_values), function (d) {
                return d3.max(d);
            });
        d3.select('#max').property('value', MAX);
        var MIN = d3.min(d3.values(feature_values), function (d) {
            return d3.min(d);
        });
        var bin_index = function (x) {
            return Math.floor((n - 1) * (x - MIN) / (MAX - MIN));
        };
        var bins = {};
        for (category in feature_values) {
            var bin = [];
            for (var i = 0; i < n; i++) {
                bin.push(0);
            }
            bins[category] = bin;
        }
        for (var category in feature_values) {
            feature_values[category].forEach(function (d) {
                var i = bin_index(d);
                bins[category][i] += 1;
            });
            var bin_sum = d3.max(bins[category]);
            for (var i = 0; i < bins[category].length; i++) {
                bins[category][i] = bins[category][i] / bin_sum;
            }
            console.log(bins[category]);
        }
        var bin_max = d3.max(d3.values(bins), function (d) {
            return d3.max(d);
        });
        var height = 50;
        var width = 300;
        var bin_width = width / n;
        var y_scale = d3.scale.linear().domain([1, 0]).range([1, height]);
        var svg = d3.select('#histogram');
        var color = d3.scale.category10();
        var categories = d3.keys(feature_values);

        var i_c = 0;
        var display_categories = ['DEV', 'WEB', 'DATA', 'DOCS', 'EDU', 'HW', 'OTHER'];
        for (var i = 0; i < display_categories.length; i++) {
            var category = display_categories[i];
            svg.selectAll('.' + category)
                .data(bins[category])
                .enter()
                .append('rect')
                .attr('x', function (d, i) {
                    return i * bin_width;
                })
                .attr('y', function (d, i) {
                    return y_scale(d) + i_c * (height + 5) + 5;
                })
                .attr('height', function (d, i) {
                    return height - y_scale(d);
                })
                .attr('width', bin_width - 2)
                .style('fill', color(category))
                .style('opacity', 0.8);
            svg.append('rect')
                .attr('width', width)
                .attr('height', height)
                .attr('x', 0)
                .attr('y', i_c * (height + 5) + 5)
                .style('fill', 'none')
                .style('stroke', 'lightgray');

            i_c++;
        }
        var legend = svg.selectAll('.legend')
            .data(display_categories)
            .enter();
        legend.append('rect')
            .attr('width', 30)
            .attr('height', 20)
            .attr('x', function (d, i) {
                return 310;
            })
            .attr('y', function (d, i) {
                return 30 + i * 55 + 5;
            })
            .style('fill', color);
        legend.append('text')
            .attr('x', function (d, i) {
                return 310 + 15;
            })
            .attr('y', function (d, i) {
                return 40 + i * 55 + 6;
            })
            .style('font-size', '8px')
            .style('fill', 'white')
            .style('text-anchor', 'middle')
            .text(function (d) {
                return d;
            });
    };
    d3.select('#max').on('change', function () {
        load(getSelectedFeature(), +d3.select(this).property('value'), +d3.select('#n').property('value'));
    });
    d3.select('#n').on('change', function () {
        load(getSelectedFeature(), +d3.select('#max').property('value'), +d3.select(this).property('value'));
    });
    load('Share of Images-extensions by size', null, 15);
}
