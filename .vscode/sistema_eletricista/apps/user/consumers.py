from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .cliente.models import Cliente
from .eletricista.models import Eletricista
from sistema_eletricista.apps.post.PedidoDeServico.models import PedidoDeServico
import json
import datetime

dados = []
eletricistas_finalizar = []
clientes_finalizar = []
usuarios_final = []
print ('eu estou aqui')



class ClienteConsumer(AsyncWebsocketConsumer):



	async def connect(self):
		self.user = None
		print (self.user)
		#self.usuarios_final = []
		# self.clientes_finalizar = []
		self.index_elec = 0
		self.index_cliente = 0
		print ('eu sou o usuario')
		
		#print (self.user.username)
		self.room_name = 'teste'
		await self.channel_layer.group_add(self.room_name, self.channel_name)
		print (self.channel_name)
		
		await self.accept()

	async def receive(self, text_data):
		#print(self.eletricistas_finalizar, self.clientes_finalizar)
		
		data = json.loads(text_data)
		#print (data)
		# nomes.append(data.get('user_em_questao'))
		# if self.user == None:
		# 	self.user = data.get('user_em_questao')
		# else:
		# 	print('self.user ja ocupado')
		# print(nomes)
		# print(self.user)

		if data.get('nome'):
		
			necessidade = data['necessidade']
			pedido_enviado = data['pedido_enviado']
			pedido_status = data['pedido_status']
			nome_ = data['nome']
			endereco = data['endereco']
			user = data['user']
			user_eletricista = data.get('user_eletricista')
			
			dados_ = {
				'necessidade' : necessidade,
				'pedido_enviado' : pedido_enviado,
				'pedido_status' : pedido_status,
				'nome' : nome_,
				'endereco' : endereco,
				'user' : user,
				'user_eletricista' : user_eletricista
				
			}
			dados.append(dados_)


		elif data.get('pedido_resposta_eletricista') == True or data.get('pedido_resposta_eletricista') == False:
			print('to em cima dos dados do userelec')
			print (data)
			pedido_resposta_eletricista = data['pedido_resposta_eletricista']
			pedido_resposta_cliente = data['pedido_resposta_cliente']
			if(data.get('user_eletricista')):
				user_eletricista = data['user_eletricista']
			else:
				user_eletricista = None

			if(data.get('user')):
				user_cliente = data['user']
			else:
				user_cliente = None
			

		elif data.get('pausar_resposta_eletricista') == True or data.get('pausar_resposta_eletricista') == False:
			
			pausar_resposta_eletricista = data['pausar_resposta_eletricista'],
			pausar_resposta_cliente = data['pausar_resposta_cliente']
			if(data.get('user_eletricista')):
				user_eletricista = data['user_eletricista']
			else:
				user_eletricista = None

			if(data.get('user')):
				user_cliente = data['user']
			else:
				user_cliente = None
			
			
		

		elif data.get('continuar_resposta_eletricista') == True or data.get('continuar_resposta_eletricista') == False:
			print ('estou passando por aqui também')
			continuar_resposta_eletricista = data['continuar_resposta_eletricista'],
			continuar_resposta_cliente = data['continuar_resposta_cliente']
			if(data.get('user_eletricista')):
				user_eletricista = data['user_eletricista']
			else:
				user_eletricista = None

			if(data.get('user')):
				user_cliente = data['user']
			else:
				user_cliente = None
			

		elif data.get('finalizar_resposta_eletricista') == True or data.get('finalizar_resposta_eletricista') == False:
			print ('estou passando por aqui também')
			
			finalizar_resposta_eletricista = data['finalizar_resposta_eletricista'],
			finalizar_resposta_cliente = data['finalizar_resposta_cliente']
			if(data.get('user_eletricista')):
				user_eletricista = data['user_eletricista']
				x = {
					'eletricista' : user_eletricista
				}
				usuarios_final.append(x)
				print(usuarios_final)
				print('dentro do iffffffffffffffffffffff elec')
				#eletricistas_finalizar.append(user_eletricista)
			else:
				user_eletricista = None

			if(data.get('user')):
				user_cliente = data['user']
				x = {
					'cliente' : user_cliente
				}
				usuarios_final.append(x)
				print(usuarios_final)
				print ('dentro do ifffffffff cliente')
				#clientes_finalizar.append(user_cliente)
			else:
				user_cliente = None
			
			if data.get('finalizar_resposta_eletricista') == True and data.get('finalizar_resposta_cliente') == True:
				dados.append(dados_)
				print (dados)
				
				# data_parcial = datetime.datetime.now()
				# data_real = str(data_parcial.day) + '/' + str(data_parcial.month) + '/' + str(data_parcial.year)
				cliente = dados[0]['nome']
				# eletricista = dados[1]['user_eletricista']
				valor = 53.30
				endereco = dados[0]['endereco']
				print ('eu sou o user_cliente e user_eletricista')
				print(usuarios_final)
				u = usuarios_final[0]
				w = usuarios_final[1]
				if 'eletricista' in u:
					eletricista = u['eletricista']
					cliente = w['cliente']
				else:
					eletricista = w['eletricista']
					cliente = u['cliente']

				#print (clientes_finalizar, eletricistas_finalizar)
				# falta só o endereço para terminar o objeto PedidoDeServico
				
				servico_feito = PedidoDeServico.objects.create(
					#data=data_real,
					valor=valor,
					endereco=endereco,
					cliente=cliente,
					eletricista=eletricista
					)
				print (servico_feito)
				#print(self.eletricistas_finalizar, self.clientes_finalizar)




		#print (dados)
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
					'user' : user,
					'user_eletricista' : user_eletricista
				})
		elif (data.get('pedido_resposta_eletricista') == True or data.get('pedido_resposta_eletricista') == False):
			await self.channel_layer.group_send(
				self.room_name,
				{
					'type' : 'ws_message_pedido',
					'pedido_resposta_eletricista' : data['pedido_resposta_eletricista'],
					'pedido_resposta_cliente' : data['pedido_resposta_cliente'],
					'user' : user_cliente,
					'user_eletricista' : user_eletricista
					#'user_eletricista' : data['user_eletricista']
					
				})
		elif data.get('pausar_resposta_eletricista') == True or data.get('pausar_resposta_eletricista') == False:
			await self.channel_layer.group_send(
				self.room_name,
				{
					'type' : 'ws_message_pausar',
					'pausar_resposta_eletricista' : data['pausar_resposta_eletricista'],
					'pausar_resposta_cliente' : data['pausar_resposta_cliente'],
					'user' : user_cliente,
					'user_eletricista' : user_eletricista
					
				})
		elif data.get('continuar_resposta_eletricista') == True or data.get('continuar_resposta_eletricista') == False:
			await self.channel_layer.group_send(
				self.room_name,
				{
					'type' : 'ws_message_continuar',
					'continuar_resposta_eletricista' : data['continuar_resposta_eletricista'],
					'continuar_resposta_cliente' : data['continuar_resposta_cliente'],
					'user' : user_cliente,
					'user_eletricista' : user_eletricista
					
				})
		elif data.get('finalizar_resposta_eletricista') == True or data.get('finalizar_resposta_eletricista') == False:
			await self.channel_layer.group_send(
				self.room_name,
				{
					'type' : 'ws_message_finalizar',
					'finalizar_resposta_eletricista' : data['finalizar_resposta_eletricista'],
					'finalizar_resposta_cliente' : data['finalizar_resposta_cliente'],
					'user' : user_cliente,
					'user_eletricista' : user_eletricista
					
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
				'user' : event['user'],
				'user_eletricista' : event['user_eletricista']
				#'meu' : json.dumps(event['meu'])
			}))

	async def ws_message_pedido(self, event):
		await self.send(text_data=json.dumps({
				'pedido_resposta_eletricista' : event['pedido_resposta_eletricista'],
				'pedido_resposta_cliente' : event['pedido_resposta_cliente'],
				'user' : event['user'],
				'user_eletricista' : event['user_eletricista']
				#'user_eletricista' : event['user_eletricista']
				
			}))

	async def ws_message_pausar(self, event):
		await self.send(text_data=json.dumps({
				'pausar_resposta_eletricista' : event['pausar_resposta_eletricista'],
				'pausar_resposta_cliente' : event['pausar_resposta_cliente'],
				'user' : event['user'],
				'user_eletricista' : event['user_eletricista']
				
			}))

	async def ws_message_continuar(self, event):
		await self.send(text_data=json.dumps({
				'continuar_resposta_eletricista' : event['continuar_resposta_eletricista'],
				'continuar_resposta_cliente' : event['continuar_resposta_cliente'],
				'user' : event['user'],
				'user_eletricista' : event['user_eletricista']
				
			}))

	async def ws_message_finalizar(self, event):
		await self.send(text_data=json.dumps({
				'finalizar_resposta_eletricista' : event['finalizar_resposta_eletricista'],
				'finalizar_resposta_cliente' : event['finalizar_resposta_cliente'],
				'user' : event['user'],
				'user_eletricista' : event['user_eletricista']
				
			}))

