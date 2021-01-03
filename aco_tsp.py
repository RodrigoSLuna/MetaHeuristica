import numpy as np
import random

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

