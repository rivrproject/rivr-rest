import json


HTML_TEMPLATE = """
<h1>Resource</h1>

<h2>Attributes</h2>
<pre>
<code>
{attributes}
</code>
</pre>

<h2>Links</h2>
<ul>
{links}
</ul>
"""

def deserialize_html(resource):
    def render(accumulator, link):
        return accumulator + '<li><a href="{0}">{0}</a></li>\n'.format(link)

    def render_links(accumulator, relation):
        resource = relation[1]

        if isinstance(resource, list):
            get_uri = lambda resource: resource.get_uri()
            links = reduce(render, map(get_uri, resource), '')
            return accumulator + '<li>{} <ul>{}</ul></li>'.format(relation[0], links)

        return accumulator + '<li><a href="{}">{}</a></li>\n'.format(resource.get_uri(), relation[0])

    return HTML_TEMPLATE.format(
        attributes=json.dumps(resource.get_attributes(), sort_keys=True, indent=4),
        links=reduce(render_links, resource.get_relations().items(), ''),
    )

