import os
import unittest
import logging
from ade.manager.template import TemplateManager
logging.getLogger('ade')


class Test_TemplateManager(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        # Create a new template manager pointing to the test templates folder
        self.template_paths = os.path.realpath('test/resources/templates')

    def test_registered_templates(self):
        manager = TemplateManager(self.template_paths)
        register = manager.register
        expected_result = [
            {'folder': True, 'permission': '0755', 'name': '@test_C@', 'children': [
                {'folder': True, 'children': [
                    {'folder': True, 'children': [], 'name': '@test_D@', 'permission': '0755'}
                    ], 'name': 'test_C1', 'permission': '0755'}]
                },
            {'folder': True, 'permission': '0755', 'name': '@+test_A+@', 'children': [
                {'folder': True, 'children': [
                    {'content': 'test', 'folder': False, 'name': 'file_B.txt', 'permission': '0644'}
                    ], 'name': '@+test_B+@', 'permission': '0755'},
                    {'folder': True, 'children': [], 'name': 'test_A1', 'permission': '0755'}
                    ]
                },
            {'folder': True, 'permission': '0755', 'name': '@test_D@', 'children': [
                {'content': '', 'folder': False, 'name': 'file_D.txt', 'permission': '0644'},
                {'folder': True, 'children': [], 'name': 'test_D1', 'permission': '0755'}
                ]
            },
            {'folder': True, 'permission': '0755', 'name': '@+test_B+@', 'children': [
                {'folder': True, 'children': [], 'name': 'test_B1', 'permission': '0755'},
                {'folder': True, 'children': [], 'name': '@test_C@', 'permission': '0755'},
                {'folder': True, 'children': [], 'name': 'test_B2', 'permission': '0755'}
                ]
            }
        ]
        self.assertEqual(register, expected_result)

    def test_register_unexisting_template(self):
        manager = TemplateManager(self.template_paths)
        with self.assertRaises(KeyError):
            manager._get_in_register('@+test_fake+@')

    def test_registered_templates_is_folder(self):
        manager = TemplateManager(self.template_paths)
        folder_A = manager._get_in_register('@+test_A+@')
        self.assertTrue(folder_A.get('folder', False))
        self.assertTrue(folder_A.get('children', False))
        self.assertEqual(folder_A.get('permission', 000), '0755')

    def test_registered_templates_is_file(self):
        manager = TemplateManager(self.template_paths)
        file_D = manager._get_in_register('@test_D@')['children'][0]
        self.assertFalse(file_D.get('folder', True))
        self.assertFalse(file_D.get('children'))
        self.assertEqual(file_D.get('permission', 000), '0644')

    def test_resolve_template(self):
        manager = TemplateManager(self.template_paths)
        expected_result = {'folder': True, 'children': [
            {'folder': True, 'children': [
                {'folder': True, 'permission': '0755', 'children': [], 'name': 'test_B1'},
                {'folder': True, 'children': [
                    {'folder': True, 'permission': '0755', 'children': [
                        {'folder': True, 'children': [
                            {'content': '', 'folder': False, 'name': 'file_D.txt', 'permission': '0644'},
                            {'folder': True, 'permission': '0755', 'children': [], 'name': 'test_D1'}
                        ], 'name': '@test_D@', 'permission': '0755'}
                    ], 'name': 'test_C1'}
                ], 'name': '@test_C@', 'permission': '0755'},
                {'folder': True, 'permission': '0755', 'children': [], 'name': 'test_B2'},
                {'content': 'test', 'folder': False, 'name': 'file_B.txt', 'permission': '0644'}
            ], 'name': '@+test_B+@', 'permission': '0755'},
            {'folder': True, 'permission': '0755', 'children': [], 'name': 'test_A1'}
        ],
        'name': '@+test_A+@', 'permission': '0755'}

        result = manager.resolve_template('@+test_A+@')
        self.assertEqual(result, expected_result)

    def test_resolve(self):
        manager = TemplateManager(self.template_paths)
        expected_result = [
            # {'content': '', 'path': ['+test_A+'], 'folder': True, 'permission': '0755'}, consitency test for bug
            {'content': '', 'path': ['+test_A+', 'test_A1'], 'folder': True, 'permission': '0755'},
            {'content': '', 'path': ['+test_A+', '+test_B+'], 'folder': True, 'permission': '0755'},
            {'content': 'test', 'path': ['+test_A+', '+test_B+', 'file_B.txt'], 'folder': False, 'permission': '0644'},
            {'content': '', 'path': ['+test_A+', '+test_B+', 'test_B2'], 'folder': True, 'permission': '0755'},
            {'content': '', 'path': ['+test_A+', '+test_B+', 'test_C'], 'folder': True, 'permission': '0755'},
            {'content': '', 'path': ['+test_A+', '+test_B+', 'test_C', 'test_C1'], 'folder': True, 'permission': '0755'},
            {'content': '', 'path': ['+test_A+', '+test_B+', 'test_C', 'test_C1', 'test_D'], 'folder': True, 'permission': '0755'},
            {'content': '', 'path': ['+test_A+', '+test_B+', 'test_C', 'test_C1', 'test_D', 'test_D1'], 'folder': True, 'permission': '0755'},
            {'content': '', 'path': ['+test_A+', '+test_B+', 'test_C', 'test_C1', 'test_D', 'file_D.txt'], 'folder': False, 'permission': '0644'},
            {'content': '', 'path': ['+test_A+', '+test_B+', 'test_B1'], 'folder': True, 'permission': '0755'}
        ]
        result = manager.resolve_template('@+test_A+@')
        resolved = manager.resolve(result)
        self.assertEqual(resolved, expected_result)
