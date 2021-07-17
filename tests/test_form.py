import unittest

from stacosys.interface import form


class FormInterfaceTestCase(unittest.TestCase):

    def test_check_form_data_ok(self):
        d = {"url": "/", "message": "", "site": "", "remarque": "", "author": "", "token": "", "email": ""}
        self.assertTrue(form.check_form_data(d))
        d = {"url": "/"}
        self.assertTrue(form.check_form_data(d))
        d = {}
        self.assertTrue(form.check_form_data(d))

    def test_check_form_data_ko(self):
        d = {"url": "/", "message": "", "site": "", "remarque": "", "author": "", "token": "", "email": "", "bonus": ""}
        self.assertFalse(form.check_form_data(d))


if __name__ == '__main__':
    unittest.main()
