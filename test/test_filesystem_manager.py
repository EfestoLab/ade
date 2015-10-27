import os
import unittest
import logging
import tempfile
from ade.manager.filesystem import FileSystemManager
from ade.manager.template import TemplateManager
from ade.manager.config import ConfigManager

log = logging.getLogger(__name__)


class Test_FilesystemManager(unittest.TestCase):

    def setUp(self):
        """Setup test session.
        """
        self.maxDiff = None
        config = 'test/resources/config'
        os.environ['ADE_CONFIG_PATH'] = config
        config_manager = ConfigManager(config)
        config_mode = config_manager.get('test')
        self.tmp = tempfile.mkdtemp()
        config_mode['project_mount_point'] = self.tmp
        self.config_mode = config_mode

        self.template_manager = TemplateManager(self.config_mode)
        self.data = {'test_A': 'Hello', 'test_B': 'World'}

    # def test_permissions(self):
    #     """Check whether the permissions are the correct one once rebuilt.
    #     """
    #     filesystem_manager = FileSystemManager(
    #         self.config_mode, self.template_manager
    #     )
    #     resolved_template = filesystem_manager.template_manager.resolve_template('@+test_A+@')
    #     results = filesystem_manager.template_manager.resolve(resolved_template)
    #     path_results = filesystem_manager._to_path(results, self.data)
    #     permission_results = [item['permission'] for item in path_results]
    #     expected_results = [
    #         '0775', '0775', '0775',
    #         '0775', '0775', '0775',
    #         '0775', '0775', '0775',
    #         '0775', '0775'
    #     ]
    #     self.assertEqual(permission_results, expected_results)

    # def test_template_to_parser(self):
    #     """ Build the template structure and convert it to parser
    #     """
    #     filesystem_manager = FileSystemManager(self.config_mode, self.template_manager)
    #     resolved_template = filesystem_manager.template_manager.resolve_template('@+test_A+@')
    #     results = filesystem_manager.template_manager.resolve(resolved_template)
    #     parsers_results = filesystem_manager._to_parser(results)
    #     expected_path = [
    #         '^(?P<test_A>[a-zA-Z0-9_]+)$',
    #         '^(?P<test_A>[a-zA-Z0-9_]+)/test_A1$',
    #         '^(?P<test_A>[a-zA-Z0-9_]+)/(?P<test_B>[a-zA-Z0-9_]+)$',
    #         '^(?P<test_A>[a-zA-Z0-9_]+)/(?P<test_B>[a-zA-Z0-9_]+)/test_C$',
    #         '^(?P<test_A>[a-zA-Z0-9_]+)/(?P<test_B>[a-zA-Z0-9_]+)/test_B2$',
    #         '^(?P<test_A>[a-zA-Z0-9_]+)/(?P<test_B>[a-zA-Z0-9_]+)/test_B1$',
    #         '^(?P<test_A>[a-zA-Z0-9_]+)/(?P<test_B>[a-zA-Z0-9_]+)/file_B.txt$',
    #         '^(?P<test_A>[a-zA-Z0-9_]+)/(?P<test_B>[a-zA-Z0-9_]+)/test_C/test_C1$',
    #         '^(?P<test_A>[a-zA-Z0-9_]+)/(?P<test_B>[a-zA-Z0-9_]+)/test_C/test_C1/test_D$',
    #         '^(?P<test_A>[a-zA-Z0-9_]+)/(?P<test_B>[a-zA-Z0-9_]+)/test_C/test_C1/test_D/test_D1$',
    #         '^(?P<test_A>[a-zA-Z0-9_]+)/(?P<test_B>[a-zA-Z0-9_]+)/test_C/test_C1/test_D/file_D.txt$',
    #     ]
    #     self.assertEqual(parsers_results, expected_path)

    # def test_template_to_path(self):
    #     """ Build the template structure and convert it to path
    #     """
    #     filesystem_manager = FileSystemManager(
    #         self.config_mode,
    #         self.template_manager
    #     )
    #     resolved_template = filesystem_manager.template_manager.resolve_template('@+test_A+@')
    #     results = filesystem_manager.template_manager.resolve(
    #         resolved_template
    #     )
    #     path_results = filesystem_manager._to_path(results, self.data)
    #     path_results = [item['path'] for item in path_results]
    #     expected_path = [
    #         u'Hello',
    #         u'Hello/test_A1',
    #         u'Hello/World',
    #         u'Hello/World/file_B.txt',
    #         u'Hello/World/test_B2',
    #         u'Hello/World/test_B1',
    #         u'Hello/World/test_C',
    #         u'Hello/World/test_C/test_C1',
    #         u'Hello/World/test_C/test_C1/test_D',
    #         u'Hello/World/test_C/test_C1/test_D/file_D.txt',
    #         u'Hello/World/test_C/test_C1/test_D/test_D1'
    #     ]

    #     self.assertEqual(path_results, expected_path)

    def test_parse_complete_path(self):
        """Check parse of a complete path.
        """
        filesystem_manager = FileSystemManager(
            self.config_mode, self.template_manager
        )
        test_path = self.tmp+'/Hello/World'
        filesystem_manager.build('@+test_A+@', self.data, test_path)

        result = filesystem_manager.parse(test_path, '@+test_A+@')
        self.assertEqual(result[0], self.data)

    def test_parse_root_path(self):
        '''Parse the root path only of the project,
            This is to check the bug which was affecting it.
        '''
        filesystem_manager = FileSystemManager(
            self.config_mode, self.template_manager
        )
        test_path = self.tmp+'/Hello'

        filesystem_manager.build('@+test_A+@', self.data, test_path)
        result = filesystem_manager.parse(test_path, '@+test_A+@')
        self.assertEqual(result[0], {'test_A': 'Hello'})

    def test_parse_trailing_path(self):
        ''' Check trailing slashes in path to parse
        '''
        filesystem_manager = FileSystemManager(
            self.config_mode, self.template_manager
        )
        test_path = self.tmp+'/Hello/'
        filesystem_manager.build('@+test_A+@', self.data, test_path)
        result = filesystem_manager.parse(test_path, '@+test_A+@')
        self.assertEqual(result[0], {'test_A': 'Hello'})

    def test_template_to_parser_prefix(self):
        """ Build the template structure and convert it to parser
        """
        filesystem_manager = FileSystemManager(self.config_mode, self.template_manager)
        resolved_template = filesystem_manager.template_manager.resolve_template('@+test_F+@')
        results = filesystem_manager.template_manager.resolve(resolved_template)
        parsers_results = filesystem_manager._to_parser(results)
        expected_path = [
            '^(?P<test_E>[a-zA-Z0-9_]+)$',
            '^(?P<test_E>[a-zA-Z0-9_]+)/pfx_(?P<test_E>[a-zA-Z0-9_]+)_sfx$',
            '^(?P<test_E>[a-zA-Z0-9_]+)/pfx_(?P<test_E>[a-zA-Z0-9_]+)_sfx/test_D$',
            '^(?P<test_E>[a-zA-Z0-9_]+)/pfx_(?P<test_E>[a-zA-Z0-9_]+)_sfx/test_D/test_D1$',
            '^(?P<test_E>[a-zA-Z0-9_]+)/pfx_(?P<test_E>[a-zA-Z0-9_]+)_sfx/test_D/file_D.txt$'
        ]
        self.assertEqual(parsers_results, expected_path)

    def test_template_to_path_prefix(self):
        """ Build the template structure and convert it to path
        """
        filesystem_manager = FileSystemManager(self.config_mode, self.template_manager)
        resolved_template = filesystem_manager.template_manager.resolve_template('@+test_F+@')
        results = filesystem_manager.template_manager.resolve(resolved_template)
        data = {'test_E': 'ZOOO', 'test_F': 'BOOO'}
        path_results = filesystem_manager._to_path(results, data)
        path_results = [item['path'] for item in path_results]
        expected_path = [
            u'BOOO',
            u'BOOO/pfx_ZOOO_sfx',
            u'BOOO/pfx_ZOOO_sfx/test_D',
            u'BOOO/pfx_ZOOO_sfx/test_D/test_D1',
            u'BOOO/pfx_ZOOO_sfx/test_D/file_D.txt'
        ]
        self.assertEqual(path_results, expected_path)
