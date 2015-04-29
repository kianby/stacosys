#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
import json
import logging
from clize import clize, run


# configure logging
level = logging.DEBUG
logger = logging.getLogger(__name__)
logger.setLevel(level)
ch = logging.StreamHandler()
ch.setLevel(level)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# regex
regex = re.compile(r"(\w+):\s*(.*)")


def convert_comment(config, filename):
    logger.info('convert %s' % filename)
    d = {}
    with open(filename) as f:
        for line in f:
            match = regex.match(line)
            if match:
                d[match.group(1)] = match.group(2)
            else:
                break
    logger.debug(d)


def convert(config):
    comment_dir = config['comments']
    logger.info('Comment directory %s' % comment_dir)
    for dirpath, dirs, files in os.walk(comment_dir):
        for filename in files:
            if filename.endswith(('.md',)):
                comment_file = '/'.join([dirpath, filename])
                convert_comment(config, comment_file)
            else:
                logger.debug('ignore file %s' % filename)


def load_config(config_pathname):
    logger.info("Load config from %s" % config_pathname)
    with open(config_pathname, 'rt') as config_file:
        config = json.loads(config_file.read())
        return config


@clize
def pecosys2stacosys(config_pathname):
    config = load_config(config_pathname)
    convert(config)


if __name__ == '__main__':
    run(pecosys2stacosys)
