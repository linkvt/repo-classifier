var reports = d3.selectAll('.report');

reports.each(function () {
    var report = d3.select(this);
    var data = JSON.parse(report.attr('data-matrix'));
    var svg = report.append('g').attr('transform', 'translate(20, 20)');

    var categories = ['DEV', 'WEB', 'DATA', 'DOCS', 'EDU', 'HW', 'OTHER', 'Average'];
    var columns = ['Precision', 'Recall', 'F1', 'Support'];
    var percentage = d3.format('.0%')
    var color = d3.scale.linear()
        .domain([0, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
        .range(['#f96a6c', '#fa8571', '#fb9f76', '#fdbc7b', '#fdc47d', '#fdea83', '#9cce7e', '#67bf7b']);

    var gridSize = 60;
    var gridSizeY = 35;
    var tip = d3.tip().attr('class', 'd3-tip').html(function (d) {
        return d;
    });
    svg.call(tip);
    var text = svg.selectAll('text')
        .data(categories)
        .enter();
    var column_text = svg.selectAll('.column')
        .data(columns)
        .enter();

    text.append('text')
        .attr('y', function (d, i) {
            return i * gridSizeY + 40;
        })
        .attr('x', 10)
        .style('font-size', function (d, i) {
            if (i < 7) {
                return '11px';
            } else {
                return '14px';
            }
        })
        .text(function (d) {
            return d;
        })
        .style('font-weight', 'bold');
    column_text.append('text')
        .attr('x', function (d, i) {
            return i * gridSize + 67;
        })
        .attr('y', 10)
        .style('font-size', '11px')
        .text(function (d) {
            return d;
        })
        .style('font-weight', 'bold');
    ;

    var gridElement = svg.selectAll("rect")
        .data(data)
        .enter()
        .append("g")
        .selectAll("rect")
        .data(function (d) {
            return d;
        })
        .enter();
    gridElement.append("rect")
        .attr("x", function (d, i) {
            return i * gridSize + 50;
        })
        .attr("y", function (d, i, j) {
            return j * gridSizeY + 20;
        })
        .attr("height", 30)
        .attr("width", 35)
        .attr("fill", function (d, i, j) {
            if (i !== 3) {
                return color(d);
            } else {
                return 'lightgray';
            }
        })
        .classed('average-rect', function (d, i, j) {
            return j == 7;
        })
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);
    gridElement.append("text")
        .attr("x", function (d, i) {
            return i * gridSize + 50 + (35 / 2);
        })
        .attr("y", function (d, i, j) {
            return j * gridSizeY + 25 + (35 / 2);
        })
        .text(function (d, i) {
            if (i !== 3) {
                return percentage(d);
            } else {
                return d;
            }
        })
        .classed('average-text', function (d, i, j) {
            return j == 7;
        })
        .style('text-anchor', 'middle');
});

