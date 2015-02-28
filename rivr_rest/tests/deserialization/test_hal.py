import unittest
from rivr_rest.deserialization.hal import deserialize_hal
from resources import EmbeddedResource, TestResource


class HALDeserializationTests(unittest.TestCase):
    def setUp(self):
        self.resource = TestResource()

    def test_includes_attributes(self):
        document = deserialize_hal(self.resource)
        self.assertEqual(document['test'], 'value')

    def test_adds_link_for_self_to_document(self):
        document = deserialize_hal(self.resource)
        self.assertEqual(document['_links']['self'], {'href':'/test'})

    def test_links_resource(self):
        document = deserialize_hal(self.resource)
        self.assertEqual(document['_links']['link'], {'href':'/embed'})

    def test_embeds_resource(self):
        document = deserialize_hal(self.resource)
        self.assertEqual(document['_embedded']['embed'], {
            '_links': {'self': {'href': '/embed'}},
            'name': 'Embedded'
        })

    def test_embeds_collection_resource(self):
        document = deserialize_hal(self.resource)
        self.assertEqual(document['_embedded']['collection'], [
            {
                '_links': {'self': {'href': '/embed'}},
                'name': 'Embedded'
            }, {
                '_links': {'self': {'href': '/embed'}},
                'name': 'Embedded',
            }
        ])
