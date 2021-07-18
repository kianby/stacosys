import unittest

from stacosys.db import dao
from stacosys.db import database


class DbTestCase(unittest.TestCase):

    def setUp(self):
        db = database.Database()
        db.setup(":memory:")

    def test_dao_published(self):

        # test count published
        self.assertEqual(0, dao.count_published_comments(""))
        c1 = dao.create_comment("/post1", "Yax", "", "", "Comment 1")
        self.assertEqual(0, dao.count_published_comments(""))
        dao.publish_comment(c1)
        self.assertEqual(1, dao.count_published_comments(""))
        c2 = dao.create_comment("/post2", "Yax", "", "", "Comment 2")
        dao.publish_comment(c2)
        self.assertEqual(2, dao.count_published_comments(""))
        c3 = dao.create_comment("/post2", "Yax", "", "", "Comment 3")
        dao.publish_comment(c3)
        self.assertEqual(1, dao.count_published_comments("/post1"))
        self.assertEqual(2, dao.count_published_comments("/post2"))

        # test find published
        self.assertEqual(0, len(dao.find_published_comments_by_url("/")))
        self.assertEqual(1, len(dao.find_published_comments_by_url("/post1")))
        self.assertEqual(2, len(dao.find_published_comments_by_url("/post2")))

        dao.delete_comment(c1)
        self.assertEqual(0, len(dao.find_published_comments_by_url("/post1")))

    def test_dao_notified(self):

        # test count notified
        self.assertEqual(0, len(dao.find_not_notified_comments()))
        c1 = dao.create_comment("/post1", "Yax", "", "", "Comment 1")
        self.assertEqual(1, len(dao.find_not_notified_comments()))
        c2 = dao.create_comment("/post2", "Yax", "", "", "Comment 2")
        self.assertEqual(2, len(dao.find_not_notified_comments()))
        dao.notify_comment(c1)
        dao.notify_comment(c2)
        self.assertEqual(0, len(dao.find_not_notified_comments()))
        c3 = dao.create_comment("/post2", "Yax", "", "", "Comment 3")
        self.assertEqual(1, len(dao.find_not_notified_comments()))
        dao.notify_comment(c3)
        self.assertEqual(0, len(dao.find_not_notified_comments()))


if __name__ == '__main__':
    unittest.main()
