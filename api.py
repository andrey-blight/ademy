from flask_restful import Api
from Resources.UserListResource import UserListResource
from Resources.UserResource import UserResource


class MainAPI:
    def __init__(self, application):
        self.api = Api(application)
        self.api.prefix = '/api/v1'
        self._resources()

    def _resources(self):
        self.api.add_resource(UserResource, '/user/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
        self.api.add_resource(UserListResource, '/users', methods=['GET', 'POST'])
