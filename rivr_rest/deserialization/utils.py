def partition(function, iterable):
    trues = []
    falses = []

    for item in iterable:
        if function(item):
            trues.append(item)
        else:
            falses.append(item)

    return (trues, falses)


def relations(resource):
    return partition(lambda relation: resource.can_embed(relation[0]),
                     resource.get_relations().items())


