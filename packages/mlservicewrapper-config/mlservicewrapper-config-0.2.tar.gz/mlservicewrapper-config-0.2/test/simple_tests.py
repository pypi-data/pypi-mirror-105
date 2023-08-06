import os
import unittest

import mlservicewrapper.config

_config_dir = os.path.dirname(__file__)
_base_config_path = os.path.join(_config_dir, "config.base.json")
_overridden_config_path = os.path.join(_config_dir, "advanced", "config.overrides.json")

class TestBaseConfig(unittest.TestCase):
    
    def load_config(self):
        return mlservicewrapper.config.from_file(_base_config_path)

    def test_load_base_config(self):
        config = self.load_config()
        
        self.assertIsNotNone(config, "Base config should not be None.")

    def test_read_number(self):
        config = self.load_config()

        val = config.get_value("numberValue", dtype=int, required=True)

        self.assertIsInstance(val, int, "numberValue must be an int")
        self.assertEqual(val, 123, "numberValue from base config should be 123")

    def test_read_string(self):
        config = self.load_config()

        val = config.get_value("stringValue", dtype=str, required=True)

        self.assertIsInstance(val, str, "stringValue must be a str")
        self.assertEqual(val, "this is a string", "stringValue not read from base config")

    def test_read_missing_prop(self):
        config = self.load_config()

        self.assertRaises(ValueError, config.get_value, "notThere", dtype=str, required=True)

    def test_read_dict(self):
        config = self.load_config()

        d = config.get_dict_value("dictValue", required=True)

        self.assertIsNotNone(d, "dictValue must not be None")
        self.assertIsInstance(d, dict, "dictValue must be a dict")

        self.assertEqual(len(d), 3)
        self.assertEqual(d["a"], 1)
        self.assertEqual(d["b"], 2)
        self.assertEqual(d["c"], 3)


class TestOverriddenConfig(unittest.TestCase):
    
    def load_config(self):
        return mlservicewrapper.config.from_file(_overridden_config_path)

    def test_load_base_config(self):
        config = self.load_config()
        
        self.assertIsNotNone(config, "Base config should not be None.")

    def test_read_number(self):
        config = self.load_config()

        val = config.get_value("numberValue", dtype=int, required=True)

        self.assertEqual(val, 456, "numberValue from base config should be 123")

    def test_read_base_string(self):
        config = self.load_config()

        val = config.get_value("stringValue", dtype=str, required=True)

        self.assertEqual(val, "this is a string", "stringValue not read from base config")

    def test_read_path(self):
        config = self.load_config()

        val = config.get_fully_qualified_path("pathValue", required=True)
        expected = os.path.join(os.path.dirname(__file__), "advanced", "config.something-else.json")

        is_same = os.path.samefile(val, expected)

        self.assertTrue(is_same, "pathValue should point to config.something-else.json")

    def test_read_missing_required_prop(self):
        config = self.load_config()

        self.assertRaises(ValueError, config.get_value, "notThere", dtype=str, required=True)

    def test_read_missing_optional_prop(self):
        config = self.load_config()

        val = config.get_value("notThere", dtype=str, required=False)

        self.assertIsNone(val, "missing property should return None")


if __name__ == "__main__":
    unittest.main()

