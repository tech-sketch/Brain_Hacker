from handlers.auth_handler import LoginHandler, LogoutHandler, SignupHandler
from handlers.index_handler import IndexHandler
from handlers.user_handler import UsersHandler, UserHandler
from handlers.group_handler import GroupsHandler, GroupHandler, GroupUserHandler, GroupEditHandler, SearchNewMembersHandler
from handlers.room_handler import RoomsHandler, RoomHandler, RoomEditHandler, RoomDeleteHandler, RoomSocketHandler

from tornado.web import url

url_patterns = (
    url(r'/', IndexHandler, name='index'),

    url(r'/auth/login/', LoginHandler, name='login'),
    url(r'/auth/logout/', LogoutHandler, name='logout'),
    url(r'/auth/signup/', SignupHandler, name='signup'),

    url(r'/users/', UsersHandler, name='users'),
    url(r'/users/([0-9]+)/', UserHandler, name='user'),

    url(r'/groups/', GroupsHandler, name='groups'),
    url(r'/groups/([0-9]+)/', GroupHandler, name='group'),
    url(r'/groups/([0-9]+)/edit', GroupEditHandler, name='group_edit'),
    url(r'/groups/([0-9]+)/members/', GroupUserHandler, name='group_user'),
    url(r'/groups/([0-9]+)/search_new_members/', SearchNewMembersHandler, name='search_new_members'),

    url(r'/groups/([0-9]+)/rooms/', RoomsHandler, name='rooms'),
    url(r'/groups/([0-9]+)/rooms/([0-9]+)/', RoomHandler, name='room'),
    url(r'/groups/([0-9]+)/rooms/([0-9]+)/edit', RoomEditHandler, name='room_edit'),
    url(r'/groups/([0-9]+)/rooms/([0-9]+)/delete', RoomDeleteHandler, name='room_delete'),
    #url(r'/groups/([0-9]+)/rooms/([0-9]+)/socket', RoomSocketHandler, name='room_socket'),
    url(r'/websocket', RoomSocketHandler, name='room_socket'),
)