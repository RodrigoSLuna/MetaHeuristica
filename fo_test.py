# Funcao verifica se a instancia está dentro do Bloco do Problema.
from cirurgia import Cirurgia, Sala

lp = {1: 3, 2: 15, 3: 60, 4: 365}
fp = {1: 90, 2: 20, 3: 5, 4: 1}


def verificaInstancia(cirurgias, salas):
    # Verifica se todos que estão na mesma sala, possuem a mesma
    dia = 1
    while dia <= 5:
        esp_sala = {}
        for sala in salas:
            for cirurgia in cirurgias:
                if cirurgia.dia == dia and cirurgia.sala == sala.id:
                    if sala.id in esp_sala.keys():
                        if esp_sala[sala.id] != cirurgia.e:
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
        for cirurgia in cirurgias:
            if (cirurgia.id != -1 and cirurgia.dia == dia):
                try:
                    tempo_gasto_semana[cirurgia.cirurgiao] += cirurgia.w
                except:
                    tempo_gasto_semana[cirurgia.cirurgiao] = cirurgia.w

                try:
                    tempo_gasto_dia[cirurgia.cirurgiao] += cirurgia.w
                except:
                    tempo_gasto_dia[cirurgia.cirurgiao] = cirurgia.w
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


def FO(cirurgias, salas):
    print("hey yo!")
    penalty = 0
    # Dar penalidade para instancias com restrições falhadas diferentemente?
    if not verificaInstancia(cirurgias, salas):
        penalty += pow(10, 9) + 1
    for cirurgia in cirurgias:
        vc = 0
        xcstd = 0
        zc = 0
        p1 = 0
        if cirurgia.dia == -1 or \
                cirurgia.tc_inicio == -1 or \
                cirurgia.tc_fim == -1:
            zc = 1
        else:
            xcstd = 1

        if cirurgia.dia + cirurgia.w > lp[cirurgia.p]:
            vc = 1

        if cirurgia.p == 1 and cirurgia.dia > 1:
            p1 = 1

        penalty += pow(10 * (cirurgia.w + 2), cirurgia.dia) * p1

        if cirurgia.dia != -1:
            penalty += (pow(cirurgia.w + 2 + cirurgia.dia, 2) + pow(
                cirurgia.w + 2 + cirurgia.dia - lp[cirurgia.dia],
                2) * vc) * xcstd
        else:
            penalty += (pow(cirurgia.w + 7, 2) * fp[cirurgia.p] + fp[
                cirurgia.p] * vc * (
                            pow(cirurgia.w + 9 - lp[cirurgia.p], 2))) * zc

    return penalty


def test_fo_toy1_urgency_delay():
    cirurgias, salas = set_toy1_original_solution()
    cirurgias[0].sala = 1
    cirurgias[0].tc_inicio = 42
    cirurgias[0].tc_fim = 46
    cirurgias[0].dia = 2
    cirurgias[0].semana = 1

    cirurgias[7].sala = 1
    cirurgias[7].tc_inicio = 1
    cirurgias[7].tc_fim = 5
    cirurgias[7].dia = 1
    cirurgias[7].semana = 1

    return FO(cirurgias, salas)


def test_fo_toy1_original():
    cirurgias, salas = set_toy1_original_solution()

    return FO(cirurgias, salas)


def set_toy1_original_solution():
    cirurgias = [
        Cirurgia(1, 1, 1, 1, 1, 5),
        Cirurgia(2, 1, 1, 1, 1, 13),
        Cirurgia(3, 1, 1, 1, 2, 8),
        Cirurgia(4, 1, 1, 1, 2, 11),
        Cirurgia(5, 2, 10, 2, 3, 10),
        Cirurgia(6, 3, 9, 2, 4, 14),
        Cirurgia(7, 2, 8, 2, 3, 11),
        Cirurgia(8, 3, 5, 2, 4, 5)
    ]
    salas = [Sala(1)]
    cirurgias[0].sala = 1
    cirurgias[0].tc_inicio = 1
    cirurgias[0].tc_fim = cirurgias[0].tc
    cirurgias[0].dia = 1
    cirurgias[0].semana = 1
    cirurgias[1].sala = 1
    cirurgias[1].tc_inicio = 8
    cirurgias[1].tc_fim = 20
    cirurgias[1].dia = 1
    cirurgias[1].semana = 1
    cirurgias[2].sala = 1
    cirurgias[2].tc_inicio = 23
    cirurgias[2].tc_fim = 30
    cirurgias[2].dia = 1
    cirurgias[2].semana = 1
    cirurgias[3].sala = 1
    cirurgias[3].tc_inicio = 33
    cirurgias[3].tc_fim = 43
    cirurgias[3].dia = 1
    cirurgias[3].semana = 1
    cirurgias[4].sala = 1
    cirurgias[4].tc_inicio = 1
    cirurgias[4].tc_fim = 10
    cirurgias[4].dia = 2
    cirurgias[4].semana = 1
    cirurgias[5].sala = 1
    cirurgias[5].tc_inicio = 26
    cirurgias[5].tc_fim = 39
    cirurgias[5].dia = 2
    cirurgias[5].semana = 1
    cirurgias[6].sala = 1
    cirurgias[6].tc_inicio = 13
    cirurgias[6].tc_fim = 23
    cirurgias[6].dia = 2
    cirurgias[6].semana = 1
    cirurgias[7].sala = 1
    cirurgias[7].tc_inicio = 42
    cirurgias[7].tc_fim = 46
    cirurgias[7].dia = 2
    cirurgias[7].semana = 1
    return cirurgias, salas


if __name__ == '__main__':
    print("I got here!")
    print(test_fo_toy1_original())
    print(test_fo_toy1_urgency_delay())



