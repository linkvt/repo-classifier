var roc_curves = d3.selectAll('.roc-curve');

roc_curves.each(function () {
    var roc_curve = d3.select(this);
    var fpr = JSON.parse(roc_curve.attr('data-fpr'));
    var tpr = JSON.parse(roc_curve.attr('data-tpr'));

    var margins = {
        top: 20,
        right: 10,
        bottom: 50,
        left: 30
    };
    var width = 330 - margins.left - margins.right;
    var height = 330 - margins.top - margins.bottom;
    roc_curve.attr('width', 300).attr('height', 330);
    var x_scale = d3.scale.linear().domain([0, 1]).range([0, width]);
    var y_scale = d3.scale.linear().domain([0, 1]).range([height, 0]);

    var svg = roc_curve.append('g')
        .attr("transform", "translate(" + margins.left + "," + margins.top + ")");

    var x_axis = d3.svg.axis()
        .scale(x_scale)
        .orient("bottom");
    var y_axis = d3.svg.axis()
        .scale(y_scale)
        .orient("left");
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(x_axis)
        .append("text")
        .attr("class", "label")
        .attr("x", width - 20)
        .attr("y", -6)
        .style("text-anchor", "end")
        .text("FPR");
    svg.append("g")
        .attr("class", "y axis")
        .call(y_axis)
        .append("text")
        .attr("class", "label")
        .attr("transform", "translate(20, -5)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("TPR");

    var random_points = [{x: 0, y: 0}, {x: 1, y: 1}];

    var to_coords = function (f, t) {
        var points = [];
        for (var i = 0; i < f.length; i++) {
            points.push({x: f[i], y: t[i]});
        }
        return points;
    };

    var points = [];
    for (var i = 0; i < tpr.length; i++) {
        points.push(to_coords(fpr[i], tpr[i]))
    }

    var roc_line = d3.svg.line()
        .x(function (d) {
            return x_scale(d.x);
        })
        .y(function (d) {
            return y_scale(d.y);
        });

    svg.append("path")
        .attr("d", roc_line(random_points))
        .classed("random-line", true);

    var color = d3.scale.category10();
    var color_order = [2, 0, 3, 4, 5, 6, 1];
    points.forEach(function (p, i) {
        svg.append("path")
            .attr("d", roc_line(p))
            .classed("roc-line", true)
            .style("stroke", color(color_order[i]));
    })

});
