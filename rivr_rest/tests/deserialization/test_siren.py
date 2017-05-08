import unittest
from rivr_rest.deserialization.siren import deserialize_siren
from .resources import EmbeddedResource, TestResource


class SirenDeserializationTests(unittest.TestCase):
    def setUp(self):
        self.resource = TestResource()
        self.document = deserialize_siren(self.resource)

    def find_link(self, name):
        find = lambda link: name in link['rel']
        return next(filter(find, self.document['links']))

    def find_entity(self, name):
        find = lambda entity: name in entity['rel']
        return list(filter(find, self.document['entities']))

    def test_includes_attributes(self):
        self.assertEqual(self.document['properties'], {'test': 'value'})

    def test_adds_link_for_self_to_document(self):
        self.assertEqual(self.find_link('self')['href'], '/test')

    def test_links_resource(self):
        self.assertEqual(self.find_link('link')['href'], '/embed')

    def test_embeds_resource(self):
        self.assertEqual(self.find_entity('embed'), [{
            'properties': {
                'name': 'Embedded',
            },
            'links': [
                { 'rel': ['self'], 'href': '/embed' }
            ],
            'rel': ['embed'],
        }])

    def test_embeds_collection_resource(self):
        self.assertEqual(self.find_entity('collection'), [
            {
                'properties': {
                    'name': 'Embedded',
                },
                'links': [
                    { 'rel': ['self'], 'href': '/embed' }
                ],
                'rel': ['collection'],
            }, {
                'properties': {
                    'name': 'Embedded',
                },
                'links': [
                    { 'rel': ['self'], 'href': '/embed' }
                ],
                'rel': ['collection'],
            }
        ])
