
/*var sampleChartData =[];
 [
 {
 className: 'now', // optional can be used for styling
 axes: [
 {axis: "0", value: 1},
 {axis: "1", value: 1},
 {axis: "2", value: 1},
 {axis: "3", value: 1},
 {axis: "4", value: 1},
 {axis: "5", value: 1},
 {axis: "6", value: 1},
 {axis: "7", value: 1}
 ]
 }];*/
var defaultDataMap;
var sampleData = [];
function initSampleData(dataMap, length)
{
    var entry = {className: 'now',
        axes: []};
    if (!dataMap && length)
    {
        dataMap = createDataMap(length);
    }
    _.each(dataMap, function(item)
    {
        entry.axes.push({axis: item.name, value: 1});
    });
    sampleData.push(entry);
}
function formatRadarChartData(data, dataMap)
{
    var chartData = [];
//    console.log(data);
    if (data.length > 0) {
//    data = (data && data.length>0)? data : sampleData;
        dataMap = (dataMap) ? dataMap : createDataMap(data[0]['values'].length);
        _.each(data, function(entry)
        {

            var t = entry['time'], values = entry['values'];
            var chartEntry = {className: t, axes: []};
            for (var i = 0, j = values.length; i < j; i++)
            {
                chartEntry.axes.push({axis: dataMap[i].name, value: values[i]});
            }
            chartData.push(chartEntry);
        });
//    console.log(chartData)
    }
    else
    {

        if (dataMap)
            initSampleData(dataMap)
        chartData = sampleData;
    }
//    console.log(chartData);
    return chartData;
}
function createDataMap(length)
{
    var dataMap = [];
    for (var i = 0; i < length; i++)
    {
        var entry = {'name': i + '', band: 'unkown', order: i};
        dataMap.push(entry);
    }
    return dataMap;
}
RadarChart = function() {
    var self = {};
    self.id = '';
    self.isDrawn = false;
    self.defaultConfig = {
        containerClass: 'radar-chart',
        w: 600,
        h: 600,
        id: '',
        factor: 0.95,
        factorLegend: 1,
        levels: 3,
        maxValue: 0,
        radians: 2 * Math.PI,
        color: d3.scale.category10(),
        axisLine: true,
        axisText: true,
        circles: true,
        circlesText: true,
        radius: 5,
        doFill: true,
        fadeLines: false,
        updateOnly: false,
        normalizeData: false,
        numberFormat : d3.format('d'),
        dataMap: null,
        axisJoin: function(d, i) {
            return d.className || i;
        },
        transitionDuration: 300
    };
    self.chart = function() {
        // default config
        var cfg = Object.create(self.defaultConfig);
        function radar(selection) {
            selection.each(function(data)
            {
                var container = d3.select(this);
                // allow simple notation
                if (cfg.normalizeData && data.length > 0)
                { 
                    if (!cfg.dataMap)
                    {
                        cfg.dataMap = createDataMap(data[0].axes.length);
                    }
                    cfg.numberFormat = d3.format('2.1%');
                    for (var i = 0, j = data[0].axes.length; i < j; i++)
                    {
                        var colData = $.map(data, function(entry,index){
                            return  data[index].axes[i].value;
                        });
                        var maxColValue = d3.max(colData);
                        _.each(data, function(d,index){
                            d.axes[i]['value'] /=maxColValue; 
                        });
                        
                        
                    }
                
                }
                data = data.map(function(datum) {
                    if (datum instanceof Array) {
                        datum = {axes: datum};
                    }
                    return datum;
                });
//                console.log(data);
                var maxValue = Math.max(cfg.maxValue, d3.max(data, function(d) {
                    return d3.max(d.axes, function(o) {
                        return o.value;
                    });
                }));
                var allAxis = data[0].axes.map(function(i, j) {

                    return i.axis;
                });
                var total = allAxis.length;
                var radius = cfg.factor * Math.min(cfg.w / 2, cfg.h / 2);
                container.classed(cfg.containerClass, 1);
                function getPosition(i, range, factor, func) {
                    factor = typeof factor !== 'undefined' ? factor : 1;
                    return range * (1 - factor * func(i * cfg.radians / total));
                }
                function getHorizontalPosition(i, range, factor) {
                    return getPosition(i, range, factor, Math.sin);
                }
                function getVerticalPosition(i, range, factor) {
                    return getPosition(i, range, factor, Math.cos);
                }
                if (!cfg.updateOnly)
                {
                    console.log('drawing first chart');
                    // levels && axises
                    var levelFactors = d3.range(0, cfg.levels).map(function(level) {
                        return radius * ((level + 1) / cfg.levels);
                    });
                    var levelGroups = container.selectAll('g.level-group').data(levelFactors);
                    levelGroups.enter().append('g');
                    levelGroups.exit().remove();
                    levelGroups.attr('class', function(d, i) {
                        return 'level-group level-group-' + i;
                    });
                    var levelLine = levelGroups.selectAll('.level').data(function(levelFactor) {
                        return d3.range(0, total).map(function() {
                            return levelFactor;
                        });
                    });
                    levelLine.enter().append('line');
                    levelLine.exit().remove();
                    levelLine
                            .attr('class', 'level')
                            .attr('x1', function(levelFactor, i) {
                                return getHorizontalPosition(i, levelFactor);
                            })
                            .attr('y1', function(levelFactor, i) {
                                return getVerticalPosition(i, levelFactor);
                            })
                            .attr('x2', function(levelFactor, i) {
                                return getHorizontalPosition(i + 1, levelFactor);
                            })
                            .attr('y2', function(levelFactor, i) {
                                return getVerticalPosition(i + 1, levelFactor);
                            })
                            .attr('transform', function(levelFactor) {
                                return 'translate(' + (cfg.w / 2 - levelFactor) + ', ' + (cfg.h / 2 - levelFactor) + ')';
                            });
                    if (cfg.axisLine || cfg.axisText) {
                        var axis = container.selectAll('.axis').data(allAxis);
                        var newAxis = axis.enter().append('g');
                        if (cfg.axisLine) {
                            newAxis.append('line');
                        }
                        if (cfg.axisText) {
                            newAxis.append('text');
                        }

                        axis.exit().remove();
                        axis.attr('class', 'axis');
                        if (cfg.axisLine) {
                            axis.select('line')
                                    .attr('x1', cfg.w / 2)
                                    .attr('y1', cfg.h / 2)
                                    .attr('x2', function(d, i) {
                                        return getHorizontalPosition(i, cfg.w / 2, cfg.factor);
                                    })
                                    .attr('y2', function(d, i) {
                                        return getVerticalPosition(i, cfg.h / 2, cfg.factor);
                                    });
                        }

                        if (cfg.axisText) {
                            axis.select('text')
                                    .attr('class', function(d, i) {
                                        var p = getHorizontalPosition(i, 0.5);
                                        return 'legend ' +
                                                ((p < 0.4) ? 'left' : ((p > 0.6) ? 'right' : 'middle'));
                                    })
                                    .attr('dy', function(d, i) {
                                        var p = getVerticalPosition(i, 0.5);
                                        return ((p < 0.1) ? '1em' : ((p > 0.9) ? '0' : '0.5em'));
                                    })
                                    .text(function(d) {
                                        console.log(d);
                                        return d;
                                    })
                                    .attr('x', function(d, i) {
                                        return getHorizontalPosition(i, cfg.w / 2, cfg.factorLegend);
                                    })
                                    .attr('y', function(d, i) {
                                        return getVerticalPosition(i, cfg.h / 2, cfg.factorLegend);
                                    });
                        }
                        if (cfg.circlesText)
                        {
                            var labelGroup = container.selectAll('.data-label')
                                    .data(data[data.length - 1].axes)
                                    .enter()
                                    .append('text')
                                    .classed('data-label', 1)
                                    .attr('dy', '1em');

                        }
                    }
                }
                // content
                data.forEach(function(d) {
                    d.axes.forEach(function(axis, i) {
                        axis.x = getHorizontalPosition(i, cfg.w / 2, (parseFloat(Math.max(axis.value, 0)) / maxValue) * cfg.factor);
                        axis.y = getVerticalPosition(i, cfg.h / 2, (parseFloat(Math.max(axis.value, 0)) / maxValue) * cfg.factor);
                    });
                });
                var polygons = container.selectAll(".area");
//                console.log(polygons[0].length);
                if (polygons[0].length > data.length + 1)
                {

                    for (var i = data.length; i < polygons[0].length; i++)
                    {
                        var poly = polygons[0][i];
                        console.log('removing poly ' + i);
                        poly.remove();
                    }
                }
                else if (polygons[0].length < data.length + 1)
                {
                    polygons.data(data).enter().append('polygon').classed('area', 1)
                }
                else
                {
                    container.select(".area").remove();
                    polygons.data(data).enter().append('polygon').classed('area', 1)
                }
                var polygon = container.selectAll(".area")
                        .data(data, cfg.axisJoin);
//                polygon.enter()
//                        .append('polygon');

                polygon.classed({area: 1, 'd3-enter': 1})
                        .on('mouseover', function(d) {
                            container.classed('focus', 1);
                            d3.select(this).classed('focused', 1);
                        })
                        .on('mouseout', function() {
                            container.classed('focus', 0);
                            d3.select(this).classed('focused', 0);
                        });
                /*
                 polygon.exit()
                 .classed('d3-exit', 1) // trigger css transition
                 .transition().duration(cfg.transitionDuration)
                 .remove();*/
                polygon
                        .each(function(d, i) {
                            var classed = {'d3-exit': 0}; // if exiting element is being reused
                            classed['radar-chart-serie' + i] = 1;
                            if (d.className) {
                                classed[d.className] = 1;
                            }
                            d3.select(this).classed(classed);
                        })

                        // styles should only be transitioned with css
                        .style('stroke', function(d, i) {
                            return cfg.color(i);
                        })
                        .style('fill', function(d, i) {
                            if (cfg.doFill)
                                return cfg.color(i);
                            else
                                return 'none';
                        })
                        .transition()
                        .duration(cfg.transitionDuration)
                        .ease('linear')
                        .style('stroke-opacity', function(d, i)
                        {

                            var smoothing = 1 - Math.pow((i / data.length), 1 / 4);
//                            console.log(i + '\t' + data.length + '\t' + smoothing);
                            if (cfg.fadeLines)
                                return smoothing;
                            else
                                return 1;
                        }).attr('points', function(d) {
                    return d.axes.map(function(p) {
//                                console.log([p.x, p.y].join(','));
                        return [p.x, p.y].join(',');
                    }).join(' ');
                })
                        .each('start', function() {
                            d3.select(this).classed('d3-enter', 0); // trigger css transition
                        })
                // svg attrs with js
                if (cfg.circlesText)
                {
                    var labelGroup = container.selectAll('.data-label')
                            .data(data[data.length - 1].axes)
                            .transition().duration(cfg.transitionDuration)
                            .attr({
                                x: function(d) {
                                    return d.x;
                                },
                                y: function(d) {
                                    return d.y;
                                },
                                'text-anchor': 'middle'})
                            .text(function(d) {
//                                console.log(d);
                                return cfg.numberFormat(d.value);
                            });
                }
                if (cfg.circles && cfg.radius) {
                    var tooltip = container.selectAll('.tooltip').data([1]);
                    tooltip.enter().append('text').attr('class', 'tooltip');
                    var circleGroups = container.selectAll('g.circle-group').data(data, cfg.axisJoin);
                    circleGroups.enter().append('g').classed({'circle-group': 1, 'd3-enter': 1});
                    circleGroups.exit()
                            .classed('d3-exit', 1) // trigger css transition
                            .transition().duration(cfg.transitionDuration).remove();
                    circleGroups
                            .each(function(d) {
                                var classed = {'d3-exit': 0}; // if exiting element is being reused
                                if (d.className) {
                                    classed[d.className] = 1;
                                }
                                d3.select(this).classed(classed);
                            })
                            .transition().duration(cfg.transitionDuration)
                            .each('start', function() {
                                d3.select(this).classed('d3-enter', 0); // trigger css transition
                            });
                    var circle = circleGroups.selectAll('.circle').data(function(datum, i) {
                        return datum.axes.map(function(d) {
                            return [d, i];
                        });
                    });
                    circle.enter().append('circle')
                            .classed({circle: 1, 'd3-enter': 1})
                            .on('mouseover', function(d) {
                                tooltip
                                        .attr('x', d[0].x - 10)
                                        .attr('y', d[0].y - 5)
                                        .text(d[0].value)
                                        .classed('visible', 1);
                                container.classed('focus', 1);
                                container.select('.area.radar-chart-serie' + d[1]).classed('focused', 1);
                            })
                            .on('mouseout', function(d) {
                                tooltip.classed('visible', 0);
                                container.classed('focus', 0);
                                container.select('.area.radar-chart-serie' + d[1]).classed('focused', 0);
                            });
                    circle.exit()
                            .classed('d3-exit', 1) // trigger css transition
                            .transition().duration(cfg.transitionDuration).remove();
                    circle
                            .each(function(d) {
                                var classed = {'d3-exit': 0}; // if exit element reused
                                classed['radar-chart-serie' + d[1]] = 1;
                                d3.select(this).classed(classed);
                            })
                            // styles should only be transitioned with css
                            .style('fill', function(d) {
                                return cfg.color(d[1]);
                            })
                            .transition().duration(cfg.transitionDuration)
                            // svg attrs with js
                            .attr('r', cfg.radius)
                            .attr('cx', function(d) {
                                return d[0].x;
                            })
                            .attr('cy', function(d) {
                                return d[0].y;
                            })
                            .each('start', function() {
                                d3.select(this).classed('d3-enter', 0); // trigger css transition
                            });
                    // ensure tooltip is upmost layer
                    var tooltipEl = tooltip.node();
                    tooltipEl.parentNode.appendChild(tooltipEl);
                }
            });
        }

        radar.config = function(value) {
            if (!arguments.length) {
                return cfg;
            }
            if (arguments.length > 1) {
                cfg[arguments[0]] = arguments[1];
            }
            else {
                d3.entries(value || {}).forEach(function(option) {
                    cfg[option.key] = option.value;
                });
            }
            return radar;
        };
        return radar;
    };
    self.draw = function(id, d, options) {
        if (!d || d.length === 0)
        {

            initSampleData(options.dataMap, 8);
            console.log('using default data');
            d = sampleData;
        }
        var chart = self.chart().config(options);
        var cfg = chart.config();
        self.id = id;
//        console.log(self.id);
        d3.select(id).select('svg').remove();
        d3.select(id)
                .append("svg")
                .attr("width", cfg.w)
                .attr("height", cfg.h)
                .datum(d)
                .call(chart);
        self.isDrawn = true;
    };
    self.update = function(d, options) {
//        if(!self.isDrawn) self.draw()
        if (!d || d.length === 0)
        {
            console.log('using default data');
            d = sampleData;
        }
        options['updateOnly'] = true;
        var chart = self.chart().config(options);
        var cfg = chart.config();
//        d3.select(self.id).select('svg').remove();
//        console.log(self.id);
        d3.select(self.id)
                .select('svg')
//                .append("svg")
//                .attr("width", cfg.w)
//                .attr("height", cfg.h)
                .datum(d)
                .call(chart);
    };
    return self;
};
