#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pytest

from stacosys.service import mailer


def test_configure_and_check():
    mailer.configure_smtp("localhost", 2525, "admin", "admin")
    mailer.configure_destination("admin@mydomain.com")
    with pytest.raises(ConnectionRefusedError):
        mailer.check()
