/*
 * This script aims to make the value of csrfmiddlewaretoken the same at the value of the csrftoken cookie.
 *
 * It saves the need to extract the token from a GET request before making each POST request.
 */


var cookieParamType = org.parosproxy.paros.network.HtmlParameter.Type.cookie;
var formParamType = org.parosproxy.paros.network.HtmlParameter.Type.form;
var urlParamType = org.parosproxy.paros.network.HtmlParameter.Type.url;


function sendingRequest(msg, initiator, helper) {
    var tokenValue = org.zaproxy.zap.extension.script.ScriptVars.getGlobalVar("csrf.cookie.value");
    if (tokenValue && initiator != "5"){
        var formParams = msg.getFormParams();
        var updatedFormParams = modifyParams(formParams, tokenValue);
        msg.setFormParams(updatedFormParams);
        var body = buildBody(updatedFormParams);
        msg.setRequestBody(body);
        msg.getRequestHeader().setContentLength(msg.getRequestBody().length());
    }
}


function responseReceived(msg, initiator, helper) {
    var cookieParams = msg.getCookieParams();
    var tokenValue = getTokenValue(cookieParams);
    org.zaproxy.zap.extension.script.ScriptVars.setGlobalVar("csrf.cookie.value", tokenValue);
}


function buildBody(params) {
    var newBody = "";
    var iterator = params.iterator();
    while(iterator.hasNext()) {
        var param = iterator.next();
        var pair = param.getName() + "=" + param.getValue() + "&";
        newBody += pair;
    }
    newBody = newBody.slice(0,-1)
    return newBody;
}


function getTokenValue(params) {
    var iterator = params.iterator();
    while(iterator.hasNext()) {
        var param = iterator.next();
        if (param.getName().equals("csrftoken")) {
            return param.getValue();
            break;
        }
    }
    return null;
}


function modifyParams(params, tokenValue) {
    var iterator = params.iterator();
    while(iterator.hasNext()) {
        var param = iterator.next();
        if (param.getName().equals("csrfmiddlewaretoken")) {
            param.setValue(tokenValue);
            break;
        }
    }
    return params;
}
