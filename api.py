from Resources.UserResources.UserListResource import UserListResource
from Resources.UserResources.UserResource import UserResource

from flask_restful import Api


class MainAPI:
    def __init__(self, application):
        self.api = Api(application)
        self.api.prefix = r"/api/v1"
        self._resources()

    def _resources(self):
        self.api.add_resource(UserResource, r"/user/<int:user_id>", methods=["GET", "PUT", "DELETE"])
        self.api.add_resource(UserListResource, r"/users", methods=["GET", "POST"])

    def get_api_prefix(self):
        return self.api.prefix