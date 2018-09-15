#!/usr/bin/python
# -*- coding: UTF-8 -*-

from datetime import datetime
import markdown
import PyRSS2Gen
from model.site import Site
from model.comment import Comment
from core.templater import get_template
from conf import config


def generate_all():
    for site in Site.select():
        generate_site(site.token)


def generate_site(token):

    site = Site.select().where(Site.token == token).get()
    rss_title = get_template("rss_title_message").render(site=site.name)
    md = markdown.Markdown()

    items = []
    for row in (
        Comment.select()
        .join(Site)
        .where(Site.token == token, Comment.published)
        .order_by(-Comment.published)
        .limit(10)
    ):
        item_link = "%s://%s%s" % (config.get(config.RSS_PROTO), site.url, row.url)
        items.append(
            PyRSS2Gen.RSSItem(
                title="%s - %s://%s%s"
                % (config.get(config.RSS_PROTO), row.author_name, site.url, row.url),
                link=item_link,
                description=md.convert(row.content),
                guid=PyRSS2Gen.Guid("%s/%d" % (item_link, row.id)),
                pubDate=row.published,
            )
        )

    rss = PyRSS2Gen.RSS2(
        title=rss_title,
        link="%s://%s" % (config.get(config.RSS_PROTO), site.url),
        description="Commentaires du site '%s'" % site.name,
        lastBuildDate=datetime.now(),
        items=items,
    )
    rss.write_xml(open(config.get(config.RSS_FILE), "w"), encoding="utf-8")

