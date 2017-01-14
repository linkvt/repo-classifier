var matrices = d3.selectAll('.confusion-matrix');

matrices.each(function () {
    var matrix = d3.select(this);
    var data = JSON.parse(matrix.attr('data-matrix'));

    var categories = ['DEV', 'WEB', 'DATA', 'DOCS', 'EDU', 'HW', 'OTHER'];
    var color = d3.scale.category10();
    var colorScales = [];
    var gridSize = 40;
    var svg = matrix.append('g').attr('transform', 'translate(100, 40)');
    var tip = d3.tip().attr('class', 'd3-tip').html(function (d) {
        return d;
    });
    svg.call(tip);
    for (var i = 0; i < data.length; i++) {
        var max = d3.max(data[i]);
        colorScales.push(d3.scale.sqrt().domain([0, max]).range(['rgb(250, 250, 250)', color(i)]));
    }
    var text = svg.selectAll('text')
        .data(categories)
        .enter();

    text.append('text')
        .attr('y', function (d, i) {
            return i * gridSize + 40;
        })
        .attr('x', 0)
        .style('font-size', '11px')
        .text(function (d) {
            return d;
        })
        .style('font-weight', 'bold');
    text.append('text')
        .attr('x', function (d, i) {
            return i * gridSize + 53;
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
            return j * gridSize + 20;
        })
        .attr("height", 35)
        .attr("width", 35)
        .attr("fill", function (d, i, j) {
            return colorScales[j](d);
        })
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);
    gridElement.append("text")
        .attr("x", function (d, i) {
            return i * gridSize + 50 + (35 / 2);
        })
        .attr("y", function (d, i, j) {
            return j * gridSize + 25 + (35 / 2);
        })
        .text(function (d) {
            return d;
        })
        .style('fill', 'white')
        .style('text-anchor', 'middle');
    svg.append('text').attr('x', -100).attr('y', 170).text('True Label').style('fill', 'gray');
    svg.append('text').attr('x', 140).attr('y', -20).text('Predicted Label').style('fill', 'gray');
});
