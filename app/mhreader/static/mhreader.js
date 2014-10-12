/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


$(document).on('ready', function() {
    initMhreader();
});

function initMhreader()
{
    //loadTemplates();
}

function loadTemplates(templates, templatesURL)
{
    console.log('loading templates ' + templates.length)
    templatesURL = (templatesURL) ? templatesURL : $('#mhreader-templates-url').val();
    for (var template in templates)
    {
        templates[template]['url'] = templatesURL + '/' + templates[template].filename;
        templates[template]['html'] = loadTemplate(templates[template].url);
        templates[template]['render'] = _.template(templates[template]['html']);
    }
    return templates;
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

function showErrorPanel(errorHTML)
{
    $('.error-form-body').html(errorHTML.responseText);
    $('.error-form').show()

}

function hideErrorPanel()
{
    $('.error-form').hide();

}
/**
 * 
 * @param {type} url
 * @param {type} parameters
 * @param {type} data
 * @param {type} method
 * @param {type} async
 * @param {type} convert_to_json
 * @param {type} success_function
 * @param {type} error_function
 * @returns {$@call;ajax.responseText|Array|Object}
 */
function getResponse(url, parameters, data, method, async, convert_to_json, success_function, error_function)
{
    console.log('getting '+ url);
    async = (async) ? async : false;
    if (parameters)
    {
        var param_str = '';
        _.each(parameters, function(key, value)
        {
            param_str += key + '=' + value;
        });
        if (param_str.length > 0)
            url += '?' + param_str;
    }
    method = (method) ? method : 'GET';
    var jqxhr = $.ajax({
        url: url,
        data: data,
        method: method,
        async: async,
        success: function(data) {
            if (success_function)
                success_function(data);
        },
        error: function(data) {
            showErrorPanel(data);
            if (error_function)
                error_function(data);
        }
    });
    var result;
    var text = jqxhr.responseText;
    /*console.log(text);
    if(!text)
    {
        console.log(jqxhr);
    }*/
    try {

        
        
        result = (convert_to_json) ? JSON.parse(text) : text;
    }
    catch (e)
    {
        console.log(e);
        if (e.message === 'Unexpected token u')
        {
            text = text.replace("u'", "'");
            console.log(text);
            result = JSON.parse(text);
        }
    }
//    console.log(result);
    return result;
}