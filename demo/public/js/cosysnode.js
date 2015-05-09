// Released under Apache license
// Copyright (c) 2015 Yannic ARNOUX

// Create the XHR object.
function createCORSRequest(method, url) {
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

function cosysload() {
  var url = 'http://cosysnode.madyanne.fr:3000/comments';
  var xhr = createCORSRequest('GET', url);
  if (!xhr) {
    alert('CORS not supported');
    return;
  }

  // Response handlers.
  xhr.onload = function() {
    var jsonResponse = JSON.parse(xhr.responseText);
    var template = document.getElementById('template').innerHTML;
    var rendered = Mustache.render(template, jsonResponse);
    document.getElementById('cosys-comments').innerHTML = rendered;
  };

  xhr.onerror = function() {
    alert('Woops, there was an error making the request.');
  };

  xhr.send();
}
window.onload = cosysload;
