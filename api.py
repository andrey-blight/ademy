from Resources.UserResources.UserListResource import UserListResource
from Resources.UserResources.UserRecommendResource import UserRecommendResource
from Resources.UserResources.UsersChatsResource import UsersChatsResource
from Resources.InterestResources.InterestListResource import InterestListResource
from Resources.LikeResources.LikeResource import LikeResource
from Resources.MessageResources.MessageListResource import MessageListResource

from flask_restful import Api


class MainAPI:
    def __init__(self, application):
        self.api = Api(application)
        self.api.prefix = r"/api/v1"
        self._resources()

    def _resources(self) -> None:
        self.api.add_resource(UserListResource, r"/users", methods=["GET", "POST"])
        self.api.add_resource(UserRecommendResource, r"/recommend_users/<int:count>/<int:sex>", methods=["GET"])
        self.api.add_resource(UsersChatsResource, r"/chats/<int:user_id>", methods=["GET"])
        self.api.add_resource(InterestListResource, r"/interests", methods=["GET"])
        self.api.add_resource(LikeResource, r"/likes/<int:from_id>/<int:to_id>", methods=["POST"])
        self.api.add_resource(MessageListResource, r"/messages/<int:chat_id>", methods=["GET", "POST"])

    def get_api_prefix(self):
        return self.api.prefix
