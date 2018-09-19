from channels.routing import ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import sistema_eletricista.apps.user.routing

application = ProtocolTypeRouter({
	'websocket': AuthMiddlewareStack(
        URLRouter(
            #chat.routing.websocket_urlpatterns
            sistema_eletricista.apps.user.routing.websocket_urlpatterns
        )
    ),
    # Empty for now (http->django views is added by default)
})