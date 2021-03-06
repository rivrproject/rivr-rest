import json

from uritemplate import expand
from negotiator import AcceptParameters, ContentType, ContentNegotiator

from rivr.views import View
from rivr.http import Response
from rivr_rest.deserialization import deserialize_json, deserialize_hal, deserialize_siren, deserialize_html


class Resource(View):
    uri_template = None
    parameters = None

    def __init__(self, parameters=None):
        self.parameters = parameters

    def get_uri(self):
        """
        Returns the URI for this resource, using the parameters for expansion.
        """
        parameters = self.get_parameters()
        return expand(self.uri_template, parameters)

    ###

    def get_parameters(self):
        """
        Returns the parameters used for the resource.
        """
        return self.parameters or {}

    def get_attributes(self):
        return {}

    def get_relations(self):
        """
        Returns a dictionary of relations, key must be a string and the value
        should be another resource or a list of resources.
        """
        return {}

    def can_embed(self, relation):
        """
        When this method returns `True` for a given relation, the relation will
        be embedded in any resource when applicable.

        By default, this returns True unless the relation is `self`,
        `next`, or `prev`.
        """
        return relation not in ('self', 'next', 'prev')

    ###

    preferred_content_type = 'application/json'

    def content_type_providers(self):
        """
        Returns a dictionary of content type providers, key is a string
        of the content type, i.e, `application/json` and the value is a
        function that returns a response for that type.
        """

        def json_provider(deserializer, content_type):
            def inner():
                content = json.dumps(deserializer(self))
                return Response(content, content_type='{}; charset=utf8'.format(content_type))
            return inner

        return {
            'application/json': json_provider(deserialize_json, 'application/json'),
            'application/hal+json': json_provider(deserialize_hal, 'application/hal+json'),
            'application/vnd.siren+json': json_provider(deserialize_siren, 'application/vnd.siren+json'),
            'text/html': lambda: Response(deserialize_html(self)),
        }

    def get(self, request):
        content_type_to_acceptable = lambda content_type: AcceptParameters(ContentType(content_type))
        acceptable = map(content_type_to_acceptable, self.content_type_providers().keys())
        preferred_content_type = self.preferred_content_type

        accept = request.headers.get('ACCEPT')

        negotiator = ContentNegotiator(
            content_type_to_acceptable(preferred_content_type),
            acceptable)
        negotiated_type = negotiator.negotiate(accept=accept)
        content_type = negotiated_type.content_type or preferred_content_type

        provider = self.content_type_providers()[str(content_type)]

        return provider()

