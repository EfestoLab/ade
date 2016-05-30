import os
import unittest
import tempfile
import logging
import copy

from ade.manager.template import TemplateManager
from ade.manager.config import ConfigManager

logging.getLogger(__name__)

class Test_TemplateManagerFindPath(unittest.TestCase):

    def setUp(self):
        """
        Setup test session.
        """
        self.maxDiff = None
        config = 'test/resources/config'
        os.environ['ADE_CONFIG_PATH'] = config
        config_manager = ConfigManager(config)
        config_mode = config_manager.get('test')
        config_mode['project_mount_point'] = tempfile.mkdtemp()
        self.config_mode = config_mode
        self.template_name = "@+test_A+@"

    def test_path_find_all(self):
        template_manager = TemplateManager(self.config_mode)
        result = template_manager.find_path(
            startwith=None, 
            contains=None, 
            endswith=None,
            template_name=self.template_name)

        expexted_result = ['+test_A+']
        
        self.assertEqual(result, expexted_result)

    def test_path_find_startswith(self):
        template_manager = TemplateManager(self.config_mode)
        result = template_manager.find_path(
            startwith='test_A', 
            contains=None, 
            endswith=None,
            template_name=self.template_name)

        expexted_result = ['+test_A+']
        
        self.assertEqual(result, expexted_result)


    def test_path_find_contains(self):
        template_manager = TemplateManager(self.config_mode)
        result = template_manager.find_path(
            startwith=None, 
            contains=['test_D1'], 
            endswith=None,
            template_name=self.template_name)

        expexted_result = [
            '+test_A+', 
            '+test_B+', 
            'test_C', 
            'test_C1', 
            'test_D', 
            'test_D1'
        ] 
        
        self.assertEqual(result, expexted_result)

    def test_path_find_endswith(self):
        template_manager = TemplateManager(self.config_mode)
        result = template_manager.find_path(
            startwith=None, 
            contains=None, 
            endswith='test_D1',
            template_name=self.template_name)

        expexted_result = [
            '+test_A+', 
            '+test_B+', 
            'test_C', 
            'test_C1', 
            'test_D', 
            'test_D1'
        ] 
        
        self.assertEqual(result, expexted_result)

    def test_path_non_existing_startswith(self):
        template_manager = TemplateManager(self.config_mode)
        result = template_manager.find_path(
            startwith='foobar', 
            contains=None, 
            endswith=None,
            template_name=self.template_name)

        expexted_result = None
        self.assertEqual(result, expexted_result)

    def test_path_non_existing_contains(self):
        template_manager = TemplateManager(self.config_mode)
        result = template_manager.find_path(
            startwith=None, 
            contains=['test_C1', 'foobar'], 
            endswith=None,
            template_name=self.template_name)

        expexted_result = None
        
        self.assertEqual(result, expexted_result)

    def test_path_non_existing_endswith(self):
        template_manager = TemplateManager(self.config_mode)
        result = template_manager.find_path(
            startwith=None, 
            contains=None, 
            endswith='foobar',
            template_name=self.template_name)

        expexted_result = None
        
        self.assertEqual(result, expexted_result)

    def test_path_non_existing_template_name(self):
        template_manager = TemplateManager(self.config_mode)
        with self.assertRaises(KeyError):
            template_manager.find_path(
                startwith='test_A', 
                contains=['test_D1'], 
                endswith=None,
                template_name='foobar')

    def test_path_contains_and_endswith(self):
        template_manager = TemplateManager(self.config_mode)
        result = template_manager.find_path(
            startwith=None, 
            contains=['test_B'], 
            endswith='test_D1',
            template_name=self.template_name)

        expexted_result = [
            '+test_A+', 
            '+test_B+', 
            'test_C', 
            'test_C1', 
            'test_D', 
            'test_D1'
        ] 
        
        self.assertEqual(result, expexted_result)

    def test_path_startswith_and_endwith(self):
        template_manager = TemplateManager(self.config_mode)
        result = template_manager.find_path(
            startwith='test_A', 
            contains=None, 
            endswith='test_D1',
            template_name=self.template_name)

        expexted_result = [
            '+test_A+', 
            '+test_B+', 
            'test_C', 
            'test_C1', 
            'test_D', 
            'test_D1'
        ] 
        
        self.assertEqual(result, expexted_result)

    def test_path_startswith_and_contains(self):
        template_manager = TemplateManager(self.config_mode)
        result = template_manager.find_path(
            startwith='test_A', 
            contains=['test_D1'], 
            endswith=None,
            template_name=self.template_name)

        expexted_result = [
            '+test_A+', 
            '+test_B+', 
            'test_C', 
            'test_C1', 
            'test_D', 
            'test_D1'
        ]
        
        self.assertEqual(result, expexted_result)

    def test_path_all_existing(self):
        template_manager = TemplateManager(self.config_mode)
        result = template_manager.find_path(
            startwith='test_A', 
            contains=['test_D'], 
            endswith='test_D1.txt',
            template_name=self.template_name)

        expexted_result = [
            '+test_A+', 
            '+test_B+', 
            'test_C', 
            'test_C1', 
            'test_D', 
            'test_D1.txt'
        ]
        
        self.assertEqual(result, expexted_result)

    def test_path_prefixes(self):
        template_manager = TemplateManager(self.config_mode)
        result = template_manager.find_path(
            startwith=None, 
            contains=['pfx_'], 
            endswith=None,
            template_name='@+test_F+@')

        expexted_result = [
            '+test_F+', 
            'pfx_+test_E+_sfx'
        ]

        self.assertEqual(result, expexted_result)

    def test_path_short(self):
        ''' 
        By default it would get +test_R+/+test_Z+/TEST1/+shot+/+shot_task+,
        we do not want this one, we want the one ending with +shot+!
        '''
        template_manager = TemplateManager(self.config_mode)
        result = template_manager.find_path(
            startwith=None, 
            contains=None, 
            endswith='shot',
            template_name='@+test_R+@')

        expexted_result = [
            '+test_R+', 
            '+test_Z+', 
            'TEST1', 
            '+shot+'
        ]

        self.assertEqual(result, expexted_result)


class Test_TemplateManager(unittest.TestCase):

    def setUp(self):
        """
        Setup test session.or
        """
        self.maxDiff = None
        config = 'test/resources/config'
        os.environ['ADE_CONFIG_PATH'] = config
        config_manager = ConfigManager(config)
        config_mode = config_manager.get('test')
        config_mode['project_mount_point'] = tempfile.mkdtemp()
        self.config_mode = config_mode

    def test_register_unexisting_template(self):
        '''
        Check when template doesn't exist
        '''
        manager = TemplateManager(self.config_mode)
        self.assertRaises(KeyError, manager._get_in_register, '@+test_fake+@')

    def test_registered_templates_is_folder(self):
        '''
        Check for template folder attributes.
        '''
        manager = TemplateManager(self.config_mode)
        folder_A = manager._get_in_register('@+test_A+@')
        self.assertTrue(folder_A.get('folder', False))
        self.assertTrue(folder_A.get('children', False))

    def test_registered_templates_is_file(self):
        '''Check for template file attributes.
        '''
        manager = TemplateManager(self.config_mode)
        file_D = manager._get_in_register('@test_D@')['children'][-1]
        self.assertFalse(file_D.get('folder'))
        self.assertFalse(file_D.get('children'))

    def test_registered_templates(self):
        ''' Register a new template through the config file.
        '''
        manager = TemplateManager(self.config_mode)
        register = manager.register

        expected = [
            dict([
                ('folder', True),
                ('children', [
                    dict([
                        ('folder', True),
                        ('name', u'@test_D@'),
                        ('permission', '0775'),
                        ('children', [])
                    ])
                ]),
                ('name', u'pfx_@+test_E+@_sfx'),
                ('permission', '0775')
            ]),
            dict([
                ('folder', True),
                ('children', []),
                ('name', u'@Publish@'),
                ('permission', '0775')
            ]),
            dict([
                ('folder', True),
                ('children', [
                    dict([
                        ('folder', True),
                        ('name', u'@+shot_task+@'),
                        ('permission', '0775'),
                        ('children', [])
                    ])
                ]),
                ('name', u'@+shot+@'),
                ('permission', '0775')
            ]),
            dict([
                ('folder', True),
                ('children', [
                    dict([
                        ('folder', True),
                        ('name', u'@Publish@'),
                        ('permission', '0775'),
                        ('children', [])
                    ]),
                    dict([
                        ('folder', True),
                        ('name', u'@Work@'),
                        ('permission', '0775'),
                        ('children', [])
                    ])
                ]),
                ('name', u'@+shot_task+@'),
                ('permission', '0775')
            ]),
            dict([
                ('folder', True),
                ('children', [
                    dict([
                        ('folder', True),
                        ('name', u'@+shot+@'),
                        ('permission', '0775'),
                        ('children', [])
                    ])
                ]),
                ('name', u'@TEST1@'),
                ('permission', '0775')
            ]),
            dict([
                ('folder', True),
                ('children', []),
                ('name', u'@TEST2@'),
                ('permission', '0775')
            ]),
            dict([
                ('folder', True),
                ('children', [
                    dict([
                        ('folder', True),
                        ('name', u'test_A1'),
                        ('permission', '0775'),
                        ('children', [])
                    ]),
                    dict([
                        ('folder', True),
                        ('name', u'@+test_B+@'),
                        ('permission', '0775'),
                        ('children', [
                            dict([
                                ('folder', False),
                                ('name', u'file_B.txt'),
                                ('permission', '0775'),
                                ('content', 'test')
                            ])
                        ])
                    ])
                ]),
                ('name', u'@+test_A+@'),
                ('permission', '0775')
            ]),
            dict([
                ('folder', True),
                ('children', [
                    dict([
                        ('folder', True),
                        ('name', u'test_B1'),
                        ('permission', '0775'),
                        ('children', [])
                    ]),
                    dict([
                        ('folder', True),
                        ('name', u'test_B2'),
                        ('permission', '0775'),
                        ('children', [])
                    ]),
                    dict([
                        ('folder', True),
                        ('name', u'@test_C@'),
                        ('permission', '0775'),
                        ('children', [])
                    ])
                ]),
                ('name', u'@+test_B+@'),
                ('permission', '0775')
            ]),
            dict([
                ('folder', True),
                ('children', [
                    dict([
                        ('folder', True),
                        ('name', u'test_C1'),
                        ('permission', '0775'),
                        ('children', [
                            dict([
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
            dict([
                ('folder', True),
                ('children', [
                    dict([
                        ('folder', True),
                        ('name', u'test_D1'),
                        ('permission', '0775'),
                        ('children', [])
                    ]),
                    dict([
                        ('folder', False),
                        ('name', u'test_D1.txt'),
                        ('permission', '0664'),
                        ('content', '')
                    ])
                ]),
                ('name', u'@test_D@'),
                ('permission', '0775')
            ]),
            dict([
                ('folder', True),
                ('children', [
                    dict([
                        ('folder', True),
                        ('name', u'pfx_@+test_E+@_sfx'),
                        ('permission', '0775'),
                        ('children', [])
                    ])
                ]),
                ('name', u'@+test_F+@'),
                ('permission', '0775')
            ]),
            dict([
                ('folder', True),
                ('children', [
                    dict([
                        ('folder', True),
                        ('name', u'@+test_Z+@'),
                        ('permission', '0775'),
                        ('children', [])
                    ])
                ]),
                ('name', u'@+test_R+@'),
                ('permission', '0775')
            ]),
            dict([
                ('folder', True),
                ('children', [
                    dict([
                        ('folder', True),
                        ('name', u'@TEST1@'),
                        ('permission', '0775'),
                        ('children', [])
                    ]),
                    dict([
                        ('folder', True),
                        ('name', u'@TEST2@'),
                        ('permission', '0775'),
                        ('children', [
                            dict([
                                ('folder', False),
                                ('name', u'gitignore'),
                                ('permission', '0664'),
                                ('content', '')
                            ])
                        ])
                    ])
                ]),
                ('name', u'@+test_Z+@'),
                ('permission', '0775')]),
            dict([
                ('folder', True),
                ('children', []),
                ('name', u'@Work@'),
                ('permission', '0775')
            ])
        ]

        self.assertEqual(register, expected)

    def test_resolve_template(self):
        '''Resolve the registered template.
        '''
        manager = TemplateManager(self.config_mode)
        result = manager.resolve_template('@+test_A+@')

        expected = dict([
            ('folder', True),
            ('children', [
                dict([
                    ('folder', True),
                    ('name', u'test_A1'),
                    ('permission', '0775'),
                    ('children', [])
                ]),
                dict([
                    ('folder', True),
                    ('children', [
                        dict([
                            ('folder', True),
                            ('name', u'test_B1'),
                            ('permission', '0775'),
                            ('children', [])
                        ]),
                        dict([
                            ('folder', True),
                            ('name', u'test_B2'),
                            ('permission', '0775'),
                            ('children', [])
                        ]),
                        dict([
                            ('folder', True),
                            ('children', [
                                dict([
                                    ('folder', True),
                                    ('name', u'test_C1'),
                                    ('permission', '0775'),
                                    ('children', [
                                        dict([
                                            ('folder', True),
                                            ('children', [
                                                dict([
                                                    ('folder', True),
                                                    ('name', u'test_D1'),
                                                    ('permission', '0775'),
                                                    ('children', [])
                                                ]),
                                                dict([
                                                    ('folder', False),
                                                    ('name', u'test_D1.txt'),
                                                    ('permission', '0664'),
                                                    ('content', '')
                                                ])
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
                        dict([
                            ('folder', False),
                            ('name', u'file_B.txt'),
                            ('permission', '0775'),
                            ('content', 'test')
                        ])
                    ]),
                    ('name', u'@+test_B+@'),
                    ('permission', '0775')
                ])
            ]),
            ('name', u'@+test_A+@'),
            ('permission', '0775')
        ])
        
        self.assertEqual(result, expected)

    def test_resolve_path(self):
        manager = TemplateManager(self.config_mode)
        result = manager.resolve_template('@+test_A+@')
        resolved = manager.resolve(result)
        expected_result = [
            dict([
                ('content', ''),
                ('path', [
                    u'+test_A+'
                ]),
                ('folder', True),
                ('permission', '0775')
            ]),
            dict([
                ('content', ''),
                ('path', [
                    u'+test_A+',
                    u'test_A1'
                ]),
                ('folder', True),
                ('permission', '0775')
            ]),
            dict([
                ('content', ''),
                ('path', [
                    u'+test_A+',
                    u'+test_B+'
                ]),
                ('folder', True),
                ('permission', '0775')
            ]),
            dict([
                ('content', ''),
                ('path', [
                    u'+test_A+',
                    u'+test_B+',
                    u'test_B1'
                ]),
                ('folder', True),
                ('permission', '0775')
            ]),
            dict([
                ('content', ''),
                ('path', [
                    u'+test_A+',
                    u'+test_B+',
                    u'test_B2'
                ]),
                ('folder', True),
                ('permission', '0775')
            ]),
            dict([
                ('content', ''),
                ('path', [
                    u'+test_A+',
                    u'+test_B+',
                    u'test_C'
                ]),
                ('folder', True),
                ('permission', '0775')
            ]),
            dict([
                ('content', ''),
                ('path', [
                    u'+test_A+',
                    u'+test_B+',
                    u'test_C',
                    u'test_C1'
                ]),
                ('folder', True),
                ('permission', '0775')
            ]),
            dict([
                ('content', ''),
                ('path', [
                    u'+test_A+',
                    u'+test_B+',
                    u'test_C',
                    u'test_C1',
                    u'test_D'
                ]),
                ('folder', True),
                ('permission', '0775')
            ]),
            dict([
                ('content', ''),
                ('path', [
                    u'+test_A+',
                    u'+test_B+',
                    u'test_C',
                    u'test_C1',
                    u'test_D',
                    u'test_D1'
                ]),
                ('folder', True),
                ('permission', '0775')
            ]),
            dict([
                ('content', ''),
                ('path', [
                    u'+test_A+',
                    u'+test_B+',
                    u'test_C',
                    u'test_C1',
                    u'test_D',
                    u'test_D1.txt'
                ]),
                ('folder', False),
                ('permission', '0664')
            ]),
            dict([
                ('content', 'test'),
                ('path', [
                    u'+test_A+',
                    u'+test_B+',
                    u'file_B.txt'
                ]),
                ('folder', False),
                ('permission', '0775')
            ])
        ]
        self.assertEqual(resolved, expected_result)
