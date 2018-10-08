from channels.routing import ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack #SessionMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url, include
import sistema_eletricista.apps.user.routing
from sistema_eletricista.apps.user import consumers

application = ProtocolTypeRouter({
	'websocket': AuthMiddlewareStack(
        URLRouter(
            #chat.routing.websocket_urlpatterns
            sistema_eletricista.apps.user.routing.websocket_urlpatterns
            #url(r'^ws/user/index/$', consumers.ClienteConsumer)
        )
    ),
    # Empty for now (http->django views is added by default)
})