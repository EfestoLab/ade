import os
import unittest
from manager.filesystem import FileSystemManager
from manager.template import TemplateManager


class Test_FilesystemManager(unittest.TestCase):

    def setUp(self):
        # Create a new template manager pointing to the test templates folder
        template_paths = os.path.realpath('unit_test/data/templates')
        self.template_manager = TemplateManager(template_paths)

    def test_create_manager(self):
    	filesystem_manager = FileSystemManager(self.template_manager)
    	print filesystem_manager
