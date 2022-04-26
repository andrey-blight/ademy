from Resources.UserResources.UserListResource import UserListResource
from Resources.UserResources.UserResource import UserResource
from Resources.UserResources.UserRecommendResource import UserRecommendResource
from Resources.UserResources.UsersChatsResource import UsersChatsResource
from Resources.ImageResources.ImageListResource import ImageListResource
from Resources.ImageResources.ImageResource import ImageResource
from Resources.InterestResources.InterestListResource import \
    InterestListResource
from Resources.LikeResources.LikeResource import LikeResource

from flask_restful import Api


class MainAPI:
    def __init__(self, application):
        self.api = Api(application)
        self.api.prefix = r"/api/v1"
        self._resources()

    def _resources(self) -> None:
        self.api.add_resource(UserResource, r"/user/<int:user_id>",
                              methods=["GET", "PUT", "DELETE"])
        self.api.add_resource(UserListResource, r"/users",
                              methods=["GET", "POST"])
        self.api.add_resource(UserRecommendResource,
                              "/recommend_user/<int:count>/<int:sex>",
                              methods=["GET"])
        self.api.add_resource(UsersChatsResource, "/chats/<int:user_id>",
                              methods=["GET"])
        self.api.add_resource(ImageResource, r"/image/<int:image_id>",
                              methods=["GET", "PUT", "DELETE"])
        self.api.add_resource(ImageListResource, r"/images/<int:user_id>",
                              methods=["GET", "POST"])
        self.api.add_resource(InterestListResource, r"/interests",
                              methods=["GET"])
        self.api.add_resource(LikeResource, "/like/<int:from_id>/<int:to_id>",
                              methods=["POST"])

    def get_api_prefix(self):
        return self.api.prefix
