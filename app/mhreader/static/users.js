/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

//renderTemplate(target, template, args, replaceContent, replaceParent, id)
$(document).on('ready', function() {

    initUserPage();
});
var TEMPLATES = {
    ADD_USER: {filename: 'add_user_form.html', target: '.popup-form-content'},
    SHOW_USERS: {filename: 'show_user_list.html', target: '#user-list'},
    CREATE_USER_EXPERIMENT: {filename: 'create_user_experiment.html', target: '.popup-form-content'}
};
var users = [];
function initUserPage()
{

    TEMPLATES = loadTemplates(TEMPLATES);
    loadUserList();

}
function loadUserList()
{
    var users = getUsers();
    var experiments = getUserExperiments();

    console.log(users);
    console.log(experiments);
    renderTemplate(TEMPLATES.SHOW_USERS.target, TEMPLATES.SHOW_USERS, {users: users, experiments: experiments}, true, false);
}
function showAddNewUserForm()
{

    renderTemplate(TEMPLATES.ADD_USER.target, TEMPLATES.ADD_USER, null, true, false);
    $(TEMPLATES.ADD_USER.target).parent().show();
    $('#add-user-form').unbind('submit').on('submit', function() {
        addNewUser();
        return false;
    });


}
function addNewUser()
{
    var url = $('#mhreader-add-new-user-url').val();
    var data = {
        name: $('#new-user-name').val(),
        age: $('#new-user-age').val(),
        gender: $('.new-user-gender-option:checked').val(),
        description: $('#new-user-description').val()
    };
    success_function = function() {
        loadUserList()
    }
    var response = getResponse(url, null, data, 'POST', false, true, success_function);
    hideAddNewUserForm();
    return false;

}
function hideAddNewUserForm()
{
    $(TEMPLATES.ADD_USER.target).parent().hide();
}

function getUsers()
{
    var url = $('#mhreader-get-users-url').val();
    var response = getResponse(url, null, null, 'GET', false, true);
    return response;

}


function deleteUser(userId)
{
    var url = $('#mhreader-delete-user-url').val();

    var success_function = function(data) {
        alert(data + '');
        loadUserList();
    };
    var response = getResponse(url, null, {id: userId}, false, false, success_function);
    return false;
}

function getExperimentSets()
{
    var url = $('#mhreader-get-experiment-sets-url').val();
    var response = getResponse(url, null, null, 'GET', false, true);
    return response;
}
function showCreateUserExperimentForm(userId)
{
    var exp_sets = getExperimentSets();
    console.log(exp_sets);
    renderTemplate(TEMPLATES.CREATE_USER_EXPERIMENT.target, TEMPLATES.CREATE_USER_EXPERIMENT, {experiment_sets: exp_sets}, true, false);
    $(TEMPLATES.CREATE_USER_EXPERIMENT.target).parent().show();
    $('#create-user-experiment-form').unbind('submit').on('submit', function() {
        console.log('creating user experiment');
        createUserExperiment(userId);
        return false;
    });

    return false;
}
function hideCreateUserExperimentForm()
{
    $(TEMPLATES.CREATE_USER_EXPERIMENT.target).parent().hide();


}
function createUserExperiment(userId)
{
    console.log('starting new experiment');
    var url = $('#mhreader-create-expriment-url').val();
    var data = {
        title: $('#experiment-title').val(),
        user_id: userId,
        experiment_set_id: $('.experiment-set-option:checked').val(),
        remarks: $('#experiment-remarks').val()
    };
    success_function = function(data) {
        console.log(data);
        loadUserList();
    };

    var response = getResponse(url, null, data, 'POST', false, false, success_function);
    hideCreateUserExperimentForm();
    return false;
}


function getUserExperiments()
{
    var url = $('#mhreader-get-user-expriments-url').val();
    
    var response = getResponse(url, null, null, 'GET', false, true);
//    var resp = JSON.parse(response);
//    console.log(resp);
    return response;
}

function loadUserExperimentPage(experiment_id)
{
    var url = $('#mhreader-load-user-expriment-page-url').val();
    url+='?experiment_id='+experiment_id;
    window.location.replace(url);
}
                            