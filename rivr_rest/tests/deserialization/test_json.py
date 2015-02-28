import unittest
from rivr_rest.deserialization.json import deserialize_json
from resources import EmbeddedResource, TestResource


class JSONDeserializationTests(unittest.TestCase):
    def setUp(self):
        self.resource = TestResource()

    def test_includes_attributes(self):
        document = deserialize_json(self.resource)
        self.assertEqual(document['test'], 'value')

    def test_adds_url_for_self_to_document(self):
        document = deserialize_json(self.resource)
        self.assertEqual(document['url'], '/test')

    def test_embeds_resource(self):
        document = deserialize_json(self.resource)
        self.assertEqual(document['embed'], {
            'url': '/embed',
            'name': 'Embedded',
        })

    def test_embeds_collection_resource(self):
        document = deserialize_json(self.resource)
        self.assertEqual(document['collection'], [
            {
                'url': '/embed',
                'name': 'Embedded',
            }, {
                'url': '/embed',
                'name': 'Embedded',
            }
        ])

    def test_links_resource(self):
        document = deserialize_json(self.resource)
        self.assertEqual(document['link_url'], '/embed')
