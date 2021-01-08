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
	def addEdge(self,s1,op,s2,id):
		e = (s1,op,s2,id)
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
					print("cirurgia_x_id: {} agendada no dia {} ".format(cirurgia_x.id,cirurgia_x.dia))
					print("cirurgia_y_id: {} agendada no dia {} ".format(cirurgia_y.id,cirurgia_y.dia))
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
						if(cirurgia.dia == dia and (cirurgia.tc_inicio == tc or cirurgia.tc_fim-2 == tc ) and cirurgia.sala == sala.id):
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
						if(value > 0):
							tempos_d[ (value,qt_f) ] = ( dia, sala.id, tc )
							qt_f += 1
				tc+=1
			dia += 1
		
		#Após ter todos os tempos disponveis, verificamos quais cirurgias podem ser agendadas
		#A restrição do problema para cirurgias que não possam ser agendadas, será penalizada na funcao FO.
		#A adição é feita no tempo correto, no entanto, para verificar se a sala/cirurgiao possam ser utilizados, será verificado em um próximo momento
		#Procuro as cirurgias que possam ser agendadas com o tempo
		print(tempos_d)
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

		print("Agendamento da cirurgia: {}".format(select_id))
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
		self.inicio = inicio
		self.fim = inicio+self.tc -1
		
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

lp = { 1:1, 2:5,3:10,4:50 }
fp = { 1:90 , 2:20, 3:5, 4:1 }
#Funcao objetivo, dado a entrada da instancia, calcula o valor atual das cirurgias e as suas respectivas datas em que foram agendadas. 
def FO(Cirurgias):
	penalty = 0
	for cirurgia in Cirurgias:
		vc = 0
		xcstd = 0
		zc = 0
		p1 = 0
		if(cirurgia.dia == -1):
			zc = 1
		else:
			xcstd = 1

		if(cirurgia.dia + cirurgia.w >= lp[ cirurgia.p ]):
			vc = 1

		if(cirurgia.p == 1 and cirurgia.dia > 1):
			p1 = 1

		penalty += 10*( pow(cirurgia.w +2, cirurgia.dia) )*p1

		if(cirurgia.dia != -1):
			penalty += ( pow(cirurgia.w +2 + cirurgia.dia, 2) + pow( cirurgia.w + 2 + cirurgia.dia - lp[cirurgia.dia],2 )*vc ) * xcstd
			penalty += ( pow( cirurgia.w + 7 ,2)*fp[cirurgia.p] +  fp[cirurgia.p]*vc*( pow(cirurgia.w +9 - lp[cirurgia.p],2) )) * zc

	return penalty

'''
TODO
- Verificar se os cirurgoes obedecam as constrains
- Verificar se as salas obedecam as constrains
'''

#Funcao verifica se a instancia está dentro do Bloco do Problema. 
def verificaInstancia():

	for cirurgia_x in Cirurgias:
		for cirurgia_y in Cirurgias:
			#Garantindo que só irá comparar uma unica vez uma cirurgia de ids diferentes.
			if(cirurgia_x.id == cirurgia_y.id or cirurgia_x < cirurgia_y):
				continue
			if(cirurgia_x.dia == cirurgia_y.dia and cirurgia_x.semana == cirurgia_y.semana and cirurgia_x.e != cirurgia_y.e and cirurgia_x.sala == cirurgia_y.sala):
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
							cirurgiao.utilizaCirurgiao(cirurgia.cirurgiao)
							
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
		self.probability = [[[1.0/float(self.op) for x in range(op)] for x in range(N)] for y in range(N)] 
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
		return len(self.edges)


	def heuristica(self,vi,vj):
		#Heuristica será o Delta: (Quanto se ganha ao utilizar a aresta,   FO(cnj2) - FO(cnj1)
		return vj.value - vi.value


	def changeProbability(self,feromonio):
		#Pego a posicao da formiga
		self.at = self.visited[-1] #Estou no último vértice

		#Para cada vértice não visitado, verifico o valor de transição e monto a tabela de probabilidade
		#
		s = 0 #Soma de todas as probabilidades
		
		#A probabilidade será: Pi,j * Pk ( Prob de ir do vértice i ao vértice j utilizando Kth operacao)
		print(self.at)
		v = G.getNode(self.at)


		#Gera a vizinhança do Estado Atual
		#Crio os estados não visitados ainda.	
		vizinhos = []
		for op in range(self.op):
			vizinho,_id = v.chooseOP(op)
			G.addNode(vizinho)
			G.addEdge( G.getNode(self.at),op,vizinho,_id )
			#Se o vértice já foi visitado continua
			if( G.nodes[vizinho] in self.visited):
				continue
			vizinhos.append( (vizinho,op,_id) )

		
			valor_heuristica = self.heuristica(v,vizinho)
			# print("Valor da heuritica: ", valor_heuristica)
			# print("Valor do feromonio: ", feromonio[ self.at ][ G.nodes[vizinho] ][op])

			self.probability[ self.at ][G.nodes[vizinho]][op] = pow(feromonio[ self.at ][ G.nodes[vizinho] ][op],self.alfa)* pow(valor_heuristica,self.beta)
			
			s += self.probability[ self.at ][ G.nodes[vizinho] ][op]

		#Atualizo a probabilidade de todo mundo viável
		for vizinho,op,id_ in vizinhos:
			self.probability[ self.at] [G.nodes[vizinho] ][op] =self.probability[ self.at ][ G.nodes[vizinho]][op]/s

	def depositaFeromonio(self,feromonio,graph):
		lenght = self.tamanhoCaminho()

		for edge in self.edges:
			
			e = graph.getEdge(edge)
			feromonio[ graph.nodes[e[0]]  ][ graph.nodes[e[2]] ][ e[1] ] = self.Q/(lenght*1.0) #Adiciono feromonio no caminho feromonio[i][j][op]

def evaporaFeromonio(feromonio,p,N,op):
	for i in range(N):
		for j in range(N):
			for k in range(op): 
				feromonio[i][j][k] = feromonio[i][j][k]*(1-p)




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
		print("Id: ", cirurgia.id, " Prioridade: ", cirurgia.p , " Especialidade: ",cirurgia.e ,  " sala: " , cirurgia.sala, " dia: ", cirurgia.dia, " semana "  ,cirurgia.semana, " Inicio ", cirurgia.tc_inicio, " Fim ", cirurgia.tc_fim )



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
1- Criar a leitura das instancias do problema - 30 Min                            > Ok
2- Verificar se a função gulosa está realizando o agendamento corretamente        > Ok
3- Criar a função que verifica se as cirurgias foram agendadas corretamente       > Sem prioridade
4- Alterar a função objetivo													  > Alterar a função objetivo
5- Ajustar as formigas para fazerem a alteração do Problema                       > Ok ( Falta verificar se está tudo certo. )
6- Criar e ajustar funções de de geração de vizinhança							  > Fazer
7- Testar se o algoritmo está funcionando corretamente                            > Fazer
8- Realizar Melhorias                                                             > Fazer
9- Otimizar                                                                       > Inumeras funcoes podem ser otimizadas. 
'''



def main():
	
	read_instances(Cirurgias,Salas,Cirurgioes)
	check(Cirurgias,Salas,Cirurgioes) 
	agendaGreedy(len(Salas),Cirurgias,Salas,Cirurgioes )
	checkConstrains(Cirurgias, Salas, Cirurgioes)
	printSolution(Cirurgias)
	print("Funcao Objetivo: ", FO(Cirurgias))
	
	'''
		Inicio da Heurística
	'''
	s1 = State(Cirurgias,FO(Cirurgias))
	global G,feromonio
	G = Graph()
	
	#Nó inicial das formigas
	G.addNode(s1)		

	#Inicialmente todas as formigas iniciam a sua busca no nó 0, que é o da solução gulosa

	best_rota = []
	best_value = 10000000000

	max_iter = 1
	N = 100
	alfa = 1
	beta = 1
	p = 0.5
	
	# graph = [[0 for x in range(N)] for y in range(N)]  
	feromonio = [[[1 for k in range(10)] for j in range(N)] for i in range(N)] # Feromonio[i][j][op]
	
	
	it = 0
	best_formiga = None
	max_nodes = 10 # Cada formiga irá descobrir 10 nós
	n_formigas = 2


	for i in range(n_formigas):
		Ants.append( Ant(N,2,alfa,beta,1) )
	f = 0
	while(it != max_iter):
		for ant in Ants:
			print("Inicio da formiga id {}".format(f%n_formigas))
			f += 1
			ant.clear()
			
			#Para cada inicio, coloca uma formiga em uma cidade aleatória diferente.
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

				print("Aplicando a operacao")
				for op in range(ant.op):
					print(op)
					vizinho,_id = v.chooseOP(op)
					print("Vizinho de valor: {}".format(vizinho.value))
					# if(vizinho == v):
					# 	print("Vizinho igual ao vértice atual")
					# 	continue
					# print(vizinhançanho.value)
					G.addNode(vizinho) #Adiciono o nó ao grafo
					G.addEdge( v,op,vizinho, _id  ) #Adiciono a vizinhança ao grafo

					Ni.append( G.edges[ (v,op,vizinho,_id) ] )

					#A probabilidade de se seguir por aquele vertice, sera dada pelo vetor de probabilidades inicial, onde todos os vertices sao equiprovaveis
					prob_Ni.append( ant.probability[ G.nodes[v] ][ G.nodes[ vizinho ] ][op] )

				if(len(Ni) == 0):
					break

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
		evaporaFeromonio(feromonio,p,N,op)

		#Altero a probabilidade de escolher aquela aresta.		
		
		ant.changeProbability(feromonio)

		it += 1


main()

