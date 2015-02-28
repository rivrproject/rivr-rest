from rivr_rest.resource import Resource


class EmbeddedResource(Resource):
    uri_template = '/embed'

    def get_attributes(self):
        return { 'name': 'Embedded' }

class TestResource(Resource):
    uri_template = '/test'

    def get_attributes(self):
        return { 'test': 'value' }

    def get_relations(self):
        return {
            'embed': EmbeddedResource(),
            'collection': [EmbeddedResource(), EmbeddedResource()],
            'link': EmbeddedResource(),
        }

    def can_embed(self, relation):
        return relation is not 'link'


