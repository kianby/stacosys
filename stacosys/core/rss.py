#!/usr/bin/python
# -*- coding: UTF-8 -*-

from datetime import datetime

import markdown
import PyRSS2Gen

import stacosys.conf.config as config
from stacosys.core.templater import get_template
from stacosys.model.comment import Comment
from stacosys.model.site import Site


class Rss:
    def __init__(self, lang, rss_file, rss_proto):
        self._lang = lang
        self._rss_file = rss_file
        self._rss_proto = rss_proto

    def generate_all(self):

        for site in Site.select():
            self._generate_site(site.token)

    def _generate_site(self, token):

        site = Site.select().where(Site.token == token).get()
        rss_title = get_template(self._lang, "rss_title_message").render(site=site.name)
        md = markdown.Markdown()

        items = []
        for row in (
            Comment.select()
            .join(Site)
            .where(Site.token == token, Comment.published)
            .order_by(-Comment.published)
            .limit(10)
        ):
            item_link = "%s://%s%s" % (self._rss_proto, site.url, row.url)
            items.append(
                PyRSS2Gen.RSSItem(
                    title="%s - %s://%s%s"
                    % (self._rss_proto, row.author_name, site.url, row.url),
                    link=item_link,
                    description=md.convert(row.content),
                    guid=PyRSS2Gen.Guid("%s/%d" % (item_link, row.id)),
                    pubDate=row.published,
                )
            )

        rss = PyRSS2Gen.RSS2(
            title=rss_title,
            link="%s://%s" % (self._rss_proto, site.url),
            description='Commentaires du site "%s"' % site.name,
            lastBuildDate=datetime.now(),
            items=items,
        )
        rss.write_xml(open(self._rss_file, "w"), encoding="utf-8")
