from doku.config_manager import ConfigManager
from pathlib import Path
from pyfakefs.fake_filesystem_unittest import TestCase

import os

class TestConfigManager(TestCase):
    configManager = None

    def setUp(self):
        self.setUpPyfakefs()
        self.config = ConfigManager()

    def test_default_value_without_file(self):
        with self.assertRaises(FileNotFoundError):
            self.config.get('settings', 'indexpage', 'index')

    def test_default_value_with_empty_file(self):
        self.fs.create_file(os.path.join(Path.home(), '.doku.ini'))

        expected = 'index'
        value = self.config.get('settings', 'indexpage', 'index')
        self.assertEqual(value, expected)

    def test_defined_value(self):
        self.fs.create_file(
            os.path.join(Path.home(), '.doku.ini'),
            contents='''[settings]\nindexpage = root\n'''
        )

        expected = 'root'
        value = self.config.get('settings', 'indexpage', 'index')
        self.assertEqual(value, expected)

        expected = 'random'
        value = self.config.get('settings', 'randompage', 'random')
        self.assertEqual(value, expected)

    def test_sections(self):
        self.fs.create_file(
            os.path.join(Path.home(), '.doku.ini'),
            contents='''[settings]\nindexpage = root\n'''
        )

        expected = ['settings']
        value = self.config.sections()
        self.assertEqual(value, expected)

    def test_sections_empty(self):
        self.fs.create_file(os.path.join(Path.home(), '.doku.ini'))

        expected = []
        value = self.config.sections()
        self.assertEqual(value, expected)

    def test_defined_value_as_dict(self):
        self.fs.create_file(
            os.path.join(Path.home(), '.doku.ini'),
            contents='''[settings]\nindexpage = root\n'''
        )

        expected = 'root'
        value = self.config['settings']['indexpage']
        self.assertEqual(value, expected)

        value = self.config['somethingelse']
        self.assertIsNone(value, expected)
