from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from sistema_eletricista.apps.user.models import ValorPorHora
from .cliente.models import Cliente
from .eletricista.models import Eletricista
from sistema_eletricista.apps.post.PedidoDeServico.models import PedidoDeServico
import json
from datetime import datetime
import time

horarios = []
id_servico = None
dados = []
eletricistas_finalizar = []
clientes_finalizar = []
usuarios_final = []

valores_atuais = ValorPorHora.objects.last()

valor_meia_hora = valores_atuais.valor_meia_hora
valor_primeira_hora = valores_atuais.valor_primeira_hora
valor_demais_horas = valores_atuais.valor_demais_horas

print(valor_meia_hora, valor_primeira_hora, valor_demais_horas)

def calculaValor(horas, minutos):
    if horas == 0:
        if minutos < 30:
            return valor_meia_hora
        elif minutos >= 30:
            return valor_primeira_hora
    elif horas == 1:
        if minutos < 30:
            return valor_primeira_hora
        elif minutos >= 30:
            return valor_primeira_hora + valor_demais_horas
    else:
        if minutos < 30:
            return valor_primeira_hora + ((horas - 1) * valor_demais_horas)
        elif minutos >= 30:
            return valor_primeira_hora + (horas * valor_demais_horas)


def calculaHorasEMinutos(inicio, tempo_de_pausa, fim):
    tempo_de_servico = fim - inicio - tempo_de_pausa

    #tempo_de_servico em segundos!
    #calulando horas/minutos/segundos dividindo e pegando os restos
    horas = tempo_de_servico // 3600 
    tempo_de_servico_restante = tempo_de_servico % 3600

    minutos = tempo_de_servico_restante // 60
    segundos = tempo_de_servico_restante % 60

    return {
            'horas': horas,
            'minutos' : minutos
            }



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
			coords_cliente = data.get('coords_cliente')
			coords_elec = data.get('coords_elec')
			
			dados_ = {
				'necessidade' : necessidade,
				'pedido_enviado' : pedido_enviado,
				'pedido_status' : pedido_status,
				'nome' : nome_,
				'endereco' : endereco,
				'user' : user,
				'user_eletricista' : user_eletricista,
				'coords_cliente' : coords_cliente,
				'coords_elec' : coords_elec
				
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
			#cliente = dados[0]['nome']
			# eletricista = dados[1]['user_eletricista']
			valor = 53.30
			endereco = dados[0]['endereco']

			dados.clear()

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
					'foto' : foto,
					'coords_cliente' : coords_cliente,
					'coords_elec' : coords_elec
					
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
				'foto' : event['foto'],
				'coords_cliente' : event['coords_cliente'],
				'coords_elec' : event['coords_elec']
				
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
			servico_iniciado = {
				'tempo_iniciado' : int(time.time())
			}
			horarios.append(servico_iniciado)
			
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
			servico_pausado = {
				'tempo_pausado' : int(time.time())
			}
			horarios.append(servico_pausado)
			
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
			servico_continuado = {
				'tempo_continuado' : int(time.time())
			}

			horarios.append(servico_continuado)
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
				servico_finalizado = {
					'tempo_finalizado' : int(time.time())
				}
				horarios.append(servico_finalizado)
				print(horarios)
				pausado = 0
				continuado = 0
				inicio = horarios[0]['tempo_iniciado']
				fim = horarios[len(horarios) - 1]['tempo_finalizado']

				for i in range(1, len(horarios) - 1):
					if 'tempo_pausado' in horarios[i]:
						pausado += horarios[i]['tempo_pausado']
					if 'tempo_continuado' in horarios[i]:
						continuado += horarios[i]['tempo_continuado']

				total_pausado = continuado - pausado
				
				horas_minutos = calculaHorasEMinutos(inicio, total_pausado, fim)
				
				valor_do_servico = calculaValor(int(horas_minutos['horas']), int(horas_minutos['minutos']))

			   	##########################################################
				#                                                        #
				#EFETUAR O PAGAMENTO AQUI com a variavel valor_do_servico#
				#														 #
				##########################################################

				servico_finalizado = PedidoDeServico.objects.get(id=self.room_name)
				servico_finalizado.status = 'Finalizado'
				servico_finalizado.valor = valor_do_servico
				servico_finalizado.save()
				
				print (servico_finalizado)
				print(servico_finalizado.status)
				horarios.clear()
				




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


