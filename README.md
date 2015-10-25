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
- Right! Stacosys is written in Python and it uses Flask Web framework. You
  keeps on serving static pages for the blog but you have to link two URL with
  Pecosys. If you use NginX or Apache2 (with Proxy modules), it's not a big
  deal.

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

