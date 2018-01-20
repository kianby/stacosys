#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with https://app.quicktype.io
#   name: stacosys

json_schema = """
{
    "$ref": "#/definitions/Stacosys",
    "definitions": {
        "Stacosys": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "general": {
                    "$ref": "#/definitions/General"
                },
                "http": {
                    "$ref": "#/definitions/HTTP"
                },
                "security": {
                    "$ref": "#/definitions/Security"
                },
                "rss": {
                    "$ref": "#/definitions/RSS"
                },
                "zmq": {
                    "$ref": "#/definitions/Zmq"
                }
            },
            "required": [
                "general",
                "http",
                "rss",
                "security",
                "zmq"
            ],
            "title": "stacosys"
        },
        "General": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "debug": {
                    "type": "boolean"
                },
                "lang": {
                    "type": "string"
                },
                "db_url": {
                    "type": "string"
                }
            },
            "required": [
                "db_url",
                "debug",
                "lang"
            ],
            "title": "general"
        },
        "HTTP": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "root_url": {
                    "type": "string"
                },
                "host": {
                    "type": "string"
                },
                "port": {
                    "type": "integer"
                }
            },
            "required": [
                "host",
                "port",
                "root_url"
            ],
            "title": "http"
        },
        "RSS": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "proto": {
                    "type": "string"
                },
                "file": {
                    "type": "string"
                }
            },
            "required": [
                "file",
                "proto"
            ],
            "title": "rss"
        },
        "Security": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "salt": {
                    "type": "string"
                },
                "secret": {
                    "type": "string"
                },
                "private": {
                    "type": "boolean"
                }
            },
            "required": [
                "private",
                "salt",
                "secret"
            ],
            "title": "security"
        },
        "Zmq": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "host": {
                    "type": "string"
                },
                "pub_port": {
                    "type": "integer"
                },
                "sub_port": {
                    "type": "integer"
                }
            },
            "required": [
                "host",
                "pub_port",
                "sub_port"
            ],
            "title": "zmq"
        }
    }
}
"""