import numpy as np
import random




class Cirurgia:

	def __init__(self,id,p,w,e,h,tc):
		self.id = id
		self.p = p
		self.w = w
		self.e = e
		self.h = h
		self.tc = tc
		self.sala = -1
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
		self.hdia = 24
		self.hsemana = 100

	def novoDia():
		self.hdia = 24
	def novaSemana():
		self.hsemana = 100


class Sala:
	def __init__(self,id):
		self.id = id
		self.disponivel = 0

	#Esse é o tempo que vai estar disponível após a limpeza da sala. no tempo Disponível a sala estará liberada
	#Por isso soma-se 3 unidades, h unidades do uso, + 2 unidades para limpeza, +1 para o tempo de disponibilidade
	def setHora(self, h):
		self.disponivel = h+3

	def novoDia():
		self.disponivel = 0


#Funcao objetivo, dado a entrada da instancia, calcula o valor atual das cirurgias e as suas respectivas datas em que foram agendadas. 
def FO():
	return None

#Funcao verifica se a instancia está dentro do Bloco do Problema. 
def verificaInstancia():
	return None



def agenda(tempo,Cirurgias,Salas,Cirurgioes):
	Cirurgias.sort()


	for s in range(len(Salas)):
		#Se a sala ja foi toda ocupada, nao adianta tentar ocupá-la
		if(Salas[s].disponivel == 46):
			continue

		#Para cada cirurgia, tenta agendar 
		for cirurgia in Cirurgias:


'''Algoritmo que agenda as cirurgias de forma gulosa, dando prioridade a algumas caracteristicas, retorna a configuração final das cirurgias agendadas
Tem como entrada: s- número de salas do problema, a lista com as Cirurgias, Cirurgioes e Salas.
'''
def agendaGreedy(s,Cirurgias,Salas,Cirurgioes ):
	tempo_atual = 1
	dia_atual = 1
	semana_atual = 1
	cirurgias_realizadas = 0

	while( cirurgias_realizadas < len(Cirurgias) ):
		agenda(tempoAtual,Cirurgias,Salas,Cirurgioes)

		tempo_atual+= 1

		#Acabou 
		if(tempo_atual == 46):
			zeraDisponibilidade()
			tempo_atual = 1
			dia_atual += 1
		if(dia_atual==5):
			dial_atual = 1
			semana_atual += 1







	return None
'''
-- Uma formiga deve ser capaz de iniciar a sua busca a partir de uma cidade específica
-- Lembrar de todas as cidades visitadas
-- Armazenar o tamanho do caminho que está seguinte
'''
class Ant:
	# Vai armazenar os vértices já visitados
	
	def __init__(self,N,a,b,q):
		#quantidade de vértices no grafo
		self.alfa = a
		self.beta = b
		self.n = N
		#Construo a funcao de probabilidade da formiga
		self.probability = [[1.0/float(self.n) for x in range(N)] for y in range(N)] 
		self.visited = []
		#Quantidade de feromonio excretada pela formiga
		self.Q = q
	
	def clear(self):
		self.visited = []

	def visitCity(self,i):
		self.visited.append(i)

	def isVisited(self,i):
		if(i in self.visited):
			return True
		return False

	def tamanhoCaminho(self,graph):
		#Percorro o caminho até o vértice inicial, somando os trajetos ao longo do grafo
		#Ao fim do caminho, percorre o inverso no grafo, dado a lista de visitados para que possa
		lenght = 0.0
		last = len(self.visited)-1
		print()
		for i in range(last,0,-1):
			print('i: ', i)
			print("Vertice ", self.visited[i], " Vertice " ,self.visited[i-1])
			lenght += graph[ self.visited[i] ][ self.visited[i-1] ]

		#No ultimo cara ele tem que voltar pro primeiro
		print(self.visited[-1], self.visited[0])
		lenght += graph[ self.visited[ -1 ] ][ self.visited[0] ]	
		return lenght


	def heuristica(i,j,graph):
		return 1.0/graph[i][j]




	def changeProbability(feromonio,graph):
		#Pego a posicao da formiga
		self.at = visited[-1]

		#Para cada vértice não visitado, verifico o valor de transição e monto a tabela de probabilidade
		#
		s = 0 #Soma de todas as probabilidades
		for i in range(self.n):
			#Se o vértice já foi visitado continua
			if(i in visited):
				continue

			self.probability[at][i] = pow(feromonio[at][i],self.alfa)* pow(self.heuristica(at,i,graph),self.beta)
			s += self.probability[at][i]

		#Atualizo a probabilidade de todo mundo viável
		for i in range(self.n):
			if(i in visited):
				continue
			self.probability[at][i] =self.probability[at][i]/s

	def depositaFeromonio(self,feromonio,graph):
		lenght = self.tamanhoCaminho(graph)

		for i in range( len(self.visited) -1 ):
			feromonio[ self.visited[i]  ][ self.visited[i+1] ] = self.Q/(lenght*1.0)


def evaporaFeromonio(feromonio,p,N):
	for i in range(N):
		for j in range(N):
			feromonio[i][j] = feromonio[i][j]*(1-p)



def read_graph(N,graph):
	
	for i in range(N):
		x = input().split(" ")
		for j in range(N):
			graph[i][j] = float(x[j])






def main():
	best_rota = []
	best_value = 10000000000

	max_iter = 100
	N = 5
	alfa = 1
	beta = 1
	p = 0.5
	graph = [[0 for x in range(N)] for y in range(N)]  
	feromonio = [[1 for x in range(N)] for y in range(N)]  
	
	Ants = []
	
	for i in range(N):
		Ants.append( Ant(N,alfa,beta,1) )
		#Visito a cidade inicial da formiga, escolho de forma aleatória! 
	read_graph(N,graph)

	it = 0
	best_formiga = None
	while(it != max_iter):
		for ant in Ants:
			# print("Inicio da formiga")
			ant.clear()
			# print(ant.visited)
			#Para cada inicio, coloca uma formiga em uma cidade aleatória diferente.
			ant.visitCity(random.randint(0,N-1))

			visited_cnt = 1 # a cidade inicial já foi visitada.
			#Enquanto não visitou todos os vértices, continua visitando:
			while(visited_cnt != N):
				#Coleto onde a formiga K está
				v = ant.visited[-1]
				# print(" Está no vértice: ", v)
				#Escolho aleatoriamente a qual vértice ir a partir da probabilidade da formiga K
				#É um vetor de probabilidades 0-N-1, que indica a probabilidade de escolher
				prob = ant.probability[v]

				#Comeco no 
				next_v = v
				while( v == next_v ):
					x = np.random.choice(N,1, p = prob)
					x = x[0] 
					# print(" Tentou ir do vertice: {} para o vértice {}".format(v,x))
					if( ant.isVisited(x) == False ):
						next_v = x
						visited_cnt += 1
				
				#Visito a cidade a partir daquela formiga
				ant.visitCity(next_v)

			ant.depositaFeromonio(feromonio,graph)
			#Verifica se a rota utilizada pela formiga foi a melhor até o momento
			# print(ant.visited)
			value = ant.tamanhoCaminho(graph)
			print(value)
			if(value < best_value):
				best_value = value
				best_rota = ant.visited
			# print("Fim da formiga")
		evaporaFeromonio(feromonio,p,N)
		

		it += 1


main()

