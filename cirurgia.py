import numpy as np
import random
import copy
#Variáveis globais
Ants = []
Cirurgias = []
Salas = []
Cirurgioes = []


'''
Classe State, indica um estado final da instância de agendamento
Recebe uma lista de Cirurgias, um estado é idêntico ao outro caso as cirurgias foram agendadas
no mesmo instante
'''

def byTC(cirurgia):
	return cirurgia.tc


#Grafo é direcionado
class Graph:
	def __init__ (self):
		self.nodes = {}
		self.revNodes = {}
		self.edges = {}
		self.revEdges = {}
		self.nidx = 0
		self.eidx = 0

	def addNode(self,s):
		if s not in self.nodes.keys():
			self.nodes[ s ] = self.nidx
			self.revNodes[self.nidx] = s
			self.nidx = self.nidx + 1 

	#Sao indices, em que as operacoes tambem sao mapeados por indices
	def addEdge(self,s1,op,s2):
		e = (s1,op,s2)
		if( e not in self.edges.keys()  ):
			self.edges[ e ] = self.eidx
			self.revEdges[self.eidx] = e
			self.eidx = self.eidx + 1

	def getNode(self,idx):
		return self.revNodes[idx]
	
	def getEdge(self,idx):
		return self.revEdges[idx]

	def showNodes(self):
		print("Nodes")
		for node in self.nodes.keys():
			print( node.lst )
	def showEdges(self):
		print("Edges")
		for edge in self.edges.keys():
			print("Node 1")
			for cirurgia in edge[0].Cirurgias:
				print(cirurgia.id,cirurgia.dia)

			print("Operation: ",edge[1])
			print("Node 2")
			for cirurgia in edge[2].Cirurgias:
				print(cirurgia.id,cirurgia.dia)
			


class State:
	# Recebe como parâmetro uma lista de cirurgias
	id_agendadas = []
	n_agendadas = []
	def __init__ (self, Cirurgias,value  ):
		
		self.Cirurgias = copy.deepcopy(Cirurgias)
		for cirurgia in Cirurgias:
			if(cirurgia.dia != -1):
				self.id_agendadas.append(cirurgia.id)
			else:
				self.n_agendadas.append(cirurgia.id)
		#Valor da função objetivo
		self.value = value

	def __hash__(self):
		return hash(tuple(self.Cirurgias))

	#Uma cirurgia é diferente de outra, caso exista alguma cirurgia agendada de forma diferente.
	def __eq__(self, Other):
		# if(self.value != Other.value):
		# 	return False
		for cirurgia_x in self.Cirurgias:
			for cirurgia_y in Other.Cirurgias:
				
				if(cirurgia_x.id == cirurgia_y.id):
					# print("cirurgia_x_id: {} agendada no dia {} ".format(cirurgia_x.id,cirurgia_x.dia))
					# print("cirurgia_y_id: {} agendada no dia {} ".format(cirurgia_y.id,cirurgia_y.dia))
					if( 
						( cirurgia_x.sala != cirurgia_y.sala 
						or cirurgia_x.dia != cirurgia_y.dia 
						or cirurgia_x.semana != cirurgia_y.semana
						or cirurgia_x.tc_inicio != cirurgia_y.tc_inicio 
						or cirurgia_x.tc_fim != cirurgia_y.tc_fim 
						or cirurgia_x.cirurgiao != cirurgia_y.cirurgiao) ):
							return False
			
		return True

	def chooseOP(self,op):
		if(op == 0):
			return self.op1()
		elif(op==1):
			return self.op2()
		elif(op==2):
			return self.op2()

	# E1 < Remove > Ex 
	#Esta operacao remove uma cirurgia agendada aleatoriamente, de acordo com a probabilidade de prioridade
	#Prioridades 1 tem baixa probalidade de ser excluída
	#
	def op2(self):
		#Seleciona a cirurgia a ser removida
		New_Cirurgias = copy.deepcopy(self.Cirurgias)

		id_ = random.choice(self.id_agendadas)
		print("Cirurgia id: {} desagendada".format(id_))
		for cirurgia in New_Cirurgias:
			#Desagenda a cirurgia.
			if(cirurgia.id == id_ ):
				cirurgia.remove()
				break
		
		return State(New_Cirurgias,FO(New_Cirurgias)),id_

	#Adiciona uma cirurgia aleatória
	#Começa com um 
	def op1(self):
		#Procura os tempos em que as cirurgias podem ser adicionadas
		
		tempos_d = {}
		dia = 1
		tc = 1
		qt_f = 1

		while(dia <= 5):
			while(tc <= 46):
				for sala in Salas:
					found = False
					for cirurgia in self.Cirurgias:
						#é levado em consideração a limpeza da sala.
						#Se a cirurgia finaizou 2 tcs atrás, esse tc não é disponível, pois é da limpeza
						if(cirurgia.dia == dia and (cirurgia.tc_inicio == tc or cirurgia.tc_fim - 2 == tc ) and cirurgia.sala == sala.id):
							found = True
							break

					#caso não tenha encontrado ninguém nessa situação, é possível agendar alguem nesse tempo
					#procura o proximo tempo fim.
					if(found == False):
						tc_fim = tc + 1
						while(tc_fim <= 46):
							found_end = False
							for cirurgia in self.Cirurgias:
								if(cirurgia.dia == dia and cirurgia.tc_inicio == tc_fim and cirurgia.sala == sala.id):
									found_end = True
									break
							if(found_end):
								break
							tc_fim += 1
						#Tempo anterior que é o correto
						tc_fim -= 1
						# #Contabiliza o tempo junto com a limepza, caso for a ultima cirurgia, deixa ela sem a limpeza
						# if(tc == 44 and tc_fim == 46 ):
						if(tc_fim != 46):
							tc_fim -= 2
						value = tc_fim - tc +1
						#t[(tempo_disponivel,id)] = ( dia,sala.id, tc )
						if(value > 0 and tc_fim > 0):
							tempos_d[ (value,qt_f) ] = ( dia, sala.id, tc )
							qt_f += 1
				tc+=1
			dia += 1
		
		#Após ter todos os tempos disponveis, verificamos quais cirurgias podem ser agendadas
		#A restrição do problema para cirurgias que não possam ser agendadas, será penalizada na funcao FO.
		#A adição é feita no tempo correto, no entanto, para verificar se a sala/cirurgiao possam ser utilizados, será verificado em um próximo momento
		#Procuro as cirurgias que possam ser agendadas com o tempo
		# print(tempos_d)

		#Garantir escopo de viabiliade ( Cirurgia só é possível caso Cirurgiao e Sala possam realizá-la)
		pos_cirurgia = []
		for wc,_id in tempos_d.keys():
			for cirurgia in self.Cirurgias:
				#Se a cirurgia não está agendada
				if(cirurgia.dia == -1):
					#Se o tempo para a conclusão daquela cirurgia for menor ou igual ao tempo disponível. Selecione
					if(cirurgia.tc <= wc):
						pos_cirurgia.append(cirurgia.id)


		#Coleto cirurgias randômicas
		try:
			select_id = random.choice(pos_cirurgia)
		except:
			select_id = -1
		#Crio um novo estado para a cirurgia
		New_Cirurgias = copy.deepcopy(self.Cirurgias)

		#Adiciono a cirurgia no dia X,no tempo Y, com inicio TC
		for cirurgia in New_Cirurgias:
			if(cirurgia.id == select_id):
				for wc,_id in tempos_d.keys():
					if(cirurgia.tc <= wc):
						d,s,w = tempos_d[ (wc,_id) ]
						cirurgia.add( d,s,w  )

		# print("Agendamento da cirurgia: {}".format(select_id))
		return State(New_Cirurgias, FO(New_Cirurgias) ),select_id
class Cirurgia:

	def __init__(self,id,p,w,e,h,tc):
		self.id = id
		self.p = p
		self.w = w
		self.e = e
		self.cirurgiao = h
		self.tc = tc
		self.sala = -1
		self.tc_inicio = -1
		self.tc_fim = -1
		self.dia = -1
		self.semana = -1
	#Overloading do 
	def __gt__(self,other):
		if(self.p < other.p):
			return True
		elif(self.p == other.p):
			if(self.w < other.w):
				return True
			elif(self.tc <= other.tc):
				return True
		return False

	def add(self,dia,sala,inicio):
		self.dia = dia
		self.sala = sala
		self.tc_inicio = inicio
		self.tc_fim = inicio+self.tc -1
		
	def remove(self):
		# print("Removido cirurgia_{}".format(self.id))
		self.dia = -1
		self.sala = -1
		self.cirurgiao = -1
		self.tc_inicio = -1
		self.tc_fim = -1
		self.semana = -1
		

	def setSala(self, s):
		self.sala = s

	def setDia(self,d):
		self.dia = d
	def setSemana(self,s):
		self.semana = s

	#Inicio da cirurgia e fim da cirurgia, inclusive
	def setTempo(self,a,b):
		self.tc_inicio = a
		self.tc_fim = b

	def setCirurgiao(self,cir):
		self.cirurgiao = cir

class Cirurgiao:

	def __init__ (self,id,especialidade):
		self.id = id
		self.e = especialidade
		self.hdia = 0
		self.hsemana = 0

	def utilizaCirurgiao(self,h):
		self.hdia += h
		self.hsemana += h
	def novoDia(self):
		self.hdia = 0
		self.especialidade = -1
	def novaSemana(self):
		self.hsemana = 0


class Sala:
	def __init__(self,id):
		self.id = id
		self.disponivel = 1
		self.especialidade = -1
	#Esse é o tempo que vai estar disponível após a limpeza da sala. no tempo Disponível a sala estará liberada
	#Por isso soma-se 3 unidades, h unidades do uso, + 2 unidades para limpeza, +1 para o tempo de disponibilidade
	def setEspecialidade(self,e):
		self.especialidade = e
	def setHora(self, h):
		self.disponivel = h+3

	def novoDia(self):
		self.disponivel = 1
		self.especialidade = -1

lp = { 1:3, 2:15,3:60,4:365 }
fp = { 1:90 , 2:20, 3:5, 4:1 }


#Necessário checar se essa FO está CORRETA ! 
#(Toy2 está com uma solução diferente Para 2 salas. Checar se a solução está CORRETA)

'''

Remover alguma Cirurgia

Conjuntos deletar: (X,Y,Z)
FO>X : 1000
FO<X : 1200

FO>Y : 1000
FO<Y : 1500

FO>Z : 1000
FO<Z : 2000
'''
def FO(Cirurgias):
	
	penalty = 0
	#Dar penalidade para instancias com restrições falhadas diferentemente?
	if(verificaInstancia(Cirurgias) == False):
		print("Instância FALHA")
		penalty += pow(10,9)+1
	for cirurgia in Cirurgias:
		vc = 0
		xcstd = 0
		zc = 0
		p1 = 0
		if(cirurgia.dia == -1 or cirurgia.tc_inicio == -1 or cirurgia.tc_fim == -1):
			zc = 1
		else:
			xcstd = 1

		if(cirurgia.dia + cirurgia.w > lp[ cirurgia.p ]):
			vc = 1

		if(cirurgia.p == 1 and cirurgia.dia > 1):
			p1 = 1

		penalty += 10*( pow(cirurgia.w +2, cirurgia.dia) )*p1

		if(cirurgia.dia != -1 ):
			penalty += ( pow(cirurgia.w +2 + cirurgia.dia, 2) + pow( cirurgia.w + 2 + cirurgia.dia - lp[cirurgia.dia],2 )*vc ) * xcstd
		else:
			penalty += ( pow( cirurgia.w + 7 ,2)*fp[cirurgia.p] +  fp[cirurgia.p]*vc*( pow(cirurgia.w +9 - lp[cirurgia.p],2) )) * zc

	return penalty

'''
TODO
- Verificar se os cirurgoes obedecam as constrains
- Verificar se as salas obedecam as constrains
'''

#Funcao verifica se a instancia está dentro do Bloco do Problema. 
def verificaInstancia(Cirurgias):

	#Verifica se todos que estão na mesma sala, possuem a mesma 
	dia = 1
	while(dia <= 5):
		esp_sala = {}
		for sala in Salas:
			for cirurgia in Cirurgias:
				if(cirurgia.dia == dia and cirurgia.sala == sala.id):
					if(sala.id in esp_sala.keys()):
						if(esp_sala[sala.id] != cirurgia.e):
							print("SALA {} COM CIRURGIA DIFERENTE !!!! ".format(sala.id))
							return False
					else:
						esp_sala[sala.id] = cirurgia.e
				
		dia += 1	

	#Verifica se o cirurgiao esta cumprindo o trabalho de 24 horas por dia e 100 horas por semana.
	tempo_gasto_semana = {}
	

	dia = 1
	while(dia <= 5):
		tempo_gasto_dia = {}
		for cirurgia in Cirurgias:
			if(cirurgia.id != -1 and cirurgia.dia == dia):
				try:
					tempo_gasto_semana[cirurgia.cirurgiao] += cirurgia.tc
				except:
					tempo_gasto_semana[cirurgia.cirurgiao] = cirurgia.tc

				try:
					tempo_gasto_dia[cirurgia.cirurgiao] += cirurgia.tc
				except:
					tempo_gasto_dia[cirurgia.cirurgiao] = cirurgia.tc
		for key in tempo_gasto_dia:
			if(tempo_gasto_dia[key] > 24):
				print("Cirurgiao {} EXCEDEU DIA".format(key))
				return False
		dia += 1
	for key in tempo_gasto_semana:
		if(tempo_gasto_semana[key] > 100):
			print("Cirurgiao {} EXCEDEU SEMANA".format(key))
			return False

	return True
#A sala tem especialidade
def agenda(tempo,dia,semana,Cirurgias,Salas,Cirurgioes):
	Cirurgias.sort(reverse=True)
	cnt = 0

	for s in range(len(Salas)):
		for tempo in range(1,47):
			#Se a sala ja foi toda ocupada, nao adianta tentar ocupá-la
			if(Salas[s].disponivel == 46):
				continue
			if(Salas[s].disponivel > tempo ):
				continue
			# print(Salas[s].disponivel, tempo)
			#Para cada cirurgia, tenta agendar 
			for cirurgia in Cirurgias:
				if(cirurgia.sala != -1 ):
					continue
				#Se sou uma cirurgia que posso ser agendada nessa sala, mas nao posso ser agendada no momento, aguardo para poder sera Agendada nessa sala
				if(Salas[s].especialidade == cirurgia.e and Salas[s].disponivel + cirurgia.tc -1 <= 46 and Salas[s].disponivel > tempo  ):
					continue

				#Há tempo disponível para agendar essa cirurgia
				# print(tempo,Salas[s].disponivel, Salas[s].disponivel + cirurgia.tc)
				if( (Salas[s].especialidade == -1 or Salas[s].especialidade == cirurgia.e) and tempo == Salas[s].disponivel and tempo + cirurgia.tc-1 <= 46):
					#Verifico se o cirurgiao requerido para essa cirurgia pode faze-la
					for cirurgiao in Cirurgioes:
						if (cirurgiao.id == cirurgia.cirurgiao and   cirurgiao.hdia + cirurgia.tc <= 24 and cirurgiao.hsemana + cirurgia.tc <=100  ):					
							#Configuro o cirurgiao
							print("Cirurgiao :{} no dia {} usou {} ".format(cirurgiao.id,dia,cirurgia.tc))
							cirurgiao.utilizaCirurgiao(cirurgia.tc)
							
							#Configuro a cirurgia
							cirurgia.setCirurgiao( cirurgiao.id )
							cirurgia.setTempo(tempo, tempo + cirurgia.tc-1)
							cirurgia.setDia(dia)
							cirurgia.setSemana(semana)

							#Utilizo a sala
							Salas[s].setEspecialidade(cirurgia.e)
							cirurgia.setSala(s)
							Salas[s].setHora(cirurgia.tc-1 + tempo)
							cnt += 1
	return cnt

def zeraDisponibilidade(tipo,Salas,Cirurgioes):
	for sala in Salas:
		sala.novoDia()
	if(tipo == "dia"):
		for cirurgiao in Cirurgioes:
			cirurgiao.novoDia()
	else:
		for cirurgiao in Cirurgioes:
			cirurgiao.novaSemana()



'''Algoritmo que agenda as cirurgias de forma gulosa, dando prioridade a algumas caracteristicas, retorna a configuração final das cirurgias agendadas
Tem como entrada: s- número de salas do problema, a lista com as Cirurgias, Cirurgioes e Salas.
'''
def agendaGreedy(s,Cirurgias,Salas,Cirurgioes ):
	tempo_atual = 1
	dia_atual = 1
	semana_atual = 1
	cirurgias_realizadas = 0

	while( cirurgias_realizadas < len(Cirurgias) ):
		cirurgias_realizadas += agenda(tempo_atual,dia_atual,semana_atual,Cirurgias,Salas,Cirurgioes)

		tempo_atual = 46

		#Acabou 
		if(tempo_atual == 46):
			zeraDisponibilidade("dia", Salas,Cirurgioes)
			tempo_atual = 1
			dia_atual += 1
		if(dia_atual==5):
			zeraDisponibilidade("semana", Salas,Cirurgioes)
			dial_atual = 1
			semana_atual += 1
			#Para de agendar as cirurgias
			break

	return None
'''
-- Uma formiga deve ser capaz de iniciar a sua busca a partir de uma cidade específica
-- Lembrar de todas as cidades visitadas
-- Armazenar o tamanho do caminho que está seguinte
'''
class Ant:
	# Vai armazenar os vértices já visitados
	
	def __init__(self,N,op,a,b,q):
		#quantidade de vértices no grafo
		self.alfa = a
		self.beta = b
		self.n = N
		self.op = op
		#Construo a funcao de probabilidade da formiga, de escolher uma operacao a ser realizada. prob[i][j][k], probabilidade de ir de i~j utilizando a operacao k
		# self.probability = [[[1.0 / float(self.op) for x in range(op)] for x in range(N)] for y in range(N)]
		self.probability = {}
		#Indices dos vértices visitados
		self.visited = []
		#Quantidade de feromonio excretada pela formiga
		self.Q = q

		#Arestas visitadas por esta formiga, (vi,op,vj)
		self.edges = []
	def addEdge(self,edge):
		self.edges.append(edge)
	def clear(self):
		self.visited = []

	def visitCity(self,i):
		self.visited.append(i)
	
	def isVisited(self,i):
		if(i in self.visited):
			return True
		return False

	def tamanhoCaminho(self):
		#Neste problema o tamanho do caminho é a quantidade de arestas
		
		#O tamanho do caminho na verdade vai ser o Quanto esse caminho incrementou na solução final

		# for edge in edges:
		return len(self.edges)


	def heuristica(self,vi,vj):
		#Heuristica será o Delta: (Quanto se ganha ao utilizar a aresta,   FO(cnj2)/FO(cnj1), assim, quanto maior o ganho 
		#melhor a atratividade de utilizar aquela aresta
		return vj.value*1.0/ vi.value*1.0


	def changeProbability(self,feromonio):
		#Pego a posicao da formiga
		self.at = self.visited[-1] #Estou no último vértice

		#Para cada vértice não visitado, verifico o valor de transição e monto a tabela de probabilidade
		#
		s = 0 #Soma de todas as probabilidades
		
		#A probabilidade será: Pi,j * Pk ( Prob de ir do vértice i ao vértice j utilizando Kth operacao)
		# print(self.at)
		v = G.getNode(self.at)


		#Gera a vizinhança do Estado Atual
		#Crio os estados não visitados ainda.	
		vizinhos = []
		for op in range(self.op):
			vizinho,_id = v.chooseOP(op)
			G.addNode(vizinho)
			edge = (G.getNode(self.at),op,vizinho)
			G.addEdge( G.getNode(self.at),op,vizinho )
			#Se o vértice já foi visitado continua
			if( G.nodes[vizinho] in self.visited):
				continue
			vizinhos.append( edge )

		
			valor_heuristica = self.heuristica(v,vizinho)
			# print("Valor da heuritica: ", valor_heuristica)
			# print("Valor do feromonio: ", feromonio[ self.at ][ G.nodes[vizinho] ][op])


			# self.probability[ edge ] = pow(feromonio[ self.at ][ G.nodes[vizinho] ][op],self.alfa)* pow(valor_heuristica,self.beta)
			try:
				self.probability[ edge ] = pow(feromonio[ edge ],self.alfa)* pow(valor_heuristica,self.beta)
			except:
				feromonio[edge] = 1
				self.probability[ edge ] = pow(feromonio[ edge ],self.alfa)* pow(valor_heuristica,self.beta)
			s += self.probability[ edge ]

		#Atualizo a probabilidade de todo mundo viável
		if(s != 0):
			for edge in vizinhos:
				self.probability[ edge ] = self.probability[ edge ]/s

	def depositaFeromonio(self,feromonio,graph):
		# lenght = self.tamanhoCaminho()
		print("Deposita feromonio")
		for edge in self.edges:
			e = graph.getEdge(edge)
			# print(E1,operacao, EX )
			value_added = e[0].value/e[2].value
			# Vao ser i,a e
			if(e not in feromonio.keys()):
				feromonio[ e ] = 1 + self.Q/(value_added*1.0) #Adiciono feromonio no caminho feromonio[i][j][op]
			else:
				feromonio[ e ] += self.Q/(value_added*1.0) #Adiciono feromonio no caminho feromonio[i][j][op]

# E1
#E3 E4
def evaporaFeromonio(feromonio,p,graph):
	print("Evapora Feromonio")
	for edge in graph.edges.keys():	
		#Caso nao tenha visitado aquela aresta ainda e nao tenha feromonio depositado, continue
		try:
			feromonio[edge] = feromonio[ edge ]*(1-p)
		except:
			pass

def read_instances(Cirurgias,Salas,Cirurgioes):
	x = input()
	n = int(x.split(" ")[0])
	s = int(x.split(" ")[1])

	for sala in range(s):
		Salas.append( Sala( (sala) )  )

	unique_id_cir = {}
	for i in range(n):
		cir = input()
		print(cir)
		c = cir.split(" ")
		Cirurgias.append(  Cirurgia(int(c[0]),int(c[1]),int(c[2]),int(c[3]),int(c[4]),int(c[5] ))  )
		unique_id_cir[ int(c[4]) ] = int( c[3] )
	
	for key in unique_id_cir.keys():
		Cirurgioes.append( Cirurgiao( key,unique_id_cir[key]  ) )



def printSolution(Cirurgias):
	print("Solucao encontrada: ")
	for cirurgia in Cirurgias:
		print("Id: ", cirurgia.id, " Prioridade: ", cirurgia.p , " Especialidade: ",cirurgia.e ,  " sala: " , cirurgia.sala, " dia: ", cirurgia.dia, " Inicio ", cirurgia.tc_inicio, " Fim ", cirurgia.tc_fim )



def checkConstrains(Cirurgias,Salas,Cirurgioes):
	#Verifica se não extrapola a quantidade de tempo
	return ''


def check(Cirurgias,Salas,Cirurgioes):

	print("Informacoes das Salas: ")
	for sala in Salas:
		print("Sala id: ", sala.id, " Disponivel: ", sala.disponivel)
	print("Informacoes das Cirurgias: ")
	for cirurgia in Cirurgias:
		print("Id: ", cirurgia.id, " Prioridade: ", cirurgia.p, " Tempo de Espera: ", cirurgia.w, 
			" Especialidade: ", cirurgia.e, " Cirurgiao: ", cirurgia.cirurgiao, " Duração: ", cirurgia.tc, " Sala: ", cirurgia.sala)

	print("Informacoes dos Cirurgioes: ")
	for cirurgiao in Cirurgioes:
		print("Cirurgiao id: " ,cirurgiao.id, " Cirurgiao especialidade: ", cirurgiao.e, " Hdia: ", cirurgiao.hdia, " hSemana ", cirurgiao.hsemana)



#Funcao para realizar o teste no grafo criado.
def change(Cirurgias):
	x = Cirurgias.copy()
	newlst = []
	for cirurgia in x:
		new_c = Cirurgia(cirurgia.id,cirurgia.p,cirurgia.w,cirurgia.e,cirurgia.cirurgiao,cirurgia.tc)
		new_c.setDia(random.randint(1,10))
		new_c.setSala(cirurgia.sala)
		new_c.setSemana(cirurgia.semana)
		new_c.setTempo(cirurgia.tc_inicio,cirurgia.tc_fim)
		newlst.append(new_c)
	
	return newlst




'''
TODO:
1- Criar a leitura das instancias do problema - 30 Min                            		> Ok
2- Verificar se a função gulosa está realizando o agendamento corretamente        		> Ok
3- Criar a função que verifica se as cirurgias foram agendadas corretamente       		> Sem prioridade
4- Alterar a função objetivo													  		> Alterar a função objetivo
5- Ajustar as formigas para fazerem a alteração do Problema                       		> Ok ( Falta verificar se está tudo certo. )
6- Criar e ajustar funções de de geração de vizinhança							  		> Ok
7- Testar se o algoritmo está funcionando corretamente                            		> FAZER ( PRIORIDADE )
 7.1 - Testar se as iterações estão corretas, analisar o comportamento das formigas     > FAZER ( PRIORIDADE ) (RODRIGO) 
 7.2 - Testar se as funções de probabilidade estão sendo alteradas de acordo			> FAZER ( PRIORIDADE ) (RODRIGO)
 7.3 - TESTAR A FO ( URGÊNCIA MÁXIMA ! )                                                > FAZER ( VILMA )  
 7.4 - Criar dois operadores : Adição e Remoção Guloso 									> FAZER ( VILMA )

8- Realizar Melhorias                                                             		> FAZER
 8.1 Não visitar ESTADOS falhos !!! Isso pode prejudicar o algoritmo, ou criar uma operacao que remove INCONSISTENCIA !!!! ( PRONTO !)
 8.2 Verificar se não visitando com estados RUINS melhora a convergência do algoritmo

9- Otimizar                                                                       		> Inumeras funcoes podem ser otimizadas. 
 9.1 Aumentar a probabilidade de escolha de vertices com FO BAIXA !						> ( Pensar )

10. Alterar 46 > 48 e adicionar variáveis globais
'''



def main():
	
	read_instances(Cirurgias,Salas,Cirurgioes)
	check(Cirurgias,Salas,Cirurgioes) 
	agendaGreedy(len(Salas),Cirurgias,Salas,Cirurgioes )
	checkConstrains(Cirurgias, Salas, Cirurgioes)
	printSolution(Cirurgias)
	print("Funcao Objetivo: ", FO(Cirurgias))
	
	# '''
	# 	Inicio da Heurística
	# '''
	s1 = State(Cirurgias,FO(Cirurgias))
	global G,feromonio
	G = Graph()
	
	#Nó inicial das formigas
	G.addNode(s1)		

	#Inicialmente todas as formigas iniciam a sua busca no nó 0, que é o da solução gulosa

	best_rota = []
	best_value = 10000000000

	max_iter = 100
	N = 1000
	alfa = 1
	beta = 1
	p = 0.5
	
	# graph = [[0 for x in range(N)] for y in range(N)]  
	#Problema aqui, visita muitos nós e da overflow
	# feromonio = [[[1 for k in range(2)] for j in range(N)] for i in range(N)] # Feromonio[i][j][op]
	
	#Alteração do feromonio para acessar um estado com lista encadeada, entrada é a aresta, saída é o total de ferômonio depositado nesta aresta
	#Aresta será levado em consideração o Mapeamento da aresta no GRAFO
	#Inicialmente TODOS começam com a mesma quantidade de ferômonio, no momento do depósito ( caso seja a primeira vez será adicionado o valor de 1 unidade)
	feromonio = {}
	
	it = 0
	best_formiga = None
	max_nodes = 10 # Cada formiga irá descobrir 10 nós
	n_formigas = 100


	for i in range(n_formigas):
		Ants.append( Ant(N,2,alfa,beta,1) )
	f = 0
	best_visited = s1.value
	best_solution = s1.Cirurgias.copy()
	while(it != max_iter):

		#Fazer uma mutação nas Formigas !!!
		#Armazenar nas formigas, o caminho de arestas com MENOR valor possivel
		for ant in Ants:
			print("Inicio da formiga id {}".format(f%n_formigas))
			f += 1
			ant.clear()
			
			#Para cada inicio, coloca uma formiga em uma cidade aleatória diferente.

			#Aumentar a chance de pegar nós com baixa FO, alguns nós com baixo e outros com FO grande
			node_start = random.randint(0,len(G.nodes)-1) 
			ant.visitCity(node_start)
			print("Visita a cidade: {}".format(node_start))
			visited_cnt = 1 # a cidade inicial já foi visitada.
			#Enquanto não visitou todos os vértices, continua visitando:

			while(visited_cnt != max_nodes): 

				#Coleto onde a formiga K está
				print(len(ant.visited),ant.visited[-1])
				v = G.getNode(ant.visited[-1])
				print(" Está no vértice com valor: ", v.value)
				
				#Para cada operacao, verifico a de maior vizinhança

				Ni = [] #Lista de vizinhança, vai possuir uma tupla (state,prob)
				prob_Ni = []

				
				for op in range(ant.op):
					print("Aplicando a operacao {}".format(op))
					vizinho,_id = v.chooseOP(op)
					# print("Vizinho de valor: {}".format(vizinho.value))
					if(vizinho.value >= pow(10,9)):
						continue
					# if(vizinho == v):
					# 	print("Vizinho igual ao vértice atual")
					# 	continue
					# print(vizinhançanho.value)
					if(vizinho.value < best_visited):
						best_visited = vizinho.value
						best_solution = vizinho.Cirurgias.copy()
					G.addNode(vizinho) #Adiciono o nó ao grafo
					G.addEdge( v,op,vizinho,   ) #Adiciono a vizinhança ao grafo

					Ni.append( G.edges[ (v,op,vizinho) ] )

					#A probabilidade de se seguir por aquele vertice, sera dada pelo vetor de probabilidades inicial, onde todos os vertices sao equiprovaveis
					edge = ( v,op,vizinho )
					try:
						prob_Ni.append( ant.probability[edge] )
					except:
						#Todos iniciam com a mesma probabilidade, sendo o numero de operacoes
						ant.probability[edge] = 1.0/ant.op
						prob_Ni.append(ant.probability[edge])
				
				if(len(Ni) == 0):
					break

				if(sum(prob_Ni) != 1):
					idx = np.random.choice(len(Ni),1, p = [1])[0] #Escolho qual aresta seguir.
				else:
					idx = np.random.choice(len(Ni),1, p = prob_Ni)[0] #Escolho qual aresta seguir.
				
				estado_escolhido = G.getEdge( Ni[idx] )[2] #Escolho o estado a ser utilizado

				print(" Tentou ir do vertice: {} com a operacao: {} para o vértice {}".format(v.value, G.getEdge(Ni[idx])[1] ,estado_escolhido.value ))
				
				if( ant.isVisited( G.nodes[estado_escolhido] ) == False ):
					print("Visistou o vértice com valor {}".format(estado_escolhido.value))
					next_v = estado_escolhido
					visited_cnt += 1
			
				#Visito a cidade a partir daquela formiga
				ant.visitCity( G.nodes[next_v] )
				
				ant.addEdge(Ni[idx])


			ant.depositaFeromonio(feromonio,G)
			#Verifica se a rota utilizada pela formiga foi a melhor até o momento
			# print(ant.visited)
			
			value = G.getNode(ant.visited[-1]).value
			
			if(value < best_value):
				best_value = value
				best_rota = ant.edges
			# print("Fim da formiga")
		evaporaFeromonio(feromonio,p,G)

		#Altero a probabilidade de escolher aquela aresta.		
		
		ant.changeProbability(feromonio)

		it += 1

	print("MELHOR VALOR ENCONTRADO: {}".format(best_visited))
	printSolution((best_solution))
main()
