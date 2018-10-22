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


	async def disconnect(self, close_code):
		pass

	async def connect(self):
		self.user = None
		print (self.user)
		self.room_name = 'teste'
		await self.channel_layer.group_add(self.room_name, self.channel_name)
		print (self.channel_name)
		
		await self.accept()

	async def receive(self, text_data):
		
		data = json.loads(text_data)

		if data.get('nome'):
			servico_id = None
		
			necessidade = data['necessidade']
			pedido_enviado = data['pedido_enviado']
			pedido_status = data['pedido_status']
			nome_ = data['nome']
			endereco = data['endereco']
			user = data['user']
			foto = data['foto']
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
			if(data.get('user_eletricista')):
				user_eletricista = data['user_eletricista']
				x = {
					'eletricista' : user_eletricista
				}
				usuarios_final.append(x)
				
				#eletricistas_finalizar.append(user_eletricista)
			else:
				user_eletricista = None

			if(data.get('user')):
				user_cliente = data['user']
				x = {
					'cliente' : user_cliente
				}
				usuarios_final.append(x)
				
				#clientes_finalizar.append(user_cliente)
			else:
				user_cliente = None
			cliente = dados[0]['nome']
			# eletricista = dados[1]['user_eletricista']
			valor = 53.30
			endereco = dados[0]['endereco']

			#print (clientes_finalizar, eletricistas_finalizar)
			# falta só o endereço para terminar o objeto PedidoDeServico
			print ('USUARIOS_FINAL')
			if(data.get('casal')):
				print(data.get('casal'))
				eletricista = data.get('casal')['eletricista']
				cliente = data.get('casal')['cliente']
				servico_feito = PedidoDeServico.objects.create(
					#data=data_real,
					valor=valor,
					endereco=endereco,
					cliente=cliente,
					eletricista=eletricista,
					status='Em andamento'
					)
				print (servico_feito.id)
				print (servico_feito)
				servico_id = servico_feito.id





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
					'user_eletricista' : user_eletricista,
					'servico_id' : servico_id,
					'foto' : foto
					
				})
		
	


	async def ws_message(self, event):
		await self.send(text_data=json.dumps({
				'pedido_enviado' : event['pedido_enviado'],
				'pedido_status' : event['pedido_status'],
				'necessidade' : event['necessidade'],
				'nome' : event['nome'],
				'endereco' : event['endereco'],
				'user' : event['user'],
				'user_eletricista' : event['user_eletricista'],
				'servico_id' : event['servico_id'],
				'foto' : event['foto']
				
			}))











class ServicoConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.user = None
		
		#self.usuarios_final = []
		# self.clientes_finalizar = [
		
		#print (self.user.username)
		print(self.scope)
		self.room_name = self.scope['url_route']['kwargs']['id_servico']
		await self.channel_layer.group_add(self.room_name, self.channel_name)
		
		await self.accept()

	async def receive(self, text_data):
		data = json.loads(text_data)
		#print (data)
		# nomes.append(data.get('user_em_questao'))
		# if self.user == None:
		# 	self.user = data.get('user_em_questao')
		# else:
		# 	print('self.user ja ocupado')
		# print(nomes)
		# print(self.user)

		# if data.get('nome'):
		
		# 	necessidade = data['necessidade']
		# 	pedido_enviado = data['pedido_enviado']
		# 	pedido_status = data['pedido_status']
		# 	nome_ = data['nome']
		# 	endereco = data['endereco']
		# 	user = data['user']
		# 	user_eletricista = data.get('user_eletricista')
			
		# 	dados_ = {
		# 		'necessidade' : necessidade,
		# 		'pedido_enviado' : pedido_enviado,
		# 		'pedido_status' : pedido_status,
		# 		'nome' : nome_,
		# 		'endereco' : endereco,
		# 		'user' : user,
		# 		'user_eletricista' : user_eletricista
				
		# 	}
		# 	dados.append(dados_)


		if data.get('pedido_resposta_eletricista') == True or data.get('pedido_resposta_eletricista') == False:
			
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
			
			pausar_resposta_eletricista = data['pausar_resposta_eletricista']
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
			
			finalizar_resposta_eletricista = data['finalizar_resposta_eletricista']
			finalizar_resposta_cliente = data['finalizar_resposta_cliente']
			if(data.get('user_eletricista')):
				user_eletricista = data['user_eletricista']
				x = {
					'eletricista' : user_eletricista
				}
				usuarios_final.append(x)
				
				#eletricistas_finalizar.append(user_eletricista)
			else:
				user_eletricista = None

			if(data.get('user')):
				user_cliente = data['user']
				x = {
					'cliente' : user_cliente
				}
				usuarios_final.append(x)
				
				#clientes_finalizar.append(user_cliente)
			else:
				user_cliente = None
			
			if data.get('finalizar_resposta_eletricista') == True and data.get('finalizar_resposta_cliente') == True:

				servico_finalizado = PedidoDeServico.objects.get(id=self.room_name)
				servico_finalizado.status = 'Finalizado'
				servico_finalizado.save()
				
				print (servico_finalizado)
				print(servico_finalizado.status)
				
				




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
					'user_eletricista' : user_eletricista,
					
				})
		elif (data.get('pedido_resposta_eletricista') == True or data.get('pedido_resposta_eletricista') == False):
			await self.channel_layer.group_send(
				self.room_name,
				{
					'type' : 'ws_message_pedido',
					'pedido_resposta_eletricista' : data['pedido_resposta_eletricista'],
					'pedido_resposta_cliente' : data['pedido_resposta_cliente'],
					'user' : user_cliente,
					'user_eletricista' : user_eletricista,
					
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
					'user_eletricista' : user_eletricista,
					
					
				})
		elif data.get('continuar_resposta_eletricista') == True or data.get('continuar_resposta_eletricista') == False:
			await self.channel_layer.group_send(
				self.room_name,
				{
					'type' : 'ws_message_continuar',
					'continuar_resposta_eletricista' : data['continuar_resposta_eletricista'],
					'continuar_resposta_cliente' : data['continuar_resposta_cliente'],
					'user' : user_cliente,
					'user_eletricista' : user_eletricista,
					
					
				})
		elif data.get('finalizar_resposta_eletricista') == True or data.get('finalizar_resposta_eletricista') == False:
			await self.channel_layer.group_send(
				self.room_name,
				{
					'type' : 'ws_message_finalizar',
					'finalizar_resposta_eletricista' : data['finalizar_resposta_eletricista'],
					'finalizar_resposta_cliente' : data['finalizar_resposta_cliente'],
					'user' : user_cliente,
					'user_eletricista' : user_eletricista,
					
					
				})
	

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
				'user_eletricista' : event['user_eletricista'],
				
				#'user_eletricista' : event['user_eletricista']
				
			}))

	async def ws_message_pausar(self, event):
		await self.send(text_data=json.dumps({
				'pausar_resposta_eletricista' : event['pausar_resposta_eletricista'],
				'pausar_resposta_cliente' : event['pausar_resposta_cliente'],
				'user' : event['user'],
				'user_eletricista' : event['user_eletricista'],
				
				
			}))

	async def ws_message_continuar(self, event):
		await self.send(text_data=json.dumps({
				'continuar_resposta_eletricista' : event['continuar_resposta_eletricista'],
				'continuar_resposta_cliente' : event['continuar_resposta_cliente'],
				'user' : event['user'],
				'user_eletricista' : event['user_eletricista'],
				
				
			}))

	async def ws_message_finalizar(self, event):
		await self.send(text_data=json.dumps({
				'finalizar_resposta_eletricista' : event['finalizar_resposta_eletricista'],
				'finalizar_resposta_cliente' : event['finalizar_resposta_cliente'],
				'user' : event['user'],
				'user_eletricista' : event['user_eletricista'],
				
				
			}))


	async def disconnect(self, close_code):
		pass


