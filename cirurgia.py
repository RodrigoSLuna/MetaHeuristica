import numpy as np
import random
import copy
import time
import glob
import statistics as stat

# Variáveis globais
from typing import List

'''
Classe State, indica um estado final da instância de agendamento
Recebe uma lista de Cirurgias, um estado é idêntico ao outro caso as cirurgias foram agendadas
no mesmo instante
'''


def byTC(cirurgia):
    return cirurgia.tc

# Grafo é direcionado
class Graph:
    def __init__(self):
        self.nodes = {}
        self.revNodes = {}
        self.edges = {}
        self.revEdges = {}
        self.nidx = 0
        self.eidx = 0

    def addNode(self, s):
        if s not in self.nodes.keys():
            self.nodes[s] = self.nidx
            self.revNodes[self.nidx] = s
            self.nidx = self.nidx + 1

    # Sao indices, em que as operacoes tambem sao mapeados por indices
    def addEdge(self, s1, op, s2):
        e = (s1, op, s2)
        if (e not in self.edges.keys()):
            self.edges[e] = self.eidx
            self.revEdges[self.eidx] = e
            self.eidx = self.eidx + 1

    def getNode(self, idx):
        return self.revNodes[idx]

    def getEdge(self, idx):
        return self.revEdges[idx]

    def showNodes(self):
        print("Nodes")
        for node in self.nodes.keys():
            print(node.lst)

    def showEdges(self):
        print("Edges")
        for edge in self.edges.keys():
            print("Node 1")
            for cirurgia in edge[0].Cirurgias:
                print(cirurgia.id, cirurgia.dia)

            print("Operation: ", edge[1])
            print("Node 2")
            for cirurgia in edge[2].Cirurgias:
                print(cirurgia.id, cirurgia.dia)


def remove_surgery_by_id(surgeries_copy, surgery_id):
    for surgery_copy in surgeries_copy:
        # Desagenda a cirurgia.
        if surgery_copy.id == surgery_id:
            surgery_copy.remove()
            break


class State:
    # Recebe como parâmetro uma lista de cirurgias
    id_agendadas = []
    n_agendadas = []

    def __init__(self, Cirurgias, Salas, value):
        self.Cirurgias = copy.deepcopy(Cirurgias)
        for cirurgia in Cirurgias:
            if (cirurgia.dia != -1):
                self.id_agendadas.append(cirurgia.id)
            else:
                self.n_agendadas.append(cirurgia.id)
        # Valor da função objetivo
        self.Salas = Salas
        self.value = value

    def __hash__(self):
        return hash(tuple(self.Cirurgias))

    # Uma cirurgia é diferente de outra, caso exista alguma cirurgia agendada de forma diferente.
    def __eq__(self, Other):
        # if(self.value != Other.value):
        # 	return False
        for cirurgia_x in self.Cirurgias:
            for cirurgia_y in Other.Cirurgias:

                if (cirurgia_x.id == cirurgia_y.id):
                    # print("cirurgia_x_id: {} agendada no dia {} ".format(cirurgia_x.id,cirurgia_x.dia))
                    # print("cirurgia_y_id: {} agendada no dia {} ".format(cirurgia_y.id,cirurgia_y.dia))
                    if (
                            (cirurgia_x.sala != cirurgia_y.sala
                             or cirurgia_x.dia != cirurgia_y.dia
                             or cirurgia_x.semana != cirurgia_y.semana
                             or cirurgia_x.tc_inicio != cirurgia_y.tc_inicio
                             or cirurgia_x.tc_fim != cirurgia_y.tc_fim
                             or cirurgia_x.cirurgiao != cirurgia_y.cirurgiao)):
                        return False

        return True

    def __gt__(self, other):
        if self.value > other.value:
            return True

    def chooseOP(self, op):
        if op == 1:
            return self.op1()
        elif op == 2:
            return self.op2()
        elif op == 3:
            return self.op3()
        elif op == 4:
            return self.op4()

    def pick_surgery_to_remove(self):
        surgery_id = None
        lowest_FO = pow(10, 14)

        for surgery in self.Cirurgias:
            if surgery.dia == -1:
                continue
            surgeries_copy = copy.deepcopy(self.Cirurgias)
            remove_surgery_by_id(surgeries_copy, surgery.id)

            fo_result = FO(surgeries_copy)
            if fo_result < lowest_FO:
                lowest_FO = fo_result
                surgery_id = surgery.id

        return surgery_id

    def op4(self):
        schedulable_surgeries, tempos_d = self.look_for_schedulable_surgeries()

        lowest_fo = pow(10, 9)
        best_surgery_id = -1
        best_surgery_final_state = copy.deepcopy(self.Cirurgias)

        for schedulable_surgery in schedulable_surgeries:
            surgery_id, dia, sala, inicio = schedulable_surgery
            surgeries_copy = copy.deepcopy(self.Cirurgias)
            for surgery in surgeries_copy:
                if surgery.id != surgery_id:
                    continue
                surgery.add(dia, sala, inicio)
                # print("Adicinou a cirugia {} no dia {} na sala {} com inicio em {}".format(surgery_id,dia,sala,inicio))
                fo_result = FO(surgeries_copy)
                if fo_result < lowest_fo:
                    lowest_fo = fo_result
                    best_surgery_id = surgery.id
                    best_surgery_final_state = surgeries_copy

        return State(best_surgery_final_state, copy.deepcopy(self.Salas),
                     lowest_fo), best_surgery_id

    def op3(self):
        id_ = self.pick_surgery_to_remove()
        # print("Cirurgia id: {} desagendada".format(id_))
        New_Cirurgias = copy.deepcopy(self.Cirurgias)
        remove_surgery_by_id(New_Cirurgias, id_)
        # for cirurgia in New_Cirurgias:
        #     if(cirurgia.id == id_):
        #         print(cirurgia.dia,cirurgia.sala,cirurgia.tc_inicio,cirurgia.tc_fim)
        #         break
        return State(New_Cirurgias, copy.deepcopy(self.Salas),
                     FO(New_Cirurgias)), id_

    # E1 < Remove > Ex
    # Esta operacao remove uma cirurgia agendada aleatoriamente, de acordo com a probabilidade de prioridade
    # Prioridades 1 tem baixa probalidade de ser excluída
    #
    def op2(self):
        # Seleciona a cirurgia a ser removida
        New_Cirurgias = copy.deepcopy(self.Cirurgias)

        id_ = random.choice(self.id_agendadas)
        # print("Cirurgia id: {} desagendada".format(id_))
        remove_surgery_by_id(New_Cirurgias, id_)

        return State(New_Cirurgias, copy.deepcopy(self.Salas),
                     FO(New_Cirurgias)), id_

    # Adiciona uma cirurgia aleatória
    # Começa com um

    def op1(self):
        pos_cirurgia, tempos_d = self.look_for_schedulable_surgeries()

        # Coleto cirurgias randômicas
        try:
            select_id = random.choice(pos_cirurgia)
        except:
            select_id = -1
        # Crio um novo estado para a cirurgia
        New_Cirurgias = copy.deepcopy(self.Cirurgias)

        # Verifico se pode ser adicionado essa cirurgia, caso ao contrário nao adicione.
        # Adiciono a cirurgia no dia X,no tempo Y, com inicio TC

        if select_id != -1:
            cirurgia_id, dia, sala_id, inicio = select_id
            for cirurgia in New_Cirurgias:
                if (cirurgia.id == cirurgia_id):
                    cirurgia.add(dia, sala_id, inicio)

        # print("Agendamento da cirurgia: {}".format(select_id))
        return State(New_Cirurgias, copy.deepcopy(self.Salas),
                     FO(New_Cirurgias)), select_id

    def look_for_schedulable_surgeries(self):
        # Procura os tempos em que as cirurgias podem ser adicionadas

        tempos_d = {}
        dia = 1
        tc = 1
        qt_f = 1
        while (dia <= 5):
            while (tc <= 46):
                for sala in self.Salas:
                    found = False
                    for cirurgia in self.Cirurgias:
                        # é levado em consideração a limpeza da sala.
                        # Se a cirurgia finaizou 2 tcs atrás, esse tc não é disponível, pois é da limpeza
                        # Se estou dentro de um intervalo, entao esse tempo é inútil
                        if (cirurgia.dia == dia and (
                                cirurgia.tc_inicio <= tc and cirurgia.tc_fim + 2 >= tc) and cirurgia.sala == sala.id):
                            found = True
                            break
                    # caso não tenha encontrado ninguém nessa situação, é possível agendar alguem nesse tempo
                    # procura o proximo tempo fim.
                    if (found == False):
                        tc_fim = tc + 1
                        while (tc_fim <= 46):
                            found_end = False
                            for cirurgia in self.Cirurgias:
                                if ( cirurgia.dia == dia and cirurgia.tc_inicio == tc_fim and cirurgia.sala == sala.id):
                                    found_end = True
                                    break
                            if (found_end):
                                break
                            tc_fim += 1
                        # Tempo anterior que é o correto
                        tc_fim -= 1
                        # #Contabiliza o tempo junto com a limepza, caso for a ultima cirurgia, deixa ela sem a limpeza
                        # if(tc == 44 and tc_fim == 46 ):
                        if (tc_fim != 46):
                            tc_fim -= 2
                        value = tc_fim - tc + 1
                        # t[(tempo_disponivel,id)] = ( dia,sala.id, tc )
                        if (value > 0 and tc_fim > 0):
                            tempos_d[(value, qt_f)] = (dia, sala.id, tc)
                            qt_f += 1
                tc += 1
            dia += 1
        # Após ter todos os tempos disponveis, verificamos quais cirurgias podem ser agendadas
        # A restrição do problema para cirurgias que não possam ser agendadas, será penalizada na funcao FO.
        # A adição é feita no tempo correto, no entanto, para verificar se a sala/cirurgiao possam ser utilizados, será verificado em um próximo momento
        # Procuro as cirurgias que possam ser agendadas com o tempo
        # print(tempos_d)
        # Garantir escopo de viabiliade ( Cirurgia só é possível caso Cirurgiao e Sala possam realizá-la)
        pos_cirurgia = []
        for wc, _id in tempos_d.keys():
            dia, sala_id, inicio = tempos_d[(wc, _id)]
            for cirurgia in self.Cirurgias:
                teste_sala = False
                teste_cirurgiao = False

                # Se a cirurgia não está agendada
                if (cirurgia.dia == -1):
                    # Se o tempo para a conclusão daquela cirurgia for menor ou igual ao tempo disponível. Selecione
                    if (cirurgia.tc <= wc):
                        # print("Tentando adicionar a cirurgia id {} com a especialidade {}".format(cirurgia.id,cirurgia.e))
                        cirurgiao_hora = 0
                        cirurgiao_semana = 0
                        for cirurgia_x in self.Cirurgias:
                            # Caso a cirurgia esteja desagendada
                            if (cirurgia_x.dia == -1):
                                continue

                                # Existe alguma cirurgia escalonada nesta sala
                            # Caso ja haja uma cirurgia nesta sala e a especialidade seja diferente, sala é inválida
                            if (
                                    cirurgia_x.dia == dia and cirurgia_x.sala == sala_id and cirurgia_x.e != cirurgia.e):
                                # Cirurgia que esta tentando adicionar anqeula sala tem especialidade diferente
                                teste_sala = True

                            # Verifico se o meu cirurgiao esta ou nao ocupado no momento do atendimento
                            if (cirurgia_x.cirurgiao == cirurgia.cirurgiao):
                                inicio_x = cirurgia_x.tc_inicio
                                fim_x = cirurgia_x.tc_fim + 2

                                fim = cirurgia.tc + inicio + 2  # Contabilizo o tempo que o cirurgiao vai precisar para poder iniciar uma outra cirurgia tb

                                if (not (inicio > fim_x or fim < inicio_x)):
                                    teste_cirurgiao = True
                            # Utilizam os mesmos cirurgioes
                            if (
                                    cirurgia_x.dia == dia and cirurgia.cirurgiao == cirurgia_x.cirurgiao):
                                cirurgiao_hora += cirurgia_x.tc_fim - cirurgia_x.tc_inicio + 1 + 2
                                cirurgiao_semana += cirurgia_x.tc_fim - cirurgia_x.tc_inicio + 1 + 2
                            elif (
                                    cirurgia_x.dia != dia and cirurgia.cirurgiao == cirurgia_x.cirurgiao):
                                cirurgiao_semana += cirurgia_x.tc_fim - cirurgia_x.tc_inicio + 1 + 2

                        # Possiveis ids de cirurgias que possam ser agendadas
                        if (
                                cirurgiao_hora + cirurgia.tc + 2 > 24 or cirurgiao_hora + cirurgia.tc + 2 > 100):
                            teste_cirurgiao = True
                        if (teste_sala == False and teste_cirurgiao == False):
                            if ((cirurgia.id, dia, sala_id,
                                 inicio) not in pos_cirurgia):
                                # Armazeno o dia, a sala e o tempo em que posso adicionar essa cirurgia
                                pos_cirurgia.append(
                                    (cirurgia.id, dia, sala_id, inicio))
        return pos_cirurgia, tempos_d


class Cirurgia:

    def __init__(self, id, p, w, e, h, tc):
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

    # Overloading do
    # def __gt__(self, other):
    #     if (self.p < other.p):
    #         return True
    #     elif (self.p == other.p):
    #         if (self.w < other.w):
    #             return True
    #         elif (self.tc <= other.tc):
    #             return True
    #     return False

    def __lt__(self, other):
        if self.p < other.p:
            return True
        elif self.p == other.p:
            if self.w > other.w:
                return True
            elif self.tc >= other.tc:
                return True
        return False

    def add(self, dia, sala, inicio):
        self.dia = dia
        self.sala = sala
        self.tc_inicio = inicio
        self.tc_fim = inicio + self.tc - 1

    def remove(self):
        self.dia = -1
        self.sala = -1
        self.tc_inicio = -1
        self.tc_fim = -1
        self.semana = -1

    def setSala(self, s):
        self.sala = s

    def setDia(self, d):
        self.dia = d

    def setSemana(self, s):
        self.semana = s

    # Inicio da cirurgia e fim da cirurgia, inclusive
    def setTempo(self, a, b):
        self.tc_inicio = a
        self.tc_fim = b

    def setCirurgiao(self, cir):
        self.cirurgiao = cir


class Cirurgiao:

    def __init__(self, id, especialidade):
        self.id = id
        self.e = especialidade
        self.hdia = 0
        self.hsemana = 0
        self.inicio = -1
        self.fim = -1
        self.dias = {}

    def utilizaCirurgiao(self, h, dia, inicio, fim):
        self.hdia += h
        self.hsemana += h
        self.inicio = inicio
        self.fim = fim
        try:
            self.dias[dia].append(self.inicio, self.fim)
        except:
            lst = []
            lst.append((self.inicio, self.fim))
            self.dias[dia] = lst

    def desocupa(self, dia, inicio, fim):
        self.dias[dia].remove((inicio, fim))

    def novoDia(self):
        self.hdia = 0
        self.especialidade = -1
        self.inicio = -1
        self.fim = -1

    def novaSemana(self):
        self.hsemana = 0


class Sala:
    def __init__(self, id):
        self.id = id
        self.disponivel = 1
        self.especialidade = -1
        self.dias = {}

    # Esse é o tempo que vai estar disponível após a limpeza da sala. no tempo Disponível a sala estará liberada
    # Por isso soma-se 3 unidades, h unidades do uso, + 2 unidades para limpeza, +1 para o tempo de disponibilidade
    def setEspecialidade(self, dia, e, cirurgia_id):
        self.especialidade = e
        try:
            self.dias[dia] = (cirurgia_id, e)
        except:
            lst = []
            lst.append((cirurgia_id, e))
            self.dias[dia] = lst

    def removeEspecialidade(self, dia, cirurgia_id, e):
        self.dias[dia].remove((cirurgia_id, e))

    def setHora(self, h):
        self.disponivel = h + 3

    def novoDia(self):
        self.disponivel = 1
        self.especialidade = -1


lp = {1: 3, 2: 15, 3: 60, 4: 365}
fp = {1: 90, 2: 20, 3: 8, 4: 1}

# Necessário checar se essa FO está CORRETA !
# (Toy2 está com uma solução diferente Para 2 salas. Checar se a solução está CORRETA)

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

    for cirurgia in Cirurgias:
        last = penalty
        vc = 0
        xcstd = 0
        zc = 0
        p1 = 0
        if (
                cirurgia.dia == -1 or cirurgia.tc_inicio == -1 or cirurgia.tc_fim == -1):
            zc = 1
        else:
            xcstd = 1

        if (cirurgia.dia + cirurgia.w >= lp[cirurgia.p] or (
                cirurgia.dia == -1 and 7 + cirurgia.w >= lp[cirurgia.p])):
            vc = 1

        if (cirurgia.p == 1 and (cirurgia.dia > 1 or cirurgia.dia == -1)):
            p1 = 1

        penalty += (pow(10 * (cirurgia.w + 2),
                        cirurgia.dia if cirurgia.dia != -1 else 7)) * p1

        # if(cirurgia.id == 1):
        # print("VC VC VC VC VC {} dia {}".format(vc,cirurgia.dia))
        if (cirurgia.dia != -1):
            penalty += (pow(cirurgia.w + 2 + cirurgia.dia, 2) + pow(
                cirurgia.w + 2 + cirurgia.dia - lp[cirurgia.p],
                2) * vc) * xcstd
        else:
            penalty += (pow(cirurgia.w + 7, 2) * fp[cirurgia.p] + fp[
                cirurgia.p] * vc * (
                            pow(cirurgia.w + 9 - lp[cirurgia.p], 2))) * zc
        # print("Cirugia {} escalonada".format("nao" if cirurgia.dia == -1 else "" ))
        # print("Cirurgia id {} igual a {}".format(cirurgia.id,penalty-last))
        # print("\n")
    return penalty


'''
TODO
- Verificar se os cirurgoes obedecam as constrains
- Verificar se as salas obedecam as constrains
'''


# Funcao verifica se a instancia está dentro do Bloco do Problema.
def verificaInstancia(Cirurgias, Salas):
    # Verifica se todos que estão na mesma sala, possuem a mesma
    dia = 1
    while (dia <= 5):
        esp_sala = {}
        for sala in Salas:
            for cirurgia in Cirurgias:
                if (cirurgia.dia == dia and cirurgia.sala == sala.id):
                    if (sala.id in esp_sala.keys()):
                        if (esp_sala[sala.id] != cirurgia.e):
                            # print("SALA {} COM CIRURGIA DIFERENTE !!!! ".format(sala.id))
                            return False
                    else:
                        esp_sala[sala.id] = cirurgia.e

        dia += 1

    # Verifica se o cirurgiao esta cumprindo o trabalho de 24 horas por dia e 100 horas por semana.
    tempo_gasto_semana = {}

    dia = 1
    while (dia <= 5):
        tempo_gasto_dia = {}
        for cirurgia in Cirurgias:
            if (cirurgia.id != -1 and cirurgia.dia == dia):
                try:
                    tempo_gasto_semana[cirurgia.cirurgiao] += cirurgia.tc
                except:
                    tempo_gasto_semana[cirurgia.cirurgiao] = cirurgia.tc

                try:
                    tempo_gasto_dia[cirurgia.cirurgiao] += cirurgia.tc
                except:
                    tempo_gasto_dia[cirurgia.cirurgiao] = cirurgia.tc
        for key in tempo_gasto_dia:
            if (tempo_gasto_dia[key] > 24):
                # print("Cirurgiao {} EXCEDEU DIA".format(key))
                return False
        dia += 1
    for key in tempo_gasto_semana:
        if (tempo_gasto_semana[key] > 100):
            # print("Cirurgiao {} EXCEDEU SEMANA".format(key))
            return False

    return True


# A sala tem especialidade
def agenda(tempo, dia, semana, Cirurgias, Salas, Cirurgioes):
    cnt = 0

    for s in range(len(Salas)):
        for tempo in range(1, 47):
            # Se a sala ja foi toda ocupada, nao adianta tentar ocupá-la
            if (Salas[s].disponivel == 46):
                continue
            if (Salas[s].disponivel > tempo):
                continue
            # print(Salas[s].disponivel, tempo)
            # Para cada cirurgia, tenta agendar
            for cirurgia in Cirurgias:
                if (cirurgia.sala != -1):
                    continue
                # Se sou uma cirurgia que posso ser agendada nessa sala, mas nao posso ser agendada no momento, aguardo para poder sera Agendada nessa sala
                if (Salas[s].especialidade == cirurgia.e and Salas[
                    s].disponivel + cirurgia.tc - 1 <= 46 and Salas[
                    s].disponivel > tempo):
                    continue

                # Há tempo disponível para agendar essa cirurgia
                # print(tempo,Salas[s].disponivel, Salas[s].disponivel + cirurgia.tc)
                if ((Salas[s].especialidade == -1 or Salas[
                    s].especialidade == cirurgia.e) and tempo == Salas[
                    s].disponivel and tempo + cirurgia.tc - 1 <= 46):
                    # Verifico se o cirurgiao requerido para essa cirurgia pode faze-la
                    for cirurgiao in Cirurgioes:
                        if (
                                cirurgiao.id == cirurgia.cirurgiao and 
                                cirurgiao.hdia + cirurgia.tc <= 24 and 
                                cirurgiao.hsemana + cirurgia.tc <= 100
                                ):
                            if ((
                                    cirurgiao.inicio == -1) or tempo > cirurgiao.fim):
                                # Configuro o cirurgiao
                                # print("Cirurgiao :{}, com tempo utilizado {} no tempo inicio {} ate o fim {} no dia {} usou {} ".format(cirurgiao.id,cirurgiao.hdia,tempo,cirurgia.tc+tempo-1,dia,cirurgia.tc))
                                cirurgiao.utilizaCirurgiao(cirurgia.tc + 2, dia,
                                                           tempo, (
                                                                       cirurgia.tc + tempo - 1) + 2)
                                # print("Cirurgiao :{}, com tempo utilizado {} no tempo inicio {} ate o fim {} no dia {} usou {} ".format(cirurgiao.id,cirurgiao.hdia,tempo,cirurgia.tc+tempo-1,dia,cirurgia.tc))
                                # print("---------")
                                # Configuro a cirurgia
                                cirurgia.setCirurgiao(cirurgiao.id)
                                cirurgia.setTempo(tempo,
                                                  tempo + cirurgia.tc - 1)
                                cirurgia.setDia(dia)
                                cirurgia.setSemana(semana)

                                # Utilizo a sala
                                Salas[s].setEspecialidade(dia, cirurgia.e,
                                                          cirurgia.id)
                                cirurgia.setSala(s)
                                Salas[s].setHora(cirurgia.tc - 1 + tempo)
                                cnt += 1
    return cnt


def zeraDisponibilidade(tipo, Salas, Cirurgioes):
    for sala in Salas:
        sala.novoDia()
    if (tipo == "dia"):
        for cirurgiao in Cirurgioes:
            cirurgiao.novoDia()
    else:
        for cirurgiao in Cirurgioes:
            cirurgiao.novaSemana()


'''Algoritmo que agenda as cirurgias de forma gulosa, dando prioridade a algumas caracteristicas, retorna a configuração final das cirurgias agendadas
Tem como entrada: s- número de salas do problema, a lista com as Cirurgias, Cirurgioes e Salas.
'''


def agendaGreedy(s, Cirurgias, Salas, Cirurgioes):
    tempo_atual = 1
    dia_atual = 1
    semana_atual = 1
    cirurgias_realizadas = 0

    while cirurgias_realizadas < len(Cirurgias):
        cirurgias_realizadas += agenda(tempo_atual, dia_atual, semana_atual,
                                       Cirurgias, Salas, Cirurgioes)

        tempo_atual = 46

        # Acabou
        if (tempo_atual == 46):
            zeraDisponibilidade("dia", Salas, Cirurgioes)
            tempo_atual = 1
            dia_atual += 1
        if (dia_atual == 5):
            zeraDisponibilidade("semana", Salas, Cirurgioes)
            dial_atual = 1
            semana_atual += 1
            # Para de agendar as cirurgias
            break

    return None


'''
-- Uma formiga deve ser capaz de iniciar a sua busca a partir de uma cidade específica
-- Lembrar de todas as cidades visitadas
-- Armazenar o tamanho do caminho que está seguinte
'''


class Ant:
    # Vai armazenar os vértices já visitados

    def __init__(self, N, op, a, b, q):
        # quantidade de vértices no grafo
        self.alfa = a
        self.beta = b
        self.n = N
        self.op: List = op
        # Construo a funcao de probabilidade da formiga, de escolher uma operacao a ser realizada. prob[i][j][k], probabilidade de ir de i~j utilizando a operacao k
        # self.probability = [[[1.0 / float(self.op) for x in range(op)] for x in range(N)] for y in range(N)]
        self.probability = {}
        # Indices dos vértices visitados
        self.visited = []
        # Quantidade de feromonio excretada pela formiga
        self.Q = q

        # Arestas visitadas por esta formiga, (vi,op,vj)
        self.edges = []

    def addEdge(self, edge):
        self.edges.append(edge)

    def clear(self):
        self.visited = []

    def visitCity(self, i):
        self.visited.append(i)

    def isVisited(self, i):
        if i in self.visited:
            return True
        return False

    def tamanhoCaminho(self):
        # Neste problema o tamanho do caminho é a quantidade de arestas

        # O tamanho do caminho na verdade vai ser o Quanto esse caminho incrementou na solução final

        # for edge in edges:
        return len(self.edges)

    def heuristica(self, vi, vj):
        # Heuristica será o Delta: (Quanto se ganha ao utilizar a aresta,   FO(cnj2)/FO(cnj1), assim, quanto maior o ganho
        # melhor a atratividade de utilizar aquela aresta
        return vj.value * 1.0 / vi.value * 1.0

    def changeProbability(self, feromonio):
        # Pego a posicao da formiga
        self.at = self.visited[-1]  # Estou no último vértice

        # Para cada vértice não visitado, verifico o valor de transição e monto a tabela de probabilidade
        #
        s = 0  # Soma de todas as probabilidades

        # A probabilidade será: Pi,j * Pk ( Prob de ir do vértice i ao vértice j utilizando Kth operacao)
        # print(self.at)
        v = G.getNode(self.at)

        # Gera a vizinhança do Estado Atual
        # Crio os estados não visitados ainda.
        vizinhos = []
        for op in self.op:
            vizinho, _id = v.chooseOP(op)
            # print(vizinho.value)
            G.addNode(vizinho)
            edge = (G.getNode(self.at), op, vizinho)
            G.addEdge(G.getNode(self.at), op, vizinho)
            # Se o vértice já foi visitado continua
            if G.nodes[vizinho] in self.visited:
                continue
            vizinhos.append(edge)

            valor_heuristica = self.heuristica(v, vizinho)
            # print("Valor da heuritica: ", valor_heuristica)
            # print("Valor do feromonio: ", feromonio[ self.at ][ G.nodes[vizinho] ][op])

            # self.probability[ edge ] = pow(feromonio[ self.at ][ G.nodes[vizinho] ][op],self.alfa)* pow(valor_heuristica,self.beta)
            try:
                self.probability[edge] = pow(feromonio[edge], self.alfa) * pow(
                    valor_heuristica, self.beta)
            except:
                feromonio[edge] = 1
                self.probability[edge] = pow(feromonio[edge], self.alfa) * pow(
                    valor_heuristica, self.beta)
            s += self.probability[edge]

        # Atualizo a probabilidade de todo mundo viável
        if s != 0:
            for edge in vizinhos:
                self.probability[edge] = self.probability[edge] / s

    def depositaFeromonio(self, feromonio, graph):
        # lenght = self.tamanhoCaminho()
        # print("Deposita feromonio")
        for edge in self.edges:
            e = graph.getEdge(edge)
            # print(E1,operacao, EX )
            value_added = e[0].value / e[2].value
            # Vao ser i,a e
            if e not in feromonio.keys():
                feromonio[e] = 1 + self.Q / (
                        value_added * 1.0)  # Adiciono feromonio no caminho feromonio[i][j][op]
            else:
                feromonio[e] += self.Q / (
                        value_added * 1.0)  # Adiciono feromonio no caminho feromonio[i][j][op]


# E1
# E3 E4
def evaporaFeromonio(feromonio, p, graph):
    # print("Evapora Feromonio")
    for edge in graph.edges.keys():
        # Caso nao tenha visitado aquela aresta ainda e nao tenha feromonio depositado, continue
        try:
            feromonio[edge] = feromonio[edge] * (1 - p)
        except:
            pass


def read_instances(file, Cirurgias, Salas, Cirurgioes):
    lines = file.readlines()
    fo_target = np.inf
    unique_id_cir = {}
    for line, x in enumerate(lines, 1):
        if line == 1:
            s = int(x.split(" ")[1])
            # fo_target = int(x.split(" ")[2])

            for sala in range(s):
                Salas.append(Sala(sala))
        else:
            c = x.split(" ")
            Cirurgias.append(
                Cirurgia(int(c[0]), int(c[1]), int(c[2]), int(c[3]), int(c[4]),
                         int(c[5])))
            unique_id_cir[int(c[4])] = int(c[3])

    for key in unique_id_cir.keys():
        Cirurgioes.append(Cirurgiao(key, unique_id_cir[key]))

    return fo_target


def printSolution(Cirurgias):
    for cirurgia in Cirurgias:
        print("Id: ", cirurgia.id, " Prioridade: ", cirurgia.p,
              " Especialidade: ", cirurgia.e, " sala: ", cirurgia.sala,
              " dia: ", cirurgia.dia, " Inicio ", cirurgia.tc_inicio, " Fim ",
              cirurgia.tc_fim)
    print("Salvando solucao")

    max_id = 0
    for cirurgia in Cirurgias:
        max_id = max(max_id, cirurgia.id)

    for i in range(max_id):
        for cirurgia in Cirurgias:
            if (i + 1 == cirurgia.id):
                print("{};{};{};{}".format(cirurgia.id, cirurgia.sala + 1,
                                           cirurgia.dia, cirurgia.tc_inicio))


def checkConstrains():
    # Verifica se não extrapola a quantidade de tempo
    return ''


def check(Cirurgias, Salas, Cirurgioes):
    print("Informacoes das Salas: ")
    for sala in Salas:
        print("Sala id: ", sala.id, " Disponivel: ", sala.disponivel)
    print("Informacoes das Cirurgias: ")
    for cirurgia in Cirurgias:
        print("Id: ", cirurgia.id, " Prioridade: ", cirurgia.p,
              " Tempo de Espera: ", cirurgia.w,
              " Especialidade: ", cirurgia.e, " Cirurgiao: ",
              cirurgia.cirurgiao, " Duração: ", cirurgia.tc, " Sala: ",
              cirurgia.sala)

    print("Informacoes dos Cirurgioes: ")
    for cirurgiao in Cirurgioes:
        print("Cirurgiao id: ", cirurgiao.id, " Cirurgiao especialidade: ",
              cirurgiao.e, " Hdia: ", cirurgiao.hdia, " hSemana ",
              cirurgiao.hsemana)


# Funcao para realizar o teste no grafo criado.
def change(Cirurgias):
    x = Cirurgias.copy()
    newlst = []
    for cirurgia in x:
        new_c = Cirurgia(cirurgia.id, cirurgia.p, cirurgia.w, cirurgia.e,
                         cirurgia.cirurgiao, cirurgia.tc)
        new_c.setDia(random.randint(1, 10))
        new_c.setSala(cirurgia.sala)
        new_c.setSemana(cirurgia.semana)
        new_c.setTempo(cirurgia.tc_inicio, cirurgia.tc_fim)
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


def getStartNode():
    States = list(G.nodes.keys())
    States.sort(reverse=False)
    idx = random.randint(0, min(10, len(States) - 1))
    return G.nodes[States[idx]]


def gt(a, b):
    if (a.p < b.p):
        return True
    elif (a.p == b.p):
        if (a.w < b.w):
            return True
        elif (a.tc <= b.tc):
            return True
    return False


def make_comparator(less_than):
    def compare(a, b):
        if (less_than(a, b)):
            return -1
        elif (less_than(b, a)):
            return 1
        return 0

    return compare


def run_instance(Cirurgias, Salas, Cirurgioes, instance_fo_target=np.inf):
    start = time.time()

    Ants = []
    # Cirurgias2 = copy.deepcopy(Cirurgias)
    # Salas2 = copy.deepcopy(Salas)
    # Cirurgioes2 = copy.deepcopy(Cirurgioes)
    # Cirurgias2.sort(reverse=True)
    # check(Cirurgias, Salas, Cirurgioes)
    # printSolution(Cirurgias2)

    agendaGreedy(len(Salas), Cirurgias, Salas, Cirurgioes)
    # checkConstrains(Cirurgias, Salas, Cirurgioes)
    # printSolution(Cirurgias)

    # print("Funcao Objetivo: ", FO(Cirurgias))

    s1 = State(Cirurgias, Salas, FO(Cirurgias))
    # '''
    # 	Inicio da Heurística
    # '''
    # Cirurgias2.sort(reverse=False)
    # agendaGreedy(len(Salas2), Cirurgias2, Salas2, Cirurgioes2)
    # checkConstrains(Cirurgias2, Salas2, Cirurgioes2)
    # printSolution(Cirurgias2)

    # print("Funcao Objetivo: ", FO(Cirurgias2))

    # s2 = State(Cirurgias2, Salas2, FO(Cirurgias2))
    global G, feromonio
    G = Graph()
    # Nó inicial das formigas
    G.addNode(s1)
    # G.addNode(s2)

    # Inicialmente todas as formigas iniciam a sua busca no nó 0, que é o da solução gulosa
    best_value = np.inf
    max_iter = 20
    if instance_fo_target != np.inf:
        max_iter = 100
    # print(f"max_iter will be:{max_iter}")
    max_iter_without_improvement = 10
    N = 1000
    OPERATORS = [1, 2, 3, 4]
    alfa = 1
    beta = 1
    p = .5
    # graph = [[0 for x in range(N)] for y in range(N)]
    # Problema aqui, visita muitos nós e da overflow
    # feromonio = [[[1 for k in range(2)] for j in range(N)] for i in range(N)] # Feromonio[i][j][op]
    # Alteração do feromonio para acessar um estado com lista encadeada, entrada é a aresta, saída é o total de ferômonio depositado nesta aresta
    # Aresta será levado em consideração o Mapeamento da aresta no GRAFO
    # Inicialmente TODOS começam com a mesma quantidade de ferômonio, no momento do depósito ( caso seja a primeira vez será adicionado o valor de 1 unidade)
    feromonio = {}
    it = 0
    iter_without_improvement = 0
    max_nodes = 5  # Cada formiga irá descobrir 10 nós
    n_formigas = 10

    for i in range(n_formigas):
        Ants.append(Ant(N, OPERATORS, alfa, beta, 1))

    # best_visited = min(s1.value, s2.value)
    best_visited = s1.value
    previous_best_visited = s1.value
    best_solution = s1.Cirurgias.copy()
    # if best_visited == s2.value:
    #     best_solution = s2.Cirurgias.copy()
    while (it <= max_iter and
            best_visited <= instance_fo_target and
            iter_without_improvement <= max_iter_without_improvement):
        # print(f"it:{it}")
        # print(f"iter_without_improvement:{iter_without_improvement}")
        # Fazer uma mutação nas Formigas !!!
        # Armazenar nas formigas, o caminho de arestas com MENOR valor possivel
        for ant in Ants:
            # print("Inicio da formiga id {}".format(f%n_formigas))
            ant.clear()

            # Para cada inicio, coloca uma formiga em uma cidade aleatória diferente.
            # Aumentar a chance de pegar nós com baixa FO, alguns nós com baixo e outros com FO grande

            node_start = getStartNode()

            ant.visitCity(node_start)
            # print("Visita a cidade: {}".format(node_start))
            visited_cnt = 1  # a cidade inicial já foi visitada.
            # Enquanto não visitou todos os vértices, continua visitando:

            while visited_cnt != max_nodes:
                # Coleto onde a formiga K está
                # print(len(ant.visited),ant.visited[-1])
                v = G.getNode(ant.visited[-1])
                # print(" Está no vértice com valor: ", v.value)

                # Para cada operacao, verifico a de maior vizinhança

                Ni = []  # Lista de vizinhança, vai possuir uma tupla (state,prob)
                prob_Ni = []

                for op in ant.op:
                    vizinho, _id = v.chooseOP(op)
                    # print(_id)
                    # print("Vizinho de valor: {}".format(vizinho.value))
                    if (vizinho.value >= pow(10, 9)):
                        continue
                    # if(vizinho.value < best_visited):
                    # 	best_visited = vizinho.value
                    # 	best_solution = vizinho.Cirurgias.copy()
                    G.addNode(vizinho)  # Adiciono o nó ao grafo
                    G.addEdge(v, op, vizinho)  # Adiciono a vizinhança ao grafo

                    Ni.append(G.edges[(v, op, vizinho)])

                    # A probabilidade de se seguir por aquele vertice, sera dada pelo vetor de probabilidades inicial, onde todos os vertices sao equiprovaveis
                    edge = (v, op, vizinho)
                    try:
                        prob_Ni.append(ant.probability[edge])
                    except:
                        # Todos iniciam com a mesma probabilidade, sendo o numero de operacoes
                        ant.probability[edge] = 1.0 / len(ant.op)
                        prob_Ni.append(ant.probability[edge])

                if 0 == len(Ni):
                    break

                if sum(prob_Ni) != 1:
                    # print(prob_Ni)
                    idx = np.random.choice(len(Ni), 1)[
                        0]  # Escolho qual aresta seguir.
                else:
                    idx = np.random.choice(len(Ni), 1, p=prob_Ni)[
                        0]  # Escolho qual aresta seguir.

                estado_escolhido = G.getEdge(Ni[idx])[
                    2]  # Escolho o estado a ser utilizado

                if estado_escolhido.value < best_visited:
                    best_visited = estado_escolhido.value
                    best_solution = estado_escolhido.Cirurgias.copy()

                if not ant.isVisited(G.nodes[estado_escolhido]):
                    # print("Visistou o vértice com valor {}".format(estado_escolhido.value))
                    next_v = estado_escolhido
                    visited_cnt += 1

                # Visito a cidade a partir daquela formiga
                ant.visitCity(G.nodes[next_v])

                ant.addEdge(Ni[idx])

            ant.depositaFeromonio(feromonio, G)
            # Verifica se a rota utilizada pela formiga foi a melhor até o momento
            # print(ant.visited)

            value = G.getNode(ant.visited[-1]).value

            if value < best_value:
                best_value = value
                best_rota = ant.edges
                
        # print("Fim da formiga")
        evaporaFeromonio(feromonio, p, G)

        # Altero a probabilidade de escolher aquela aresta.

        ant.changeProbability(feromonio)

        it += 1
        if best_visited < previous_best_visited:
            previous_best_visited = best_visited
            iter_without_improvement = 0
        elif best_visited == previous_best_visited:
            iter_without_improvement += 1
        
    stop_criteria = 0
    if it >= max_iter:
        stop_criteria = 1
    elif best_value >= instance_fo_target:
        stop_criteria = 2
    elif iter_without_improvement >= max_iter_without_improvement:
        stop_criteria = 3
    # print(f"stop_criteria {stop_criteria}")
    print("MELHOR VALOR ENCONTRADO: {}".format(best_visited))

    # printSolution(best_solution)

    end = time.time()
    time_elapsed = end - start
    # print(time_elapsed)

    return time_elapsed, best_visited, stop_criteria


N_TIMES_EACH_INSTANCE = 5


def main():
    filenames = glob.glob("I*.txt")
    print(f"About to get data to {len(filenames)} instances")
    for file in filenames:
        print(file)

        Cirurgias = []
        Salas = []
        Cirurgioes = []

        instance_results = {}
        with open(file, 'r') as f:
            fo_target = read_instances(f, Cirurgias, Salas, Cirurgioes)

        for i in range(N_TIMES_EACH_INSTANCE):
            print(f"{i+1}th time running {file} instance")
            instance_results[i] = run_instance(copy.deepcopy(Cirurgias),
                                               copy.deepcopy(Salas),
                                               copy.deepcopy(Cirurgioes),
                                               fo_target
                                               )

        print(instance_results)
        time_values = list(map(lambda x: x[0], instance_results.values()))
        time_elapsed_avg = sum(time_values) / \
                           len(instance_results.values())
        min_time_elapsed = min(time_values)
        max_time_elapsed = max(time_values)
        med_time_elapsed = np.median(time_values)
        std = np.std(time_values)
        print(f"Time elapsed avg: {time_elapsed_avg}")
        print(f"Time elapsed min: {min_time_elapsed}")
        print(f"Time elapsed max: {max_time_elapsed}")
        print(f"Time elapsed med: {med_time_elapsed}")
        print(f"Time elapsed std: {std}")

        fo_values = list(map(lambda x: x[1], instance_results.values()))
        time_elapsed_avg = sum(fo_values) / \
                           len(instance_results.values())
        min_time_elapsed = min(fo_values)
        max_time_elapsed = max(fo_values)
        med_time_elapsed = np.median(fo_values)
        std = np.std(fo_values)
        print(f"FO avg: {time_elapsed_avg}")
        print(f"FO min: {min_time_elapsed}")
        print(f"FO max: {max_time_elapsed}")
        print(f"FO med: {med_time_elapsed}")
        print(f"FO std: {std}")

        stop_criteria_values = list(map(lambda x: x[2], instance_results.values()))
        stop_criteria_mode = stat.mode(stop_criteria_values)
        print(f"Stop Criteria mode: {stop_criteria_mode}")


if __name__ == '__main__':
    main()
