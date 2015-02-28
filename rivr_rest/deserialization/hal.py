from rivr_rest.deserialization.utils import relations


def deserialize_hal(resource):
    if isinstance(resource, (list, tuple)):
        return map(deserialize_hal, resource)

    embedded, links = relations(resource)
    embed = lambda relation: (relation[0], deserialize_hal(relation[1]))

    link = lambda relation: (relation[0], {'href':relation[1].get_uri()})
    links = dict(map(link, links))
    links['self'] = { 'href': resource.get_uri() }

    document = resource.get_attributes()
    document['_links'] = links
    if len(embedded) > 0:
        document['_embedded'] = dict(map(embed, embedded))

    return document

