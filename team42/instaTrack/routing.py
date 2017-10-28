from channels.routing import route, include
from .consumers import Demultiplexer

# TODO: here we connect the conusmer methods with channels names
# something similar to URL routing

# we can rout based on the path, based on the any message attribute that is string # i.e. method=POST for http
app_routing = [
    # route("websocket.connect", ws_app_connect),
    # route("websocket.receive", ws_app_message),
    # route("websocket.connect", ws_app_disconnect)

    Demultiplexer.as_route()
]

routing = [
    include(app_routing, path=r"^/app")
]
