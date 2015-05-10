// Copyright (c) 2015 Yannic ARNOUX

/**
 * Make a X-Domain request to url and callback.
 *
 * @param url {String}
 * @param method {String} HTTP verb ('GET', 'POST', 'DELETE', etc.)
 * @param data {String} request body
 * @param callback {Function} to callback on completion
 * @param errback {Function} to callback on error
 */
function xdr(url, method, data, callback, errback) {
    var req;
    
    if(XMLHttpRequest) {
        req = new XMLHttpRequest();
 
        if('withCredentials' in req) {
            req.open(method, url, true);
            req.onerror = errback;
            req.onreadystatechange = function() {
                if (req.readyState === 4) {
                    if (req.status >= 200 && req.status < 400) {
                        callback(req.responseText);
                    } else {
                        errback(new Error('Response returned with non-OK status'));
                    }
                }
            };
            req.send(data);
        }
    } else if(XDomainRequest) {
        req = new XDomainRequest();
        req.open(method, url);
        req.onerror = errback;
        req.onload = function() {
            callback(req.responseText);
        };
        req.send(data);
    } else {
        errback(new Error('CORS not supported'));
    }
}


// Create the XHR object.
function stacosys_get_cors_request(method, url) {
  var xhr = new XMLHttpRequest();
  if ("withCredentials" in xhr) {
    // XHR for Chrome/Firefox/Opera/Safari.
    xhr.open(method, url, true);
  } else if (typeof XDomainRequest != "undefined") {
    // XDomainRequest for IE.
    xhr = new XDomainRequest();
    xhr.open(method, url);
  } else {
    // CORS not supported.
    xhr = null;
  }
  return xhr;
}

function stacosys_count(callback) {

  var url = STACOSYS_URL + '/comments/count?token=' + STACOSYS_TOKEN + '&url=' + STACOSYS_PAGE;
  var xhr = stacosys_get_cors_request('GET', url);
  if (!xhr) {
    console.log('CORS not supported');
    callback(0);
    return;
  }

  // Response handlers.
  xhr.onload = function() {
    var jsonResponse = JSON.parse(xhr.responseText);
    var count = jsonResponse.count;
    callback(count);
  };

  xhr.onerror = function() {
    console.log('Woops, there was an error making the request.');
    callback(0);
  };

  xhr.send();
}

function stacosys_load(callback) {

  var url = STACOSYS_URL + '/comments?token=' + STACOSYS_TOKEN + '&url=' + STACOSYS_PAGE;
  var xhr = stacosys_get_cors_request('GET', url);
  if (!xhr) {
    console.log('CORS not supported');
    return;
  }

  // Response handlers.
  xhr.onload = function() {
    var jsonResponse = JSON.parse(xhr.responseText);
    callback(jsonResponse);
  };

  xhr.onerror = function() {
    console.log('Woops, there was an error making the request.');
  };

  xhr.send();
}

function stacosys_new(author, email, site, captcha, callback) {

  var url = STACOSYS_URL + '/comments?token=' + STACOSYS_TOKEN 
              + '&url=' + STACOSYS_PAGE + '&author=' + author 
              + '&email=' + email + '&site=' + site 
              + '&captcha=' + captcha;
  var xhr = stacosys_get_cors_request('POST', url);
  if (!xhr) {
    console.log('CORS not supported');
    callback(false);
    return;
  }

  // Response handlers.
  xhr.onload = function() {
    var jsonResponse = JSON.parse(xhr.responseText);
    callback(jsonResponse);
  };

  xhr.onerror = function() {
    console.log('Woops, there was an error making the request.');
    callback(false);
  };

  xhr.send();
}
