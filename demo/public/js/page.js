// --------------------------------------------------------------------------
//  Common functions
// --------------------------------------------------------------------------

function show_hide(panel_id, button_id){
    if (document.getElementById(panel_id).style.display == 'none'){
        document.getElementById(panel_id).style.display = '';
        document.getElementById(button_id).style.display = 'none';
    } else {
        document.getElementById(panel_id).style.display = 'none';
    }
}

// --------------------------------------------------------------------------
//  Load and display page comments
// --------------------------------------------------------------------------

function initialize_comments() { 
  stacosys_get_count(init_success, init_failure);
}

function init_success(data) {
  var response = JSON.parse(data);
  var count = response.count;
  if (count > 0) {
    if (count > 1) { 
      document.getElementById('show-comment-label').innerHTML = 'Voir les ' + count + ' commentaires';
    }
    document.getElementById('show-comments-button').style.display = '';
  }
  console.log('initialization success');
}

function init_failure(error) { 
  // NOP
  console.log('initialization failure');
}

function show_comments() {
  stacosys_load_comments(loading_success, loading_failure);
}

function loading_success(data) { 
  var response = JSON.parse(data);
  for (var i = 0, numTokens = response.data.length; i < numTokens; ++i) {
    response.data[i].mdcontent = markdown.toHTML(response.data[i].content);
  }
  show_hide('stacosys-comments', 'show-comments-button');
  var template = document.getElementById('stacosys-template').innerHTML;
  var rendered = Mustache.render(template, response);
  document.getElementById('stacosys-comments').innerHTML = rendered;
}

function loading_failure(error) {
  // NOP
  console.log('loading failure');
}

// --------------------------------------------------------------------------
//  Submit a new comment
// --------------------------------------------------------------------------

function new_comment() {
  var author = document.getElementById('author').value;
  var email = document.getElementById('email').value;
  var site = document.getElementById('site').value;
  var captcha = document.getElementById('captcha').value;
  var subscribe = document.getElementById('subscribe').value;
  var message = document.getElementById('message').value;
  
  stacosys_new_comment(author, email, site, captcha, subscribe, message, submit_success, submit_failure);
}

function submit_success(data) { 
  console.log('submit ' + data);
  window.location="redirect.html?p=" + STACOSYS_PAGE;
}

function submit_failure(error) {
  console.log('submit failure');
  // TODO redirect to error page
}

// --------------------------------------------------------------------------
//  Markdown preview
// --------------------------------------------------------------------------

function preview_markdown() {
    if (document.getElementById('preview-container').style.display == 'none'){
        document.getElementById('preview-container').style.display = '';
    }
    var $ = function (id) { return document.getElementById(id); };
    new Editor($("message"), $("preview"));
}

function Editor(input, preview) {
    this.update = function () {
        preview.innerHTML = markdown.toHTML(input.value);
    };
    input.editor = this;
    this.update();
}


