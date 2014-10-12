/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

$(document).on('ready', function() {
    initMindwaveClient();
})
var mindwaveData = [];
var radarChart = RadarChart();

var INTERVAL = 1000;
var DATA_LIMIT = 30;
var options = {transitionDuration: INTERVAL, normalizeData: true, circles: false, doFill: false, fadeLines: true, dataMap: dataMap, color: function(i) {
        return '#9900aa';
    }};
var TEMPLATES = {
    DATA_COUNTER: {filename: 'data_counter.html', target: '#data-counter'}
};

/*********************************
 *  Page Actions
 *****************************/
function initMindwaveClient()
{
    TEMPLATES = loadTemplates(TEMPLATES);
    initMindwaveChart();
}

function startMindwave(random)
{
    var url = (random) ?
            $('#mhreader-start-random-mindwave-url').val()
            : $('#mhreader-start-mindwave-url').val();
    console.log(url);
    $.ajax({
        url: url,
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

function dumpMindwaveData()
{
    var url = $('#mhreader-dump-mindwave-data-url').val(),
            filename = $('#dump-data-filename').val();
    $.ajax({
        url: url + '/' + filename,
        success: function(data) {
            console.log(data);
        }
    });
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