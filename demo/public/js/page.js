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
  stacosys_count(comments_initialized);
}

function comments_initialized(count) { 
  if (count > 0) {
    if (count > 1) { 
      document.getElementById('show-comment-label').innerHTML = 'Voir les ' + count + ' commentaires';
    }
    document.getElementById('show-comments-button').style.display = '';
  }
}

function show_comments() {
  stacosys_load(comments_loaded);
}

function comments_loaded(response) { 
  for (var i = 0, numTokens = response.data.length; i < numTokens; ++i) {
    response.data[i].mdcontent = markdown.toHTML(response.data[i].content);
  }
  show_hide('stacosys-comments', 'show-comments-button');
  var template = document.getElementById('stacosys-template').innerHTML;
  var rendered = Mustache.render(template, response);
  document.getElementById('stacosys-comments').innerHTML = rendered;
}

// --------------------------------------------------------------------------
//  Submit a new comment
// --------------------------------------------------------------------------

function new_comment() {
  var author = document.getElementById('author').value;
  var email = document.getElementById('email').value;
  var site = document.getElementById('site').value;
  var captcha = document.getElementById('captcha').value;
  //var subscribe = document.getElementById('subscribe').value;
  
  stacosys_new(author, email, site, captcha, comment_submitted);
}

function comment_submitted(success) { 
  console.log('SUBMITTED : ' + success);
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


