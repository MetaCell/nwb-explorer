import uuid

from traitlets import Bool
from tornado import gen

from jupyterhub.auth import Authenticator
from jupyterhub.handlers import BaseHandler
from jupyterhub.utils import url_path_join


class TmpAuthenticateHandler(BaseHandler):
    def initialize(self, force_new_server, process_user):
        super().initialize()
        self.force_new_server = force_new_server
        self.process_user = process_user

    @gen.coroutine
    def get(self):

        username = str(uuid.uuid4())
        raw_user = self.user_from_username(username)
        self.set_login_cookie(raw_user)
        user = yield gen.maybe_future(self.process_user(raw_user, self))
        
        if 'hub/nwbfile=' in self.request.uri:
            user.spawners[''].environment["NWBFILE"] = self.request.uri.split('=')[-1]

        self.redirect(self.get_next_url(user))


class TmpAuthenticator(Authenticator):
    auto_login = True
    login_service = 'tmp'

    force_new_server = Bool(
        False,
        help="""
        Stop the user's server and start a new one when visiting /hub/tmplogin
        When set to True, users going to /hub/tmplogin will *always* get a
        new single-user server. When set to False, they'll be
        redirected to their current session if one exists.
        """,
        config=True
    )

    def process_user(self, user, handler):
        return user

    def get_handlers(self, app):
        # FIXME: How to do this better?
        extra_settings = {
            'force_new_server': self.force_new_server,
            'process_user': self.process_user
        }
        return [
            ('/tmplogin.*', TmpAuthenticateHandler, extra_settings),
            ('/nwbfile=.*', TmpAuthenticateHandler, extra_settings)
        ]

    def login_url(self, base_url):
        return url_path_join(base_url, 'tmplogin')
