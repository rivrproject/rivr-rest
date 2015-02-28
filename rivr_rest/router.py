import re
from rivr.http import Http404
from rivr_rest.resource import Resource


EXTRACT_VARIABLE_REGEX = re.compile(r'\{([\w]+)\}')

def extract(uri_template, uri):
    """
    Reverse URI Template implementation.

    Note, only simple variable templates are currently supported.
    """

    if uri == uri_template:
        return {}

    escaped_uri_template = re.escape(uri_template).replace('\{', '{').replace('\}', '}')

    def replace(match):
        return '(?P<{}>[\w]+)'.format(match.group(1))

    pattern = '^{}$'.format(
        re.sub(EXTRACT_VARIABLE_REGEX, replace, escaped_uri_template))

    match = re.match(pattern, uri)
    if match:
        return match.groupdict()

    return None


class RootResource(Resource):
    uri_template = '/'

    def __init__(self, resources):
        self.resources = resources

    def get_relations(self):
        def to_resource(relation):
            if isinstance(relation[1], type):
                return (relation[0], relation[1]())

            return relation

        return dict(map(to_resource, self.resources.items()))

    def can_embed(self, relation):
        return False


class Router(object):
    root_resource = RootResource

    def __init__(self, *resources):
        self.root_resources = {}
        self.resources = list(resources)

    def register(self, resource):
        self.resources.append(resource)

    def add_root_resource(self, relation, resource):
        self.root_resources[relation] = resource

    def resolve(self, path):
        for resource in self.resources:
            parameters = extract(resource.uri_template, path)
            if parameters is not None:
                return (resource, parameters)

        return None

    def __call__(self, request):
        if request.path == '/' and len(self.root_resources) > 0:
            resource = self.root_resource(resources=self.root_resources)
            return resource.dispatch(request)

        match = self.resolve(request.path)
        if not match:
            raise Http404

        resource, parameters = match

        return resource(parameters=parameters).dispatch(request)

