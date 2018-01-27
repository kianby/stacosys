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
                "rabbitmq": {
                    "$ref": "#/definitions/Rabbitmq"
                }
            },
            "required": [
                "general",
                "http",
                "rabbitmq",
                "rss",
                "security"
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
        "Rabbitmq": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "active": {
                    "type": "boolean"
                },
                "host": {
                    "type": "string"
                },
                "port": {
                    "type": "integer"
                },
                "username": {
                    "type": "string"
                },
                "password": {
                    "type": "string"
                },
                "vhost": {
                    "type": "string"
                },
                "exchange": {
                    "type": "string"
                }
            },
            "required": [
                "active",
                "exchange",
                "host",
                "password",
                "port",
                "username",
                "vhost"
            ],
            "title": "rabbitmq"
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
        }
    }
}
"""