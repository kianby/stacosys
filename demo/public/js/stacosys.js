// Released under Apache license
// Copyright (c) 2015 Yannic ARNOUX

STACOSYS_URL = 'http://127.0.0.1:8000';
STACOSYS_TOKEN = '9fb3fc042c572cb831005fd16186126765140fa2bd9bb2d4a28e47a9457dc26c';
//STACOSYS_PAGE = 'blogduyax.madyanne.fr/mes-applications-pour-blackberry.html'
STACOSYS_PAGE = 'blogduyax.madyanne.fr/migration-du-blog-sous-pelican.html'

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

function stacosys_get_url() {
  return STACOSYS_URL + '/comments?token=' + STACOSYS_TOKEN + '&url=' + STACOSYS_PAGE;
}

function stacosys_load() {
  var url = stacosys_get_url();
  var xhr = stacosys_get_cors_request('GET', url);
  if (!xhr) {
    alert('CORS not supported');
    return;
  }

  // Response handlers.
  xhr.onload = function() {
    var jsonResponse = JSON.parse(xhr.responseText);
    for (var i = 0, numTokens = jsonResponse.data.length; i < numTokens; ++i) {
      jsonResponse.data[i].mdcontent = markdown.toHTML(jsonResponse.data[i].content);
    }
    var template = document.getElementById('stacosys-template').innerHTML;
    var rendered = Mustache.render(template, jsonResponse);
    document.getElementById('stacosys-comments').innerHTML = rendered;
  };

  xhr.onerror = function() {
    alert('Woops, there was an error making the request.');
  };

  xhr.send();
}
window.onload = stacosys_load;
