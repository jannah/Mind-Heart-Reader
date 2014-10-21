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
    EXPERIMENT_INTRO: {filename: 'experiment_intro.html', target: '#experiment-content'},
    EXPERIMENT_UPLOAD: {filename: 'experiment_upload_data.html', target: '#experiment-content'}

};

var experiment, experiment_id, experiment_set, user_id;
var active_file_index = -1;
var TIME_INTERVAL = 15;
var IMAGE_LIMIT = 25;
var mindwave_file;
function initExperimentPage() {
    TEMPLATES = loadTemplates(TEMPLATES);
    experiment_id = $('#experiment-id').val();
    experiment = getExperiment(experiment_id);
    experiment_set = getExperimentSet(experiment_id);
    user_id = $('#user-id').val();
    console.log(experiment_set);
    console.log(experiment);
    if (experiment.completed)
        showUploadForm()
    else
        showIntro();
}
function showIntro()
{
    renderTemplate(TEMPLATES.EXPERIMENT_INTRO.target, TEMPLATES.EXPERIMENT_INTRO, null, true);
}
function hideIntro()
{
    $('#experiment-intro').hide();
//    startExperiment(experiment_id);
//    loadNextImage();
}
function hideUploadForm() {
    $('#experiment-upload').hide();
}
function uploadFile()
{
//    var f = $('#experiment-mindwave-file').files[0];
//    console.log(f);
    var formData = new FormData();
    console.log(mindwave_file);
//    formData.append('file', $('#experiment-mindwave-file').files[0])
    formData.append('mindwave_file', mindwave_file[0], mindwave_file[0].name);
    formData.append('experiment_id', experiment_id);
    var url = $('#mhreader-upload-mindwave-data-url').val();
    var resp = $.ajax({
        url: url, //Server script to process data
        type: 'POST',
        xhr: function() {  // Custom XMLHttpRequest
            var myXhr = $.ajaxSettings.xhr();
//            if (myXhr.upload) { // Check if upload property exists
//                myXhr.upload.addEventListener('progress', progressHandlingFunction, false); // For handling the progress of the upload
//            }
            return myXhr;
        },
        //Ajax events
        // Form data
        data: formData,
        //Options to tell jQuery not to process data or worry about content-type.
        cache: false,
        contentType: false,
        processData: false,
        async:false
    });
    console.log(resp);
    return false;
}
function startExperiment()
{
    hideIntro();
    active_file_index = -1;
    var url = $('#mhreader-start-experiment-url').val();
    var data = {experiment_id: experiment_id};
    var resp = getResponse(url, null, data, 'GET', false, false);
    loadNextImage();
}

function pauseExperiment()
{

}

function stopExperiment()
{
    var url = $('#mhreader-stop-experiment-url').val();
    var data = {experiment_id: experiment_id};
    return getResponse(url, null, data, 'GET', false, false);
}
function getExperiment()
{
    var url = $('#mhreader-get-experiment-url').val();
    var data = {experiment_id: experiment_id};
    return getResponse(url, null, data, 'GET', false, true);
}

function getExperimentSet()
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
        showUploadForm();

    }
}
function showUploadForm()
{

    renderTemplate(TEMPLATES.EXPERIMENT_UPLOAD.target, TEMPLATES.EXPERIMENT_UPLOAD, {experiment_id: experiment_id}, false, false);
    $('#experiment-mindwave-file').on('change', prepareMindaveUpload);
}
function prepareMindaveUpload(event)
{
    mindwave_file = event.target.files;
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