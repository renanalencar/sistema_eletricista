from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .cliente.models import Cliente
from .eletricista.models import Eletricista

class ClienteConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name = 'teste'
		await self.channel_layer.group_add(self.room_name, self.channel_name)
		await self.accept()

	async def receive(self, text_data):
		data = json.loads(text_data)
		if data.get('user'):
		
			necessidade = data['necessidade']
			pedido_enviado = data['pedido_enviado']
			pedido_status = data['pedido_status']
			nome_ = data['nome']
			endereco = data['endereco']
			user = data['user']
		elif (data.get('pedido_resposta_eletricista') == True or data.get('pedido_resposta_eletricista') == False):
			print ('estou passando por aqui')
			pedido_resposta_eletricista = data['pedido_resposta_eletricista']
			pedido_resposta_cliente = data['pedido_resposta_cliente']
		else:
			print ('estou passando por aqui também')
			pausar_resposta_eletricista = data['pausar_resposta_eletricista'],
			pausar_resposta_cliente = data['pausar_resposta_cliente']
		
		if data.get('nome'):
			await self.channel_layer.group_send(
				self.room_name,
				{
					'type' : 'ws_message',
					'pedido_enviado' : pedido_enviado,
					'pedido_status' : pedido_status,
					'necessidade' : necessidade,
					'nome' : nome_,
					'endereco' : endereco,
					'user' : user
				})
		elif (data.get('pedido_resposta_eletricista') == True or data.get('pedido_resposta_eletricista') == False):
			await self.channel_layer.group_send(
				self.room_name,
				{
					'type' : 'ws_message_pedido',
					'pedido_resposta_eletricista' : data['pedido_resposta_eletricista'],
					'pedido_resposta_cliente' : data['pedido_resposta_cliente']
					
				})
		else:
			await self.channel_layer.group_send(
				self.room_name,
				{
					'type' : 'ws_message_pausar',
					'pausar_resposta_eletricista' : data['pausar_resposta_eletricista'],
					'pausar_resposta_cliente' : data['pausar_resposta_cliente']
					
				})
	

	async def disconnect(self, close_code):
		pass

	async def ws_message(self, event):
		await self.send(text_data=json.dumps({
				'pedido_enviado' : event['pedido_enviado'],
				'pedido_status' : event['pedido_status'],
				'necessidade' : event['necessidade'],
				'nome' : event['nome'],
				'endereco' : event['endereco'],
				'user' : event['user']
			}))

	async def ws_message_pedido(self, event):
		await self.send(text_data=json.dumps({
				'pedido_resposta_eletricista' : event['pedido_resposta_eletricista'],
				'pedido_resposta_cliente' : event['pedido_resposta_cliente']
				
			}))

	async def ws_message_pausar(self, event):
		await self.send(text_data=json.dumps({
				'pausar_resposta_eletricista' : event['pausar_resposta_eletricista'],
				'pausar_resposta_cliente' : event['pausar_resposta_cliente']
				
			}))

