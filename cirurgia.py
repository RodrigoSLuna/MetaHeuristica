import numpy as np
import random



'''
A classe Graph, vai armazenar uma lista de nós e arestas.
Realizará o mapeamento das instâncias State para indices.
E irá mapear as Arestas em indices também. 
'''

#Grafo é direcionado
# class Graph:
# 	def __init__ (self):
# 		self.nodes = {}
# 		self.revNodes = {}
# 		self.edges = {}
# 		self.revEdges = {}
# 		self.nidx = 0
# 		self.eidx = 0

# 	def add_Node(self,s):
# 		if s not in self.nodes.keys():
# 			self.nodes[ s ] = self.nidx
# 			self.revNodes[self.nidx] = s
# 			self.nidx = self.nidx + 1 

# 	#Sao indices, em que as operacoes tambem sao mapeados por indices
# 	def add_Edge(self,s1,op,s2):
# 		e = (s1,op,s2)
# 		if( e not in self.edges.keys()  ):
# 			self.edges[ e ] = self.eidx
# 			self.revEdges[self.eidx] = e
# 			self.eidx = self.eidx + 1

# 	def get_Node(self,idx):
# 		return self.revNodes[idx]
	
# 	def get_Edge(self,idx):
# 		return self.revEdges[idx]

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
	def __init__ (self, Cirurgias,value  ):
		
		self.Cirurgias = Cirurgias.copy()
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
					print("> ",cirurgia_x.dia,cirurgia_y.dia)
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
			return self.op3()

	#Escolhe uma cirurgia de prioridade diferente e adiciona em um outro dia




	#Algoritmo noob
	def op1(self):
		best = {}
		Cirurgias_sorted = self.Cirurgias.copy()
		
		#Inverto o array para procurar as menores.
		Cirurgias_sorted.sort(key = byTC )

		for cirurgia_x in self.Cirurgias:
			if(cirurgia_x.p == 1):
				continue
			#Procuro algua cirurgia idêntica a minha, de mesma prioridade, mas com tempo de espera diferenciado
			#Assim que encontra o par, procure chooseOP

			time_left = cirurgia_x.tc
			swap = []
			
			for cirurgia_y in Cirurgias_sorted:
				# #Procuro apenas salas que não foram agendadas
				# if(cirurgia_y.dia !=  -1 ):
				# 	continue
				if( cirurgia_y.id == cirurgia_x.id):
					continue
				# if(cirurgia_x.p == cirurgia_y.p and cirurgia_x.w > cirurgia_y.w and cirurgia_x.w and cirurgia_x.e == cirurgia_y.e and time_left >= cirurgia_y.tc):
				#Teste
				if( cirurgia_x.w > cirurgia_y.w and cirurgia_x.w and cirurgia_x.e == cirurgia_y.e and time_left >= cirurgia_y.tc):
					# print("Id: ",cirurgia_x.id, " Dia: ",cirurgia_x.dia, " TC ",type(cirurgia_x.tc))
					# print("Id: ",cirurgia_y.id, " Dia: ",cirurgia_y.dia, " TC ",type(cirurgia_y.tc))
					
					#Incluo a condição das cirurgias terem sido adicionados posteriomente
					if(cirurgia_x.dia <= cirurgia_y.dia):

						#Tenho que incluir o tempo 
						if(len(swap) > 0):
							time_left -= (cirurgia_y.tc + 2)
						else:
							#O primeiro a ser adicionado não precisa remover 2 unidades para limpeza da sala, pois já está incluso.
							time_left -= (cirurgia_y.tc)
						swap.append(cirurgia_y.id)

			best[cirurgia_x.id] = swap
		
		bigger = -1

		#Procuro a melhor escolha de troca
		for key in best.keys():
			try:
				# print(key,best[key])	
				if(best[key][0] > bigger ):
					bigger = key
			except:
				pass
		idx = 0
		

		dia = Cirurgias_sorted[idx].dia
		semana = Cirurgias_sorted[idx].semana
		tc_inicio = Cirurgias_sorted[idx].tc_inicio
		tc_fim = Cirurgias_sorted[idx].tc_fim
		for cirurgia in Cirurgias_sorted:
			for cirurgia_id in best[bigger]:
				# print(cirurgia_id)
				#Faco a substituicao das datas
				if(cirurgia == cirurgia_id):
					cirurgia_id.dia = dia
					cirurgia_id.semana = semana
					cirurgia_id.tc_inicio = tc_inicio 
					cirurgia_id.tc_fim    = tc_inicio + cirurgia_id.tc -1

					tc_inicio = cirurgia_id.tc_fim + 3
		
		#Coloco a cirurgia agendada para o grupo de não agendada
		Cirurgias_sorted[idx].dia = -1
		Cirurgias_sorted[idx].semana = -1
		Cirurgias_sorted[idx].tc_inicio = -1
		Cirurgias_sorted[idx].tc_fim = -1
		#Preciso agora achar um espaco para colocar a cirurgia.

		#Realizo a troca
		
		return State(Cirurgias_sorted,FO(Cirurgias_sorted))


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

penality = { 1:90, 2:20,3:5,4:1 }
#Funcao objetivo, dado a entrada da instancia, calcula o valor atual das cirurgias e as suas respectivas datas em que foram agendadas. 
def FO(Cirurgias):
	penalty = 0
	for cirurgia in Cirurgias:
		#Cirurgias que não foram marcadas
		if(cirurgia.dia == -1):
			penalty += (cirurgia.dia)*penality[cirurgia.e] + cirurgia.w # Minimo de tempo de espera é 1.
		else:
			penalty += cirurgia.dia + cirurgia.w

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
		#Heuristica será o Delta: (Quanto se ganha ao utilizar a aresta,  FO(cnj1) - FO(cnj2)  )
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

		#Crio os estados não visitados ainda.	
		vizinhos = []
		for op in range(self.op):
			vizinho = v.chooseOP(op)
			G.addNode(vizinho)
			G.addEdge( G.getNode(self.at),op,vizinho )
			#Se o vértice já foi visitado continua
			if( G.nodes[vizinho] in self.visited):
				continue
			vizinhos.append( (vizinho,op) )

		
			valor_heuristica = self.heuristica(v,vizinho)
			# print("Valor da heuritica: ", valor_heuristica)
			# print("Valor do feromonio: ", feromonio[ self.at ][ G.nodes[vizinho] ][op])

			self.probability[ self.at ][G.nodes[vizinho]][op] = pow(feromonio[ self.at ][ G.nodes[vizinho] ][op],self.alfa)* pow(valor_heuristica,self.beta)
			
			s += self.probability[ self.at ][ G.nodes[vizinho] ][op]

		print("Valor de s ",s)
		#Atualizo a probabilidade de todo mundo viável
		for vizinho,op in vizinhos:
			self.probability[ self.at] [G.nodes[vizinho] ][op] =self.probability[ self.at ][ G.nodes[vizinho]][op]/s

	def depositaFeromonio(self,feromonio):
		lenght = self.tamanhoCaminho()

		for edge in self.edges:
			feromonio[ edge[0]  ][ edge[2] ][ edge[1] ] = self.Q/(lenght*1.0) #Adiciono feromonio no caminho feromonio[i][j][op]

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
	Ants = []
	Cirurgias = []
	Salas = []
	Cirurgioes = []
	read_instances(Cirurgias,Salas,Cirurgioes)
	check(Cirurgias,Salas,Cirurgioes) 
	agendaGreedy(len(Salas),Cirurgias,Salas,Cirurgioes )
	checkConstrains(Cirurgias, Salas, Cirurgioes)
	printSolution(Cirurgias)
	# print("Funcao Objetivo: ", FO(Cirurgias))
	
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

	max_iter = 100
	N = 100
	alfa = 1
	beta = 1
	p = 0.5
	
	# graph = [[0 for x in range(N)] for y in range(N)]  
	feromonio = [[[1 for k in range(1)] for j in range(N)] for i in range(N)] # Feromonio[i][j][op]
	
	
	it = 0
	best_formiga = None
	max_nodes = 10 # Cada formiga irá descobrir 10 nós
	n_formigas = 2


	for i in range(n_formigas):
		Ants.append( Ant(N,1,alfa,beta,1) )

	while(it != max_iter):
		for ant in Ants:
			print("Inicio da formiga")
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
					vizinho = v.chooseOP(op)
					if(vizinho == v):
						print("Vizinho igual ao vértice atual")
						continue
					print(vizinho.value)
					G.addNode(vizinho) #Adiciono o nó ao grafo
					G.addEdge( v,op,vizinho   ) #Adiciono a vizinhança ao grafo

					Ni.append( G.edges[ (v,op,vizinho) ] )

					#A probabilidade de se seguir por aquele vertice, sera dada pelo vetor de probabilidades inicial, onde todos os vertices sao equiprovaveis
					prob_Ni.append( ant.probability[ G.nodes[v] ][ G.nodes[ vizinho ] ][op] )

				if(len(Ni) == 0):
					break
				idx = np.random.choice(len(Ni),1, p = prob_Ni)[0] #Escolho qual aresta seguir.
				
				
				estado_escolhido = G.getEdge(Ni[idx])[2] #Escolho o estado a ser utilizado

				print(" Tentou ir do vertice: {} com a operacao: {} para o vértice {}".format(v.value, G.getEdge(Ni[idx])[1] ,estado_escolhido.value ))
				
				if( ant.isVisited( G.nodes[estado_escolhido] ) == False ):
					print("Visistou o vértice ")
					next_v = estado_escolhido
					visited_cnt += 1
			
				#Visito a cidade a partir daquela formiga
				ant.visitCity( G.nodes[next_v] )
				
				ant.addEdge(Ni[idx])


			ant.depositaFeromonio(feromonio)
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

