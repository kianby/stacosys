#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with https://app.quicktype.io
#   name: stacosys

json_schema = """
{
    "$schema": "http://json-schema.org/draft-06/schema#",
    "$ref": "#/definitions/Welcome",
    "definitions": {
        "Welcome": {
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
                }
            },
            "required": [
                "general",
                "http",
                "rss",
                "security"
            ],
            "title": "Welcome"
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
            "title": "General"
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
            "title": "HTTP"
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
            "title": "RSS"
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
                }
            },
            "required": [
                "salt",
                "secret"
            ],
            "title": "Security"
        }
    }
}
"""