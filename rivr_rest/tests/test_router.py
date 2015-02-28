import unittest
from rivr_rest import Resource, Router
from rivr_rest.router import extract


class RootResource(Resource):
    uri_template = '/'


class UsersResource(Resource):
    uri_template = '/users'


class RouterTests(unittest.TestCase):
    def test_register_resource(self):
        router = Router()
        router.register(RootResource)

        self.assertEqual(len(router.resources), 1)

    def test_routing_path(self):
        router = Router(RootResource, UsersResource)
        root, root_params = router.resolve('/')
        users, users_params = router.resolve('/users')

        self.assertEqual(root, RootResource)
        self.assertEqual(users, UsersResource)
        self.assertIsNone(router.resolve('/unknown'))


class URITemplateExtractTests(unittest.TestCase):
    def test_no_variables_not_match(self):
        self.assertIsNone(extract('/pathy', '/path'))

    def test_no_variables(self):
        self.assertEqual(extract('/path', '/path'), {})

    def test_simple_variable(self):
        self.assertEqual(extract('/{name}', '/kyle'), {'name': 'kyle'})

    def test_simple_variables(self):
        self.assertEqual(extract('/{x}/{y}', '/a/bcd'), {'x': 'a', 'y': 'bcd'})


