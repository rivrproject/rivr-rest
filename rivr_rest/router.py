import re
from rivr.http import Http404


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


class Router(object):
    def __init__(self, *resources):
        self.resources = list(resources)

    def register(self, resource):
        self.resources.append(resource)

    def resolve(self, path):
        for resource in self.resources:
            parameters = extract(resource.uri_template, path)
            if parameters is not None:
                return (resource, parameters)

        return None

    def __call__(self, request):
        match = self.resolve(request.path)
        if not match:
            raise Http404

        resource, parameters = match

        return resource(parameters=parameters).dispatch(request)

