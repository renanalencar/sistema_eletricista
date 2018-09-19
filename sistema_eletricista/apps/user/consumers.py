from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .cliente.models import Cliente
from .eletricista.models import Eletricista

class ClienteConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name = 'teste'
		await self.channel_layer.group_add(
				self.room_name,
				self.channel_name
			)
		await self.accept()

	async def receive(self, text_data):
		data = json.loads(text_data)
		print (data)
		necessidade = data['necessidade']
		pedido_enviado = data['pedido_enviado']
		pedido_status = data['pedido_status']
		usuario = data['usuario']
		endereco = data['endereco']
		await self.channel_layer.group_send(
			self.room_name,
			{
				'type' : 'ws_message',
				'pedido_enviado' : pedido_enviado,
				'pedido_status' : pedido_status,
				'necessidade' : necessidade,
				'usuario' : usuario,
				'endereco' : endereco
			})
	

	async def disconnect(self, close_code):
		pass

	async def ws_message(self, event):
		await self.send(text_data=json.dumps({
				'pedido_enviado' : event['pedido_enviado'],
				'pedido_status' : event['pedido_status'],
				'necessidade' : event['necessidade'],
				'usuario' : event['usuario'],
				'endereco' : event['endereco']
			}))

