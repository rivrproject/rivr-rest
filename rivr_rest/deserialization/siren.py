from functools import reduce
from rivr_rest.deserialization.utils import relations


def flatten(accumulator, item):
    if isinstance(item, list):
        return accumulator + item
    return accumulator + [item]


def deserialize_siren(resource, rel=None):
    if isinstance(resource, (list, tuple)):
        return list(map(lambda r: deserialize_siren(r, rel), resource))

    embedded, links = relations(resource)

    link = lambda relation: { 'rel': [ relation[0] ], 'href': relation[1].get_uri() }
    links = list(map(link, links)) + [
        { 'rel': [ 'self' ], 'href': resource.get_uri() }
    ]

    document = {
        'properties': resource.get_attributes(),
        'links': links,
    }

    entities = reduce(flatten,
                      map(lambda e: deserialize_siren(e[1], e[0]), embedded), [])
    if len(entities) > 0:
        document['entities'] = entities

    if rel:
        document['rel'] = [rel]

    return document

