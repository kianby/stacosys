#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
import time
from datetime import datetime

from core import mailer, rss
from core.templater import get_template
from model.comment import Comment, Site
from model.email import Email

logger = logging.getLogger(__name__)


def cron(func):
    def wrapper():
        logger.debug('execute CRON ' + func.__name__)
        func()

    return wrapper


@cron
def fetch_mail_answers():

    for msg in mailer.fetch():
        if re.search(r'.*STACOSYS.*\[(\d+)\:(\w+)\]', msg.subject, re.DOTALL):
            if _reply_comment_email(msg):
                mailer.delete(msg.id)


@cron
def submit_new_comment():

    for comment in Comment.select().where(Comment.notified.is_null()):

        comment_list = (
            'author: %s' % comment.author_name,
            'site: %s' % comment.author_site,
            'date: %s' % comment.created,
            'url: %s' % comment.url,
            '',
            '%s' % comment.content,
            '',
        )
        comment_text = '\n'.join(comment_list)
        email_body = get_template('new_comment').render(
            url=comment.url, comment=comment_text
        )

        # send email
        site = Site.get(Site.id == comment.site)
        subject = 'STACOSYS %s: [%d:%s]' % (site.name, comment.id, site.token)
        if mailer.send(site.admin_email, subject, email_body):
            logger.debug('new comment processed ')

            # notify site admin and save notification datetime
            comment.notify_site_admin()
        else:
            logger.warn('rescheduled. send mail failure ' + subject)


def _reply_comment_email(email : Email):

    m = re.search(r'\[(\d+)\:(\w+)\]', email.subject)
    if not m:
        logger.warn('ignore corrupted email. No token %s' % email.subject)
        return
    comment_id = int(m.group(1))
    token = m.group(2)

    # retrieve site and comment rows
    try:
        comment = Comment.select().where(Comment.id == comment_id).get()
    except:
        logger.warn('unknown comment %d' % comment_id)
        return True

    if comment.published:
        logger.warn('ignore already published email. token %d' % comment_id)
        return

    if comment.site.token != token:
        logger.warn('ignore corrupted email. Unknown token %d' % comment_id)
        return

    if not email.plain_text_content:
        logger.warn('ignore empty email')
        return

    # safe logic: no answer or unknown answer is a go for publishing
    if email.plain_text_content[:2].upper() in ('NO'):
        logger.info('discard comment: %d' % comment_id)
        comment.delete_instance()
        new_email_body = get_template('drop_comment').render(original=email.plain_text_content)
        if not mailer.send(email.from_addr, 'Re: ' + email.subject, new_email_body):
            logger.warn('minor failure. cannot send rejection mail ' + email.subject)
    else:
        # save publishing datetime
        comment.publish()
        logger.info('commit comment: %d' % comment_id)

        # rebuild RSS
        rss.generate_site(token)

        # send approval confirmation email to admin
        new_email_body = get_template('approve_comment').render(original=email.plain_text_content)
        if not mailer.send(email.from_addr, 'Re: ' + email.subject, new_email_body):
            logger.warn('minor failure. cannot send approval email ' + email.subject)

    return True
