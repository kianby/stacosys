// Released under Apache license
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

function stacosys_count() {
  var url = STACOSYS_URL + '/comments/count?token=' + STACOSYS_TOKEN + '&url=' + STACOSYS_PAGE;
  var xhr = stacosys_get_cors_request('GET', url);
  if (!xhr) {
    console.log('CORS not supported');
    return 0;
  }

  // Response handlers.
  xhr.onload = function() {
    var jsonResponse = JSON.parse(xhr.responseText);
    var count = jsonResponse.count;
    if (count > 0) {
      if (count > 1) { 
        document.getElementById('show-comment-label').innerHTML = 'Voir les ' + count + ' commentaires';
      }
      document.getElementById('show-comments-button').style.display = '';
    }
    return jsonResponse.count;
  };

  xhr.onerror = function() {
    console.log('Woops, there was an error making the request.');
    return 0;
  };

  xhr.send();
}

function stacosys_load() {
  var url = STACOSYS_URL + '/comments?token=' + STACOSYS_TOKEN + '&url=' + STACOSYS_PAGE;

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
