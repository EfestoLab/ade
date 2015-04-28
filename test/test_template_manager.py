import os
import unittest
import tempfile
import logging
from pprint import pformat
from collections import OrderedDict

from ade.manager.template import TemplateManager
from ade.manager.config import ConfigManager

logging.getLogger(__name__)


class Test_TemplateManager(unittest.TestCase):

    def setUp(self):
        """Setup test session.
        """
        self.maxDiff = None
        config = 'test/resources/config'
        os.environ['ADE_CONFIG_PATH'] = config
        config_manager = ConfigManager(config)
        config_mode = config_manager.get('test')
        config_mode['project_mount_point'] = tempfile.mkdtemp()
        self.config_mode = config_mode

    def test_register_unexisting_template(self):
        '''Check when template doesn't exist
        '''
        manager = TemplateManager(self.config_mode)
        self.assertRaises(KeyError, manager._get_in_register, '@+test_fake+@')

    def test_registered_templates_is_folder(self):
        '''Check for template folder attributes.
        '''
        manager = TemplateManager(self.config_mode)
        folder_A = manager._get_in_register('@+test_A+@')
        self.assertTrue(folder_A.get('folder', False))
        self.assertTrue(folder_A.get('children', False))
        self.assertEqual(folder_A.get('permission', 000), '0775')

    def test_registered_templates_is_file(self):
        '''Check for template file attributes.
        '''
        manager = TemplateManager(self.config_mode)
        file_D = manager._get_in_register('@test_D@')['children'][-1]
        self.assertFalse(file_D.get('folder'))
        self.assertFalse(file_D.get('children'))
        self.assertEqual(file_D.get('permission', 000), '0775')

    def test_registered_templates(self):
        ''' Register a new template through the config file.
        '''
        manager = TemplateManager(self.config_mode)
        register = manager.register
        expected_result = [
            OrderedDict([
                ('folder', True),
                ('children', [
                    OrderedDict([
                        ('folder', True),
                        ('name', u'@+test_B+@'),
                        ('permission', '0775'),
                        ('children', [
                            OrderedDict([
                                ('folder', False),
                                ('name', u'file_B.txt'),
                                ('permission', '0775'),
                                ('content', 'test')
                            ])
                        ])
                    ]),
                    OrderedDict([
                        ('folder', True),
                        ('name', u'test_A1'),
                        ('permission', '0775'),
                        ('children', [])
                    ])
                ]),
                ('name', u'@+test_A+@'),
                ('permission', '0775')
            ]),
            OrderedDict([
                ('folder', True),
                ('children', [
                    OrderedDict([
                        ('folder', True),
                        ('name', u'@test_C@'),
                        ('permission', '0775'),
                        ('children', [])
                    ]),
                    OrderedDict([
                        ('folder', True),
                        ('name', u'test_B1'),
                        ('permission', '0775'),
                        ('children', [])
                    ]),
                    OrderedDict([
                        ('folder', True),
                        ('name', u'test_B2'),
                        ('permission', '0775'),
                        ('children', [])
                    ])
                ]),
                ('name', u'@+test_B+@'),
                ('permission', '0775')
            ]),
            OrderedDict([
                ('folder', True),
                ('children', [
                    OrderedDict([
                        ('folder', True),
                        ('name', u'test_C1'),
                        ('permission', '0775'),
                        ('children', [
                            OrderedDict([
                                ('folder', True),
                                ('name', u'@test_D@'),
                                ('permission', '0775'),
                                ('children', [])
                            ])
                        ])
                    ])
                ]),
                ('name', u'@test_C@'),
                ('permission', '0775')
            ]),
            OrderedDict([
                ('folder', True),
                ('children', [
                    OrderedDict([
                        ('folder', True),
                        ('name', u'test_D1'),
                        ('permission', '0775'),
                        ('children', [])
                    ]),
                    OrderedDict([
                        ('folder', False),
                        ('name', u'file_D.txt'),
                        ('permission', '0775'),
                        ('content', '')
                        ])
                ]),
                ('name', u'@test_D@'),
                ('permission', '0775')
            ]),
            OrderedDict([
                ('folder', True),
                ('children', [
                    OrderedDict([
                        ('folder', True),
                        ('name', u'@test_D@'),
                        ('permission', '0775'),
                        ('children', [])
                    ])
                ]),
                ('name', u'pfx_@+test_E+@_sfx'),
                ('permission', '0775')
            ]),
            OrderedDict([
                ('folder', True),
                ('children', [
                    OrderedDict([
                        ('folder', True),
                        ('name', u'pfx_@+test_E+@_sfx'),
                        ('permission', '0755'),
                        ('children', [])
                    ])
                ]),
                ('name', u'@+test_F+@'),
                ('permission', '0755')
            ])
        ]
        self.assertEqual(register, expected_result)

    def test_resolve_template(self):
        '''Resolve the registered template.
        '''
        manager = TemplateManager(self.config_mode)
        expected_result = OrderedDict([
            ('folder', True),
            ('children', [
                OrderedDict([
                    ('folder', True),
                    ('children', [
                        OrderedDict([
                            ('folder', True),
                            ('children', [
                                OrderedDict([
                                    ('folder', True),
                                    ('name', u'test_C1'),
                                    ('permission', '0775'),
                                    ('children', [
                                        OrderedDict([
                                            ('folder', True),
                                            ('children', [
                                                OrderedDict([
                                                    ('folder', True),
                                                    ('name', u'test_D1'),
                                                    ('permission', '0775'),
                                                    ('children', [])
                                                ]),
                                                OrderedDict([
                                                    ('folder', False),
                                                    ('name', u'file_D.txt'),
                                                    ('permission', '0775'),
                                                    ('content', '')])
                                                ]),
                                            ('name', u'@test_D@'),
                                            ('permission', '0775')
                                        ])
                                    ])
                                ])
                            ]),
                            ('name', u'@test_C@'),
                            ('permission', '0775')
                        ]),
                        OrderedDict([
                            ('folder', True),
                            ('name', u'test_B1'),
                            ('permission', '0775'),
                            ('children', [])
                        ]),
                        OrderedDict([
                            ('folder', True),
                            ('name', u'test_B2'),
                            ('permission', '0775'),
                            ('children', [])]),
                        OrderedDict([
                            ('folder', False),
                            ('name', u'file_B.txt'),
                            ('permission', '0775'),
                            ('content', 'test')
                        ])
                    ]),
                    ('name', u'@+test_B+@'),
                    ('permission', '0775')
                ]),
                OrderedDict([
                    ('folder', True),
                    ('name', u'test_A1'),
                    ('permission', '0775'),
                    ('children', [])
                ])
            ]),
            ('name', u'@+test_A+@'),
            ('permission', '0775')
        ])

        result = manager.resolve_template('@+test_A+@')
        self.assertEqual(result, expected_result)

    def test_resolve_path(self):
        manager = TemplateManager(self.config_mode)
        expected_result = [
            OrderedDict([
                ('content', ''),
                ('path', [u'+test_A+']),
                ('folder', True),
                ('permission', '0775')
            ]),
            OrderedDict([
                ('content', ''),
                ('path', [u'+test_A+', u'test_A1']),
                ('folder', True),
                ('permission', '0775')
            ]),
            OrderedDict([
                ('content', ''),
                ('path', [u'+test_A+', u'+test_B+']),
                ('folder', True),
                ('permission', '0775')
            ]),
            OrderedDict([
                ('content', 'test'),
                ('path', [u'+test_A+', u'+test_B+', u'file_B.txt']),
                ('folder', False),
                ('permission', '0775')
            ]),
            OrderedDict([
                ('content', ''),
                ('path', [u'+test_A+', u'+test_B+', u'test_B2']),
                ('folder', True),
                ('permission', '0775')
            ]),
            OrderedDict([
                ('content', ''),
                ('path', [u'+test_A+', u'+test_B+', u'test_B1']),
                ('folder', True),
                ('permission', '0775')
            ]),
            OrderedDict([
                ('content', ''),
                ('path', [u'+test_A+', u'+test_B+', u'test_C']),
                ('folder', True),
                ('permission', '0775')
            ]),
            OrderedDict([
                ('content', ''),
                ('path', [u'+test_A+', u'+test_B+', u'test_C', u'test_C1']),
                ('folder', True),
                ('permission', '0775')
            ]),
            OrderedDict([
                ('content', ''),
                ('path', [
                    u'+test_A+',
                    u'+test_B+',
                    u'test_C',
                    u'test_C1',
                    u'test_D']),
                ('folder', True),
                ('permission', '0775')
            ]),
            OrderedDict([
                ('content', ''),
                ('path', [
                    u'+test_A+',
                    u'+test_B+',
                    u'test_C',
                    u'test_C1',
                    u'test_D',
                    u'file_D.txt']),
                ('folder', False),
                ('permission', '0775')
            ]),
            OrderedDict([
                ('content', ''),
                ('path', [
                    u'+test_A+',
                    u'+test_B+',
                    u'test_C',
                    u'test_C1',
                    u'test_D',
                    u'test_D1']),
                ('folder', True),
                ('permission', '0775')
            ])
        ]
        result = manager.resolve_template('@+test_A+@')
        resolved = manager.resolve(result)
        self.assertEqual(resolved, expected_result)
