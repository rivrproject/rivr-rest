from rivr import serve
from rivr_rest import Resource, Router


class UsersResource(Resource):
    uri_template = '/users'

    def get_relations(self):
        return {
            'users': [
                UserResource(parameters={'username': 'kyle'}),
                UserResource(parameters={'username': 'katie'}),
            ]
        }

class UserResource(Resource):
    uri_template = '/users/{username}'

    def get_attributes(self):
        return {
            'username': self.parameters['username'],
        }

router = Router(
    UsersResource,
    UserResource,
)

router.add_root_resource('users', UsersResource)

if __name__ == '__main__':
    serve(router)

