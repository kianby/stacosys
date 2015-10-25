## Stacosys

Stacosys (aka STAtic blog COmment SYStem) is a fork of [Pecosys](http://github.com/kianby/pecosys) trying to fix Pecosys design drawbacks and to provide an alternative to hosting services like Disqus. Stacosys protects your readers's privacy.

Stacosys works with any static blog or even a simple HTML page. It  privilegiates e-mails to communicate with the blog administrator. It doesn't sound *hype* but I'm an old-school guy ;-) E-mail is reliable and an
universal way to discuss. You can answer from any device using an e-mail client or a Webmail.

###  Features overview

Stacosys main feature is comment management.

Here is the workflow:

-    Readers submit comments via a comment form embedded in blog pages
-    Blog administrator receives an email notification from Stacosys when a
     comment is submitted
-    Blog administrator can approve or drop the comment by replying to e-mail
-    Stacosys stores approved comment in its database.
     
Moreover Stacosys has an additional feature: readers can subscribe to further
comments for a post if they have provided an email.

Stacosys is localized (english and french).

### Technically speaking, how does it work?

Stacosys can be hosted on the same server or on a different server than the blog. Stacosys offers a REST API to retrieve and post comments. Static blog is HTML-based and a piece of JavaScript code  interacts with Stacosys using [CORS](http://enable-cors.org) requests. Each blog has a unique ID. Thus Stacosys can serve multiple blogs. Each page has a unique id and a simple request allows to retrieve comments for a given page. Similarly a POST request allows to send a comment from reader browser to Stacosy server. The comment post is relayed to the administrator by e-mail. for this purpose a dedicated email is assigned to Stacosys to communicate with blog administrator and blog subscribers.

### FAQ

*So the blog needs a server-side language?*
- It depends on your hosting configuration. Stacosys can run on a different host than the blog and it can serve several blogs. You have to change JS code embedded in blog pages to point the right Stacosys API URL.

*How do you block spammers?*
- That's a huge topic. Current comment form is basic: no captcha support but a honey
  pot. Nothing prevents from improving the template with JavaScript libs to do more
  complex things.

*Which database is used?*
- Thanks to Peewee ORM a wide range of databases is supported. I personnaly uses SQLite.

*Which technologies are used?*

-    [Python](https://www.python.org)
-    [Flask](http://flask.pocoo.org)
-    [Peewee ORM](http://docs.peewee-orm.com)
-    [Markdown](http://daringfireball.net/projects/markdown)

### Ways of improvement

Current version of Stacosys fits my needs and it serves comments on [my blog](http://blogduyax.madyanne.fr) for 6 months. However Stacosys has been designed to serve several blogs and e-mail can be a constraint for some people. So an area of improvement would be to add an administration UI to configure sites, approve or reject comments, keep track of usage statistics and to make e-mail communication optional. I encourage you to fork the project and create such improvements if you need them. I'll be happy to see the project evolving and growing according to users needs.      
