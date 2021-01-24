#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from datetime import datetime

import markdown
import PyRSS2Gen

from stacosys.core.templater import Templater, Template
from stacosys.model.comment import Comment


class Rss:
    def __init__(
        self,
        lang,
        rss_file,
        rss_proto,
        site_name,
        site_url,
    ):
        self._lang = lang
        self._rss_file = rss_file
        self._rss_proto = rss_proto
        self._site_name = site_name
        self._site_url = site_url
        current_path = os.path.dirname(__file__)
        template_path = os.path.abspath(os.path.join(current_path, "../templates"))
        self._templater = Templater(template_path)

    def generate(self):
        rss_title = self._templater.get_template(
            self._lang, Template.RSS_TITLE_MESSAGE
        ).render(site=self._site_name)
        md = markdown.Markdown()

        items = []
        for row in (
            Comment.select()
            .where(Comment.published)
            .order_by(-Comment.published)
            .limit(10)
        ):
            item_link = "%s://%s%s" % (self._rss_proto, self._site_url, row.url)
            items.append(
                PyRSS2Gen.RSSItem(
                    title="%s - %s://%s%s"
                    % (self._rss_proto, row.author_name, self._site_url, row.url),
                    link=item_link,
                    description=md.convert(row.content),
                    guid=PyRSS2Gen.Guid("%s/%d" % (item_link, row.id)),
                    pubDate=row.published,
                )
            )

        rss = PyRSS2Gen.RSS2(
            title=rss_title,
            link="%s://%s" % (self._rss_proto, self._site_url),
            description='Commentaires du site "%s"' % self._site_name,
            lastBuildDate=datetime.now(),
            items=items,
        )
        rss.write_xml(open(self._rss_file, "w"), encoding="utf-8")
