import os
import pw
import pyperclip
import unittest
# from unittest.mock import patch


class TestPw(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pw.initialize()
        f = pw.initialize_storage()
        cls.f = f
        return cls.f

    def test_load_manager(self):
        self.assertIsInstance(pw.load_manager(), dict)

    def test_add_new(self):
        pw.add_new("test_account", "test_value", self.f)
        self.assertTrue(pw.exist_in_storage("test_account", pw.load_manager()))

    def test_retrieve(self):
        pw.add_new("test_account", "test_value", self.f)
        pw.retrieve("test_account", self.f)
        self.assertEqual(pyperclip.paste(), "test_value")

    def test_update(self):
        pw.add_new("test_account", "test_value", self.f)
        pw.update("test_account", "new_test_value", self.f)
        pw.retrieve("test_account", self.f)
        self.assertEqual(pyperclip.paste(), "new_test_value")

    def test_delete(self):
        pw.delete("test_account")
        self.assertFalse(pw.exist_in_storage("test_account",
                         pw.load_manager()))

    @classmethod
    def tearDownClass(cls):
        os.remove("storage.json")


if __name__ == '__main__':
    unittest.main()
