import unittest

from manager.template import TemplateManager


class Test_TemplateManager(unittest.TestCase):

    def setUp(self):
        self.manager = TemplateManager()

    def test_register(self):
        assert self.manager.register


if __name__ == '__main__':
    unittest.main()

    # M = TemplateManager()
    # schema = '@+show+@'
    # print pformat(M._register)
    # resolved_template = M.resolve_template(schema)
    # resolved = M.resolve(resolved_template)

    # print pformat(resolved_template)
    # print pformat(resolved)

    # print 'PARSERs:'
    # pareser_results = M.to_parser(schema)
    # print pformat(pareser_results)

    # context = {
    # 	'show': 'white',
    # 	'department': 'show',
    # 	'sequence': 'AA',
    # 	'shot': 'AA000',
    # 	'user': 'ennio',
    # 	'python_version': '2.6.4'
    # }

    # path_results = M.to_path(schema, context)
    # print pformat(path_results)

    # build = M.build(schema, context)
    # path = path_results[11]
    # print 'TEST PARSE:', path

    # results = M.parse(path, schema)
    # print pformat(results)
