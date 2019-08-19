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

        raw_user = yield self.get_current_user()

        if raw_user:
            if self.force_new_server and raw_user.running:
                status = yield raw_user.spawner.poll_and_notify()
                if status is None:
                    yield self.stop_single_user(raw_user)
            
        else:
            username = str(uuid.uuid4())
            raw_user = self.user_from_username(username)
            self.set_login_cookie(raw_user)

        user = yield gen.maybe_future(self.process_user(raw_user, self))
        
        server_name = ''
        redirection = self.get_next_url(user)
        user.spawners[server_name].environment["NWBFILE"] = ''

        if 'hub/nwbfile=' in self.request.uri:
            server_name = str(uuid.uuid4()).split('-').pop()
            redirection = f'/hub/spawn/{user.name}/{server_name}'
            url = self.request.uri.split('=').pop()
            user.spawners[server_name].environment["NWBFILE"] = url
            self._set_cookie("nwbloadurl", bytes(url, 'utf-8'), encrypted=False, httponly=False)
        
        self.redirect(redirection)


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