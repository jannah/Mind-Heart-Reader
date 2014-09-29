/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


$(document).on('ready', function() {
    initMhreader();
});
var TEMPLATES = {
    DATA_COUNTER: {filename: 'data_counter.html', target: '#data-counter'}
};
var mindwaveData = [];
var radarChart = RadarChart();

var INTERVAL = 1000;
var DATA_LIMIT = 30;
var options = {transitionDuration: INTERVAL, normalizeData: true, circles: false, doFill: false, fadeLines: true, dataMap: dataMap, color: function(i) {
        return '#9900aa';
    }};
function initMhreader()
{
    loadTemplates();
    initMindwaveChart();
//    loadDataCounter();
    //updateMindwaveStatus();


}

function loadTemplates()
{
    templates_url = $('#mhreader-templates-url').val();
    for (var template in TEMPLATES)
    {
        TEMPLATES[template]['url'] = templates_url + '/' + TEMPLATES[template].filename;
        TEMPLATES[template]['html'] = loadTemplate(TEMPLATES[template].url);
        TEMPLATES[template]['render'] = _.template(TEMPLATES[template]['html']);
    }
}


function loadTemplate(filename)
{
    var jqxhr = $.ajax({url: filename, async: false});
    return jqxhr.responseText;
}

/*
 * Render a specific HTML template
 * @param {string} target target HTML element ID to render the template under
 * @param {Object} template template  from TEMPLATES
 * @param {Object} args arguments to pass to the templates
 * @param {boolean} replace whether to replace the existing contents of the target
 * @param {string} id the id to give the rendered template
 * @returns {undefined}
 */
function renderTemplate(target, template, args, replaceContent, replaceParent, id)
{
    if (replaceContent)
    {
        $(target).empty().append(template.render(args));

    }
    else if (replaceParent)
    {
        console.log('replacing')
        if ($(target).length > 0)
        {
            $(target).replaceWith(template.render(args));
        }
        else
        {
            $(target).append(template.render(args));
        }
    }
    else
    {
        $(target).append(template.render(args));
    }
//    $(target).trigger(BODY_CHANGE_EVENT);
}


/*********************************
 *  Page Actions
 *****************************/


function startMindwave()
{
    $.ajax({
        url: $('#mhreader-start-mindwave-url').val(),
        success: function(data) {
            autoRefreshMindwaveData(INTERVAL);
//            updateMindwaveStatus();
        },
        fail: function(data) {
            console.log(data);
        }
    });
}

function stopMindwave()
{
    $.ajax({
        url: $('#mhreader-stop-mindwave-url').val(),
        success: function(data) {
            updateMindwaveStatus();
        },
        fail: function(data) {
            console.log(data);
        }
    });
}

function updateMindwaveStatus()
{
    $.ajax({
        url: $('#mhreader-get-mindwave-status-url').val(),
        success: function(data) {
            $('#mhreader-mindwave-status').text(data);
        },
        fail: function(data) {
            $('#mhreader-mindwave-status').text('Failed to retrieve status');
        }
    });
}


function initMindwaveChart()
{
//    $('#mindwave-chart-container').html('test')
    loadDataMap();
    radarChart.draw("#mindwave-chart-container", null, options);
    loadDataCounter();

}
function loadDataCounter()
{
    var url = $('#mhreader-get-mindwave-data-url').val();
    DATA_LIMIT = $('#text-data-limit').val();
//    console.log(url);
    var jqxhr = $.ajax(
            {
                url: url + '/' + DATA_LIMIT,
                async: false
            })
            .fail(function(data) {
                console.log('failed');
                $('#data-counter').html(data.responseText);
            })
            .success(function(data)
            {
//                console.log('success');
//                console.log(data);
                mindwaveData = JSON.parse(data);
//                console.log(mindwaveData);
                var chartData = formatRadarChartData(mindwaveData, dataMap);
                renderTemplate(TEMPLATES.DATA_COUNTER.target, TEMPLATES.DATA_COUNTER, {data: mindwaveData}, true);
//                if(chartData.length==0) chartData = sampleData;
                radarChart.update(chartData, options);
                if (!enableAutoRefresh)
                    autoRefreshMindwaveData(INTERVAL);
            });
    ;
//    data = jqxhr.responseText
}
var dataMap = []
function loadDataMap()
{

    var url = $('#mhreader-get-mindwave-data-map-url').val();
    console.log(url);
    var jqxhr = $.ajax({
        url: url,
        async: false
    });

    var data = jqxhr.responseText;
    dataMap = JSON.parse(data);
    console.log(dataMap);
    options.dataMap = dataMap;

}

var enableAutoRefresh = false;
function autoRefreshMindwaveData(interval)
{
    enableAutoRefresh = true;
    var refresh = function() {
//        console.log('refreshing');
        loadDataCounter();
        updateMindwaveStatus();
        setTimeout(refresh, interval);
    };

    refresh();
}