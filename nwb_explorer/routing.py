from channels.routing import include

channel_routing = [
    include('pygeppetto_server.routing.server_routing', path=r"^/org.geppetto.frontend/Geppetto"),
]