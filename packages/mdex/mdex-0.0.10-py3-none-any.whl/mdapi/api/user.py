from ..endpoints import Endpoints
from ..util import PaginatedRequest, _type_id
from ..schema import Type


class UserAPI:
    def __init__(self, api):
        self.api = api

    def get_list(self):
        return PaginatedRequest(self.api, Endpoints.User.LIST)

    def get_list_for(self, user):
        return PaginatedRequest(
            self.api,
            Endpoints.User.OTHER_LIST,
            urlparams={
                "user": _type_id(user)
            }
        )

    def get_self(self):
        return Type.parse_obj(self.api._make_request(Endpoints.User.GET_ME))

    def get_followed_groups(self):
        return PaginatedRequest(self.api, Endpoints.User.FOLLOWS_GROUP)

    def get_followed_chapters(self):
        return PaginatedRequest(self.api, Endpoints.User.FOLLOWS_CHAPTERS)

    def get_followed_manga(self):
        return PaginatedRequest(self.api, Endpoints.User.FOLLOWS_MANGA)
