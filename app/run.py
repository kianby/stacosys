#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import json
from clize import Clize, run
from jsonschema import validate
from conf import config, schema


def load_json(filename):
    jsondoc = None
    with open(filename, 'rt') as json_file:
        jsondoc = json.loads(json_file.read())
    return jsondoc


@Clize
def stacosys_server(config_pathname):

    # load and validate startup config
    conf = load_json(config_pathname)
    json_schema = json.loads(schema.json_schema)
    validate(conf, json_schema)

    # set configuration
    config.general = conf['general']
    config.http = conf['http']
    config.security = conf['security']
    config.rss = conf['rss']

    # start application
    from core import app

if __name__ == '__main__':
    run(stacosys_server)
