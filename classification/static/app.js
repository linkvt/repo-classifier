var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 300 - margin.left - margin.right,
    height = 150 - margin.top - margin.bottom;


var test = d3.selectAll('.validation-svg');

test.each(function (ob) {
    svg = d3.select(this);

    var tip = d3.tip().attr('class', 'd3-tip').html(function (d) {
        return 'Value: ' + d.value;
    });
    svg.call(tip);

    var x = d3.scale.ordinal().rangeRoundBands([0, width], .4);

    var y = d3.scale.linear().range([height, 1]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .ticks(10);

    data = [
        {category: 'DATA', value: svg.attr('data-prob-data')},
        {category: 'DEV', value: svg.attr('data-prob-dev')},
        {category: 'DOCS', value: svg.attr('data-prob-docs')},
        {category: 'EDU', value: svg.attr('data-prob-edu')},
        {category: 'HW', value: svg.attr('data-prob-hw')},
        {category: 'OTHER', value: svg.attr('data-prob-other')},
        {category: 'WEB', value: svg.attr('data-prob-web')}
    ];

    x.domain(data.map(function (d) {
        return d.category;
    }));

    y.domain([0, 1]);

    svg.attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
        .selectAll("text")
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", "-.55em")
        .attr("transform", "rotate(-90)");

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Probability");

    var groups = svg.selectAll("bar")
        .data(data)
        .enter().append('g');

    groups.append("rect")
        .style("fill", "steelblue")
        .attr("x", function (d) {
            return x(d.category);
        })
        .attr("width", x.rangeBand())
        .attr("y", function (d) {
            return y(d.value);
        })
        .attr("height", function (d) {
            return height - y(d.value);
        })
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);

    groups.append("text")
        .attr("x", function (d) {
            return -70;
        })
        .attr("y", function (d) {
            return x(d.category) + 15;
        })
        .attr("transform", "rotate(-90)")
        .style("text-anchor", "end")
        .text(function (d) {
            return d.value;
        });
});

