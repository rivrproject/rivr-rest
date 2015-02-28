from rivr_rest.deserialization.utils import relations


def deserialize_json(resource):
    if isinstance(resource, (list, tuple)):
        return map(deserialize_json, resource)

    document = resource.get_attributes()

    if 'url' not in document:
        document['url'] = resource.get_uri()

    embedded, links = relations(resource)

    embed = lambda relation: (relation[0], deserialize_json(relation[1]))
    document.update(dict(map(embed, embedded)))

    link = lambda relation: (relation[0] + '_url', relation[1].get_uri())
    document.update(dict(map(link, links)))

    return document

