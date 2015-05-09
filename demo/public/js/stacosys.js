// Copyright (c) 2015 Yannic ARNOUX

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
    alert('Woops, there was an error making the request.');
  };

  xhr.send();
}
