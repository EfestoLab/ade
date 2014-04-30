import os
import unittest
import logging
from ade.manager.filesystem import FileSystemManager
from ade.manager.template import TemplateManager

logging.getLogger('ade')


class Test_FilesystemManager(unittest.TestCase):

    def setUp(self):
        # Create a new template manager pointing to the test templates folder
        template_paths = os.path.realpath('test/data/templates')
        self.template_manager = TemplateManager(template_paths)
        self.data = {'test_A': 'Hello', 'test_B': 'World'}
        self.root_path  = '/tmp'

    def test_permissions(self):
        filesystem_manager = FileSystemManager(self.root_path, self.template_manager)
        resolved_template = filesystem_manager.template_manager.resolve_template('@+test_A+@')
        results = filesystem_manager.template_manager.resolve(resolved_template)
        path_results = filesystem_manager._to_path(results, self.data)
        permission_results = [item['permission'] for item in path_results]
        expected_results = [
            '0755', '0755', '0644', '0755', '0755',
            '0755', '0755', '0755', '0644', '0755'
        ]
        self.assertEqual(permission_results, expected_results)

    def test_template_to_parser(self):
        filesystem_manager = FileSystemManager(self.root_path, self.template_manager)
        resolved_template = filesystem_manager.template_manager.resolve_template('@+test_A+@')
        results = filesystem_manager.template_manager.resolve(resolved_template)
        parsers_results = filesystem_manager._to_parser(results)
        expected_path = [
            '^(?P<test_A>[a-zA-Z0-9_]+)/test_A1$',
            '^(?P<test_A>[a-zA-Z0-9_]+)/(?P<test_B>[a-zA-Z0-9_]+)$',
            '^(?P<test_A>[a-zA-Z0-9_]+)/(?P<test_B>[a-zA-Z0-9_]+)/test_C$',
            '^(?P<test_A>[a-zA-Z0-9_]+)/(?P<test_B>[a-zA-Z0-9_]+)/test_B2$',
            '^(?P<test_A>[a-zA-Z0-9_]+)/(?P<test_B>[a-zA-Z0-9_]+)/test_B1$',
            '^(?P<test_A>[a-zA-Z0-9_]+)/(?P<test_B>[a-zA-Z0-9_]+)/file_B.txt$',
            '^(?P<test_A>[a-zA-Z0-9_]+)/(?P<test_B>[a-zA-Z0-9_]+)/test_C/test_C1$',
            '^(?P<test_A>[a-zA-Z0-9_]+)/(?P<test_B>[a-zA-Z0-9_]+)/test_C/test_C1/test_D$',
            '^(?P<test_A>[a-zA-Z0-9_]+)/(?P<test_B>[a-zA-Z0-9_]+)/test_C/test_C1/test_D/test_D1$',
            '^(?P<test_A>[a-zA-Z0-9_]+)/(?P<test_B>[a-zA-Z0-9_]+)/test_C/test_C1/test_D/file_D.txt$',
        ]
        self.assertEqual(parsers_results, expected_path)

    def test_template_to_path(self):
        filesystem_manager = FileSystemManager(self.root_path, self.template_manager)
        resolved_template = filesystem_manager.template_manager.resolve_template('@+test_A+@')
        results = filesystem_manager.template_manager.resolve(resolved_template)
        path_results = filesystem_manager._to_path(results, self.data)
        path_results = [item['path'] for item in path_results]
        expected_path = [
            'Hello/test_A1',
            'Hello/World',
            'Hello/World/file_B.txt',
            'Hello/World/test_B2',
            'Hello/World/test_C',
            'Hello/World/test_C/test_C1',
            'Hello/World/test_C/test_C1/test_D',
            'Hello/World/test_C/test_C1/test_D/test_D1',
            'Hello/World/test_C/test_C1/test_D/file_D.txt',
            'Hello/World/test_B1'
        ]
        self.assertEqual(path_results, expected_path)

    def test_parse_complete_path(self):
        filesystem_manager = FileSystemManager(self.root_path, self.template_manager)
        test_path = 'Hello/World/test_C/test_D'
        result = filesystem_manager.parse(test_path, '@+test_A+@')
        self.assertEqual(result, self.data)

