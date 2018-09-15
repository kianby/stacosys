## Stacosys

Stacosys (aka STAtic blog COmment SYStem) is a fork of [Pecosys](http://github.com/kianby/pecosys) trying to fix Pecosys design drawbacks and to provide an alternative to hosting services like Disqus. Stacosys protects your readers's privacy.

Stacosys works with any static blog or even a simple HTML page. It  privilegiates e-mails to communicate with the blog administrator. It doesn't sound *hype* but I'm an old-school guy ;-) E-mail is reliable and an
universal way to discuss. You can answer from any device using an e-mail client.

###  Features overview

Stacosys main feature is comment management.

Here is the workflow:

-    Readers submit comments via a comment form embedded in blog pages
-    Blog administrator receives an email notification from Stacosys when a
     comment is submitted
-    Blog administrator can approve or drop the comment by replying to e-mail
-    Stacosys stores approved comment in its database.

Stacosys is localized (english and french).

### Technically speaking, how does it work?

Stacosys can be hosted on the same server or on a different server than the blog. Stacosys offers a REST API to retrieve and post comments. Static blog is HTML-based and a piece of JavaScript code interacts with Stacosys using HTTP requests. Each page has a unique id and a simple request allows to retrieve comments for a given page. Similarly a POST request allows to send a comment from reader browser to Stacosy server. The comment post is relayed to the administrator by e-mail. for this purpose a dedicated email is assigned to Stacosys to communicate with blog administrator and blog subscribers.

### FAQ

*How do you block spammers?*
- Current comment form is basic: no captcha support but a honey pot. Second defense barrier: admin can tag comment as SPAM and, for example, link stacosys log to fail2ban tool. 

*Which database is used?*
- Thanks to Peewee ORM a wide range of databases is supported. I personnaly uses SQLite.

*Which technologies are used?*

-    [Python](https://www.python.org)
-    [Flask](http://flask.pocoo.org)
-    [Peewee ORM](http://docs.peewee-orm.com)
-    [Markdown](http://daringfireball.net/projects/markdown)

### Installation

Python 3.7

pip libs: flask peewee pyrss2gen markdown clize flask-apscheduler profig

### Ways of improvement

Current version of Stacosys fits my needs and it serves comments on [my blog](https://blogduyax.madyanne.fr). However Stacosys has been designed to serve several blogs and e-mail can be a constraint for some people. So an area of improvement would be to add an administration UI to configure sites, approve or reject comments, keep track of usage statistics and get rid of e-mails. I encourage you to fork the project and create such improvements if you need them.
