/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


$(document).on('ready', function() {

    initExperimentPage();
});

var TEMPLATES = {
    EXPERIMENT_FILE_VIEW: {filename: 'experiment_file_view.html', target: '#experiment-content'},
    EXPERIMENT_INTRO: {filename: 'experiment_intro.html', target: '#experiment-content'}

};

var experiment_id, experiment_set, user_id;
var active_file_index = -1;
var TIME_INTERVAL = 20;
var IMAGE_LIMIT = 20;
function initExperimentPage() {
    TEMPLATES = loadTemplates(TEMPLATES);
    experiment_id = $('#experiment-id').val();
    experiment_set = getExperimentSet(experiment_id);
    user_id = $('#user-id').val();
    console.log(experiment_set);
    showIntro();
}
function showIntro()
{
    renderTemplate(TEMPLATES.EXPERIMENT_INTRO.target, TEMPLATES.EXPERIMENT_INTRO, null, true);
}
function hideIntro()
{
    $('#experiment-intro').hide();
    startExperiment(experiment_id);
    loadNextImage();
}
function startExperiment(experiment_id)
{
    var url = $('#mhreader-start-experiment-url').val();
    var data = {experiment_id: experiment_id};
    return getResponse(url, null, data, 'GET', false, false);

}

function pauseExperiment(experiment_id)
{

}

function stopExperiment(experiment_id)
{
    var url = $('#mhreader-stop-experiment-url').val();
    var data = {experiment_id: experiment_id};
    return getResponse(url, null, data, 'GET', false, false);
}


function getExperimentSet(experiment_id)
{
    var url = $('#mhreader-get-experiment-sets-url').val();
    console.log(url);
    var data = {experiment_id: experiment_id};
    return getResponse(url, null, data, 'GET', false, true);
}

function getExperimentFiles(experiment_id)
{

}

function updateExperimentLog(experiment_id, time, action, target, result)
{

}

function submitUserResponse(resp, file_id)
{
    var url = $('#mhreader-add-user-response-url').val();
    var data = {user_id: user_id,
        experiment_id: experiment_id,
        experiment_file_id: file_id,
        action: resp,
        action_type: 'click'};

    var success_function = function(data) {
        console.log(data);
    };
    getResponse(url, null, data, 'POST', false, false, success_function);
    loadNextImage();
}

function loadNextImage()
{

    active_file_index++;
    if (active_file_index < experiment_set.set_files.length && active_file_index < IMAGE_LIMIT)
    {
        console.log(active_file_index);
        var expFile = experiment_set.set_files[active_file_index];
        console.log(expFile);
        var limit = (experiment_set.set_files.length < IMAGE_LIMIT) ? experiment_set.set_files.length : IMAGE_LIMIT;
        renderTemplate(TEMPLATES.EXPERIMENT_FILE_VIEW.target, TEMPLATES.EXPERIMENT_FILE_VIEW,
                {experiment_file: expFile.experiment_file, file_index: active_file_index, file_count: limit},
        true);
        startButtonTimer();
    }
    else
    {
        $('#experiment-media-view').hide();
        stopExperiment(experiment_id);

    }
}

function startButtonTimer()
{
    var counter = TIME_INTERVAL;
    disableButtons(counter);
    var mytimer = window.setInterval(function() {
        disableButtons(counter);
        if (counter === 0)
        {
            clearInterval(mytimer);
            enableButtons();
        }
        counter--;
    }, 1000);
}

function disableButtons(counter)
{
    var buttons = $('#experiment-responses input[type=button]');

    _.each(buttons, function(btn) {
        var value = $(btn).attr('data-value');
        $(btn).val(value + ' (' + counter + ')').prop("disabled", true);
    });
}
function enableButtons()
{
    var buttons = $('#experiment-responses input[type=button]');

    _.each(buttons, function(btn) {
        var value = $(btn).attr('data-value');
        $(btn).val(value).prop("disabled", false);
    });
}
//renderTemplate(target, template, args, replaceContent, replaceParent, id)
//getResponse(url, parameters, data, method, async, convert_to_json, success_function, error_function)