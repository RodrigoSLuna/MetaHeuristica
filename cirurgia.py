import numpy as np
import random







'''
Classe State, indica um estado final da instância de agendamento
Recebe uma lista de Cirurgias, um estado é idêntico ao outro caso as cirurgias foram agendadas
no mesmo instante
'''

def byTC(cirurgia):
	return cirurgia.tc

class State:

	# Recebe como parâmetro uma lista de cirurgias
	def __init__ (self, Cirurgias,value  ):
		self.Cirurgias = Cirurgias
		#Valor da função objetivo
		self.value = value
	def __eq__(self, Other):
		equal = 0
		for cirurgia_x in Cirurgias:
			for cirurgia_y in Other:
				if(cirurgia_x.id == cirurgia_y.id):
					if( !(cirurgia_x.sala == cirurgia_y.sala and cirurgia_x.dia == cirurgia_y.dia and cirurgia_x.semana == cirurgia_y.semana and cirurgia_x.tc_inicio == cirurgia_y.tc_fim and cirurgia_x.cirurgiao == cirurgia_y.cirurgiao) ):					
						return False
		return True

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
			#Assim que encontra o par, procure outro par.
			time_left = cirurgia_x
			swap = []
			
			for cirurgia_y in Cirurgias_sorted:
				if(cirurgia_y.id in id_used or cirurgia_y.id == cirurgia_x.id):
					continue
				if(cirurgia_x.p == cirurgia_y.o and cirurgia_x.w > cirurgia_y.w and cirurgia_x.w and cirurgia_x.e == cirurgia_y.e and time_left >= cirurgia_y.tc):

					#Incluo a condição das cirurgias terem sido adicionados posteriomente
					if(cirurgia_x.dia < cirurgia_y.dia and cirurgia_x.semana <= cirurgia_y.semana):

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
			if(best[key] > bigger ):
				bigger = key

		idx = 0
		for i in range(len(Cirurgias_sorted)):
			if(cirurgia[i].id == best.keys()[0] ):
				idx = i
				break 
		dia = Cirurgias_sorted[idx].dia
		semana = Cirurgias_sorted[idx].semana
		tc_inicio = Cirurgias_sorted[idx].tc_inicio
		tc_fim = Cirurgias_sorted[idx].tc_inicio
		for cirurgia in Cirurgias_sorted:
			for cirurgia_id in best[bigger].values():
				#Faco a substituicao das datas
				if(cirurgia == cirurgia_id):
					cirurgia_id.setTempo(tempo, tempo + cirurgia.tc-1)
					cirurgia_id.setDia(dia)
					cirurgia_id.setSemana(semana)


		#Realizo a troca
		return State(novaCirurgias,FO(Cirurgias_sorted))




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
		penalty += ( cirurgia.dia*cirurgia.semana)*penality[cirurgia.e] + cirurgia.w-1 # Minimo de tempo de espera é 1.
	
	#Inviabilizar cirurgias que não devem ser possíveis de serem realizadas, como por exemplo, mais de 1 especialidade na sala durante aquele dia

	#Identificar cirurgias que foram agendadas no mesmo dia e mesma semana, e que possuem 
	for cirurgia_x in Cirurgias:
		for cirurgia_y in Cirurgias:
			#Garantindo que só irá comparar uma unica vez uma cirurgia de ids diferentes.
			if(cirurgia_x.id == cirurgia_y.id or cirurgia_x < cirurgia_y):
				continue
			if(cirurgia_x.dia == cirurgia_y.dia and cirurgia_x.semana == cirurgia_y.semana and cirurgia_x.e != cirurgia_y.e and cirurgia_x.sala == cirurgia_y.sala):
				penalty +=  100000000  # Penalidade de inviabilizar

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


'''
TODO:
1- Criar a leitura das instancias do problema - 30 Min                            > Ok
2- Verificar se a função gulosa está realizando o agendamento corretamente        > Ok
3- Criar a função que verifica se as cirurgias foram agendadas corretamente       > sem prioridade
4- Criar a função objetivo														  > running
5- Ajustar as formigas para fazerem a alteração do problema
6- 
'''

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


def main():
	Cirurgias = []
	Salas = []
	Cirurgioes = []
	read_instances(Cirurgias,Salas,Cirurgioes)
	check(Cirurgias,Salas,Cirurgioes)
	agendaGreedy(len(Salas),Cirurgias,Salas,Cirurgioes )
	checkConstrains(Cirurgias, Salas, Cirurgioes)
	printSolution(Cirurgias)
	print("Funcao Objetivo: ", FO(Cirurgias))
	# best_rota = []
	# best_value = 10000000000

	# max_iter = 100
	# N = 5
	# alfa = 1
	# beta = 1
	# p = 0.5
	
	# # graph = [[0 for x in range(N)] for y in range(N)]  
	# feromonio = [[1 for x in range(N)] for y in range(N)]  
	
	# # Ants = []
	
	# # for i in range(N):
	# # 	Ants.append( Ant(N,alfa,beta,1) )
	# # 	#Visito a cidade inicial da formiga, escolho de forma aleatória! 
	# # read_graph(N,graph)

	# it = 0
	# best_formiga = None
	# while(it != max_iter):
	# 	for ant in Ants:
	# 		# print("Inicio da formiga")
	# 		ant.clear()
	# 		# print(ant.visited)
	# 		#Para cada inicio, coloca uma formiga em uma cidade aleatória diferente.
	# 		ant.visitCity(random.randint(0,N-1))

	# 		visited_cnt = 1 # a cidade inicial já foi visitada.
	# 		#Enquanto não visitou todos os vértices, continua visitando:
	# 		while(visited_cnt != N):
	# 			#Coleto onde a formiga K está
	# 			v = ant.visited[-1]
	# 			# print(" Está no vértice: ", v)
	# 			#Escolho aleatoriamente a qual vértice ir a partir da probabilidade da formiga K
	# 			#É um vetor de probabilidades 0-N-1, que indica a probabilidade de escolher
	# 			prob = ant.probability[v]

	# 			#Comeco no 
	# 			next_v = v
	# 			while( v == next_v ):
	# 				x = np.random.choice(N,1, p = prob)
	# 				x = x[0] 
	# 				# print(" Tentou ir do vertice: {} para o vértice {}".format(v,x))
	# 				if( ant.isVisited(x) == False ):
	# 					next_v = x
	# 					visited_cnt += 1
				
	# 			#Visito a cidade a partir daquela formiga
	# 			ant.visitCity(next_v)

	# 		ant.depositaFeromonio(feromonio,graph)
	# 		#Verifica se a rota utilizada pela formiga foi a melhor até o momento
	# 		# print(ant.visited)
	# 		value = ant.tamanhoCaminho(graph)
	# 		print(value)
	# 		if(value < best_value):
	# 			best_value = value
	# 			best_rota = ant.visited
	# 		# print("Fim da formiga")
	# 	evaporaFeromonio(feromonio,p,N)
		

	# 	it += 1


main()

