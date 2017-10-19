import json
import os
import pw
import pyperclip
import unittest
# from unittest.mock import patch


class TestPw(unittest.TestCase):

    def setUp(self):
        """Call initialize() to create a JSON object. Assert to check
        initialization functions before running other tests.
        Return "f" for testing the following methods' encryption."""

        # Assert initialize() working as expected
        pw.initialize()
        with open("storage.json") as file:
            storage_dict = file.read()
        assert storage_dict == "{}"

        # Assert initialize_storage() working as expected
        self.f = pw.initialize_storage()
        with open("storage.json") as file:
            storage_dict = json.load(file)
        assert storage_dict.get("key")

        # Assert exist_in_storage working as expected
        assert pw.exist_in_storage("accounts", storage_dict)
        assert pw.exist_in_storage("key", storage_dict)

        return self.f

    def tearDown(self):
        os.remove("storage.json")

    def test_load_manager(self):
        """Call load_manager() to load the JSON object and assert is dict"""
        self.assertIsInstance(pw.load_manager(), dict)

    def test_add_new(self):
        """Call add_new() to add a new pair into the dict, and assert it exists
        in the dict"""
        pw.add_new("test_add_account", "test_value", self.f)
        self.assertTrue(pw.exist_in_storage("test_add_account",
                                            pw.load_manager()))

        pw.add_new("test_add_account1", "test_value1", self.f)
        self.assertTrue(pw.exist_in_storage("test_add_account1",
                                            pw.load_manager()))

    def test_retrieve(self):
        """add_new() pair into the dict, retrieve it and assert that the
        retrieved value which has been copied to the clipboard is the newly
        added pair's value"""
        pw.add_new("test_retrieve_account", "test_value", self.f)
        pw.retrieve("test_retrieve_account", self.f)
        self.assertEqual(pyperclip.paste(), "test_value")

        pw.add_new("test_retrieve_account1", "test_value1", self.f)
        pw.retrieve("test_retrieve_account1", self.f)
        self.assertEqual(pyperclip.paste(), "test_value1")

    def test_update(self):
        """add_new() pair into the dict. Update the pair's value and retrieve
        the new value. Assert that the retrieved value copied to the clipboard
        has been updated with the newer value."""
        pw.add_new("test_update_account", "test_value", self.f)
        pw.update("test_update_account", "new_test_value", self.f)
        pw.retrieve("test_update_account", self.f)
        self.assertEqual(pyperclip.paste(), "new_test_value")

    def test_delete(self):
        """add_new() pair into the dict. Delete the pair, and assert that the
        pair no longer exists in storage."""
        pw.add_new("test_delete_account", "test_value", self.f)
        self.assertTrue(pw.exist_in_storage("test_delete_account",
                        pw.load_manager()))
        pw.delete("test_delete_account")
        self.assertFalse(pw.exist_in_storage("test_delete_account",
                         pw.load_manager()))


if __name__ == '__main__':
    unittest.main()
