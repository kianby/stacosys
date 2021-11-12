[![GitLicense](https://gitlicense.com/badge/kianby/stacosys)](https://gitlicense.com/license/kianby/stacosys)
 [![Python version](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/) [![Flask version](https://img.shields.io/badge/Flask-2.0.1-green.svg)](https://flask.palletsprojects.com) [![Peewee version](https://img.shields.io/badge/Peewee-3.14.0-green.svg)](https://docs.peewee-orm.com/)

[![Build Status - pytest](https://github.com/kianby/stacosys/workflows/pytest/badge.svg)](https://github.com/kianby/stacosys) [![Coverage Status](https://coveralls.io/repos/github/kianby/stacosys/badge.svg?branch=master)](https://coveralls.io/github/kianby/stacosys?branch=master) [![Build status - docker image](https://github.com/kianby/stacosys/workflows/docker/badge.svg)](https://hub.docker.com/r/kianby/stacosys)  

## Stacosys

Stacosys (aka STAtic blog COmment SYStem) is a fork of [Pecosys](http://github.com/kianby/pecosys) trying to fix Pecosys design drawbacks and to provide an humble alternative to comment hosting services like Disqus. Stacosys protects your readers's privacy.

Stacosys works with any static blog or even a simple HTML page. It uses e-mails to communicate with the blog administrator. It doesn't sound *hype* but I'm an old-school guy. E-mails are reliable and an universal way to communicate. You can answer from any device using an e-mail client.

###  Features overview

Stacosys main feature is comment management.

Here is the workflow:

-    Readers submit comments via a comment form embedded in blog pages
-    Blog administrator receives an email notification from Stacosys when a
     comment is submitted
-    Blog administrator can approve or drop the comment by replying to e-mail
-    Stacosys stores approved comment in its database.

Privacy concerns: only surname, gravatar id and comment itself are stored in DB. E-mail is requested in submission form (but optional) to resolve gravatar id and it it not sent to stacosys.

Stacosys is localized (english and french).

### Technically speaking, how does it work?

Stacosys can be hosted on the same server or on a different server than the blog. Stacosys offers a REST API to retrieve and post comments. Static blog is HTML-based and a piece of JavaScript code interacts with Stacosys using HTTP requests. Each page has a unique id and a simple request allows to retrieve comments for a given page. Similarly a form request allows to post a comment which is relayed to the administrator by e-mail. For this purpose a dedicated email is assigned to Stacosys.


### Little FAQ

*How do you block spammers?*

- Current comment form is basic: no captcha support but protected by an honey pot. 

*Which database is used?*

- SQLite.

*Which technologies are used?*

-    [Python](https://www.python.org)
-    [Flask](http://flask.pocoo.org)
-    [Peewee ORM](http://docs.peewee-orm.com)
-    [Markdown](http://daringfireball.net/projects/markdown)

### Installation

Build is based on [Poetry](https://python-poetry.org/) but you can also use [published releases](https://github.com/kianby/stacosys/releases) or [Docker image](https://hub.docker.com/r/kianby/stacosys).

### Improvements

Stacosys fits my needs and it manages comments on [my blog](https://blogduyax.madyanne.fr) for a while. I don't have any plan to make big changes, it's more a python playground for me. So I strongly encourage you to fork the project and enhance the project if you need more features.

