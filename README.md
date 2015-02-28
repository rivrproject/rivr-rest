# rivr-rest

[![Build Status](http://img.shields.io/travis/rivrproject/rivr-rest/master.svg?style=flat)](https://travis-ci.org/rivrproject/rivr-rest)

A library for building REST APIs with [rivr](https://github.com/rivrproject/rivr).

## Example

An example resource representing the repository for rivr.

```python
class RepositoryResource(Resource):
    uri_template = '/repositories/rivr'

    def get_attributes(self):
        return {
            'name': 'Rivr',
            'description': 'Elegant microweb framework',
        }
```

When you request this resource as JSON, it will be serialized as the following:

```javascript
{
    "name": "Rivr",
    "description": "Elegant microweb framework",
    "url": "/repositories/rivr"
}
```

It can be serialized to [JSON HAL](http://stateless.co/hal_specification.html):

```javascript
{
    "_links": {
        "self": { "href": "/repositories/rivr" }
    },
    "name": "Rivr",
    "description": "Elegant microweb framework"
}
```

We can define another resource with a relation to the repository as follows:

```python
class UserResource(Resource):
    uri_template = '/kyle'

    def get_attributes(self):
        return {
            'name': 'Kyle',
        }

    def get_relations(self):
        return {
            'repository': RepositoryResource()
        }
```

This relation will automatically be embedded in the JSON representation:

```javascript
{
    "name": "Kyle",
    "repository": {
        "name": "Rivr",
        "description": "Elegant microweb framework",
        "url": "/repositories/rivr"
    }
}
```

Along with HAL:

```javascript
{
    "name": "Kyle",
    "_embedded": {
        "repository": [
            {
                "_links": {
                    "self": { "href": "/repositories/rivr" }
                },
                "name": "Rivr",
                "description": "Elegant microweb framework"
            }
        ]
    }
}
```

You can opt-out of the automatic embedding of our resources:

```python
def can_embed(self, relation):
    return False
```

Now when we serialize the resource, the relations will instead be links:

```javascript
{
    "name": "Kyle",
    "repository_url": "/repositories/rivr"
}
```

## License

rivr-rest is released under the BSD license. See [LICENSE](LICENSE).

