import os
import pw
import unittest
from unittest import mock

class TestPw(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pw.initialize()
        f = pw.initialize_storage()

    def test_add_new(self):

    def test_retrieve(self):
        pass
    def test_update(self):
        pass
    def test_delete(self):
        pass

    @classmethod
    def tearDownClass(cls):
        os.remove("storage.json")


if name == '__main__': unittest.main()