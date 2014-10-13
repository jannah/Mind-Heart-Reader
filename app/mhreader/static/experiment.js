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

var experiment_id, experiment_files = []
function initExperimentPage() {
    TEMPLATES = loadTemplates(TEMPLATES);
    experiment_id = $('#experiment-id').val();
    experiment_files =  getExperimentSet(experiment_id);
    console.log(experiment_files);
}

function startExperiment(experiment_id)
{

}

function pauseExperiment(experiment_id)
{

}

function finishExperiment(experiment_id)
{

}


function getExperimentSet(experiment_id)
{
    var url = $('#mhreader-get-experiment-sets-url').val();
    console.log(url);
    var data = {experiment_id: experiment_id};
    return getResponse(url, null, data, 'GET', true, true);
}

function getExperimentFiles(experiment_id)
{

}

function updateExperimentLog(experiment_id, time, action, target, result)
{

}