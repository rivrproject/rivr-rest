import unittest
from rivr.http import Request
from rivr_rest.resource import Resource


class TestResource(Resource):
    uri_template = '/resource/{id}'

    def get_parameters(self):
        return {
            'id': 5,
        }

    def get_relations(self):
        return {
            'next': TestResource(parameters={'id': 6})
        }


class ResourceTests(unittest.TestCase):
    def setUp(self):
        self.resource = TestResource()

    # URI

    def test_uri_template(self):
        self.assertEqual(self.resource.uri_template, '/resource/{id}')

    def test_uri_expansion(self):
        self.assertEqual(self.resource.get_uri(), '/resource/5')

    # Parameters

    def test_parameters(self):
        resource = Resource(parameters={'id': 6})
        self.assertEqual(resource.get_parameters(), {'id': 6})

    # Can Embed

    def test_cannot_embed_self(self):
        self.assertFalse(self.resource.can_embed('self'))

    def test_cannot_embed_next(self):
        self.assertFalse(self.resource.can_embed('next'))

    def test_cannot_embed_prev(self):
        self.assertFalse(self.resource.can_embed('prev'))

    def test_can_embed_arbitary_relation(self):
        self.assertTrue(self.resource.can_embed('arbitary'))

    #

    def test_content_types(self):
        self.assertEqual(self.resource.content_type_providers().keys(),
            ['application/json', 'application/hal+json'])

    def test_preferred_content_type(self):
        self.assertEqual(self.resource.preferred_content_type,
            'application/json')

    def test_get(self):
        request = Request()
        response = self.resource.get(request)

        self.assertEqual(response.headers['Content-Type'],
            'application/json; charset=utf8')

        self.assertEqual(response.content,
            '{"url": "/resource/5", "next_url": "/resource/5"}')

