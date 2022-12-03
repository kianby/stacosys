[![GitLicense](https://gitlicense.com/badge/kianby/stacosys)](https://gitlicense.com/license/kianby/stacosys)
 [![Python version](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Flask version](https://img.shields.io/badge/Flask-2.1-green.svg)](https://flask.palletsprojects.com) 

[![Build Status - pytest](https://github.com/kianby/stacosys/workflows/pytest/badge.svg)](https://github.com/kianby/stacosys) [![Coverage Status](https://coveralls.io/repos/github/kianby/stacosys/badge.svg?branch=main)](https://coveralls.io/github/kianby/stacosys?branch=main) [![Build status - docker image](https://github.com/kianby/stacosys/workflows/docker/badge.svg)](https://hub.docker.com/r/kianby/stacosys)

## Stacosys

Stacosys (aka STAtic blog COmment SYStem) is a fork of [Pecosys](http://github.com/kianby/pecosys) trying to fix Pecosys design drawbacks and to provide a basic alternative to comment hosting services like Disqus. Stacosys works with any static blog or even a simple HTML page. 

###  Features overview

Stacosys main feature is comment management.

Here is the workflow:

-    Readers submit comments via a comment form embedded in blog pages
-    Blog administrator receives an e-mail notification from Stacosys when a
     comment is submitted
-    Blog administrator can approve or drop the comment through a simple web admin interface
-    Stacosys stores approved comment in its database.

Privacy concerns: only surname, gravatar id and comment itself are stored in DB. E-mail is optionally requested in submission form to resolve gravatar id but never sent to Stacosys.

Stacosys is more or less localized (english and french).

### Technically speaking, how does it work?

Stacosys offers a REST API to retrieve and post comments. Static blog is HTML-based and a piece of JavaScript code interacts with Stacosys using HTTP requests. Each page has a unique id and a request allows retrieving comments for a given page. Similarly, a form request allows to post a comment which is relayed to the administrator by e-mail. For this purpose an SMTP configuration is needed.

### Little FAQ

*How do you block spammers?*

- Current comment form is basic: no captcha support but protected by a honeypot. 

*Which database is used?*

- SQLite.

*Which technologies are used?*

-    [Python](https://www.python.org)
-    [Flask](http://flask.pocoo.org)
-    [Markdown](http://daringfireball.net/projects/markdown)

### Installation

Build and Dependency management relies on [Poetry](https://python-poetry.org/), but you can also use [published releases](https://github.com/kianby/stacosys/releases) or [Docker image](https://hub.docker.com/r/kianby/stacosys).

### Improvements

Stacosys fits my needs, and it manages comments on [my blog](https://blogduyax.madyanne.fr) for a while. I don't have any plan to make big changes, it's more a python playground for me. So I strongly encourage you to fork and enhance the project if you need additional features.
