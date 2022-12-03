#!/usr/bin/python
# -*- coding: UTF-8 -*-

from datetime import datetime

import markdown
import PyRSS2Gen

from stacosys.db import dao


class Rss:
    def __init__(self) -> None:
        self._rss_file: str = ""
        self._site_proto: str = ""
        self._site_name: str = ""
        self._site_url: str = ""

    def configure(
        self,
        rss_file,
        site_name,
        site_proto,
        site_url,
    ) -> None:
        self._rss_file = rss_file
        self._site_name = site_name
        self._site_proto = site_proto
        self._site_url = site_url

    def generate(self) -> None:
        markdownizer = markdown.Markdown()

        items = []
        for row in dao.find_recent_published_comments():
            item_link = f"{self._site_proto}://{self._site_url}{row.url}"
            items.append(
                PyRSS2Gen.RSSItem(
                    title=f"{self._site_proto}://{self._site_url}{row.url} - {row.author_name}",
                    link=item_link,
                    description=markdownizer.convert(row.content),
                    guid=PyRSS2Gen.Guid(f"{item_link}{row.id}"),
                    pubDate=row.published,
                )
            )

        rss_title = f"Commentaires du site {self._site_name}"
        rss = PyRSS2Gen.RSS2(
            title=rss_title,
            link=f"{self._site_proto}://{self._site_url}",
            description=rss_title,
            lastBuildDate=datetime.now(),
            items=items,
        )
        # pylint: disable=consider-using-with
        rss.write_xml(open(self._rss_file, "w", encoding="utf-8"), encoding="utf-8")
