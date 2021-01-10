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
    # print("hey yo!")
    penalty = 0
    # Dar penalidade para instancias com restrições falhadas diferentemente?
    # if not verificaInstancia(cirurgias, salas):
    #     penalty += pow(10, 9) + 1
    for cirurgia in cirurgias:
        copy_penalty = penalty
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
            # print("scheduled")
            # if vc == 1:
            #     # print("vencida")
            penalty += (pow(cirurgia.w + 2 + cirurgia.dia, 2) +
                        (pow(cirurgia.w + 2 + cirurgia.dia - lp[cirurgia.dia],
                             2) * vc)
                        ) * xcstd
        else:
            # print("not scheduled")
            penalty += (pow(cirurgia.w + 7, 2) * fp[cirurgia.p] + fp[
                cirurgia.p] * vc * (
                            pow(cirurgia.w + 9 - lp[cirurgia.p], 2))) * zc

        print(f"\t{cirurgia.id}:{penalty - copy_penalty}")

    return penalty


def test_fo_toy1_urgency_delay(wc5=10):
    cirurgias, salas = set_toy1_original_solution(wc5)
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


def test_fo_toy1_original(wc5=10):
    cirurgias, salas = set_toy1_original_solution(wc5)

    return FO(cirurgias, salas)


def test_fo_toy2_original_2rooms():
    cirurgias, salas = set_toy2_original_solution()

    return FO(cirurgias, salas)


def test_fo_toy2_manysurgeons():
    cirurgias, salas = set_toy2_original_solution_withmanysurgeons()

    return FO(cirurgias, salas)


def test_fo_toy2_original_manysurgeons_wc5():
    cirurgias, salas = set_toy2_original_solution(20)

    return FO(cirurgias, salas)


def set_surgery_by_id(cirurgias, id, sala, inicio, fim, dia):
    cirurgias[id].sala = sala
    cirurgias[id].tc_inicio = inicio
    cirurgias[id].tc_fim = fim
    cirurgias[id].dia = dia
    cirurgias[id].semana = 1


def test_fo_toy4_original():
    cirurgias, salas = set_toy4_original_solution()
    return FO(cirurgias, salas)


def test_fo_toy4_boosted_solution():
    cirurgias, salas = set_toy4_boosted_solution()
    return FO(cirurgias, salas)


def set_toy4_boosted_solution():
    cirurgias = [
        Cirurgia(1, 2, 1, 1, 1, 10),
        Cirurgia(2, 2, 1, 1, 2, 10),
        Cirurgia(3, 2, 1, 1, 3, 20),
        Cirurgia(4, 2, 10, 1, 4, 20),
        Cirurgia(5, 2, 12, 1, 5, 20),
        Cirurgia(6, 2, 15, 1, 6, 20),
        Cirurgia(7, 2, 1, 1, 7, 10),
        Cirurgia(8, 2, 1, 1, 8, 10),
        Cirurgia(9, 2, 1, 1, 9, 5),
        Cirurgia(10, 2, 1, 1, 10, 5),
        Cirurgia(11, 2, 1, 1, 10, 5),
        Cirurgia(12, 2, 1, 1, 10, 5)
    ]

    set_surgery_by_id(cirurgias, 0, 1, 23, 32, 4)
    set_surgery_by_id(cirurgias, 1, 1, 35, 44, 2)
    set_surgery_by_id(cirurgias, 2, 1, 1, 20, 3)
    set_surgery_by_id(cirurgias, 3, 1, 1, 20, 4)
    set_surgery_by_id(cirurgias, 4, 1, 23, 43, 1)
    set_surgery_by_id(cirurgias, 5, 1, 1, 20, 1)
    set_surgery_by_id(cirurgias, 6, 1, 23, 32, 3)
    set_surgery_by_id(cirurgias, 7, 1, 35, 44, 3)
    set_surgery_by_id(cirurgias, 8, 1, 1, 5, 2)
    set_surgery_by_id(cirurgias, 9, 1, 8, 12, 2)
    set_surgery_by_id(cirurgias, 10, 1, 15, 19, 2)
    set_surgery_by_id(cirurgias, 11, 1, 22, 26, 2)
    return cirurgias, None


def set_toy4_original_solution():
    cirurgias = [
        Cirurgia(1, 2, 1, 1, 1, 10),
        Cirurgia(2, 2, 1, 1, 2, 10),
        Cirurgia(3, 2, 1, 1, 3, 20),
        Cirurgia(4, 2, 10, 1, 4, 20),
        Cirurgia(5, 2, 12, 1, 5, 20),
        Cirurgia(6, 2, 15, 1, 6, 20),
        Cirurgia(7, 2, 1, 1, 7, 10),
        Cirurgia(8, 2, 1, 1, 8, 10),
        Cirurgia(9, 2, 1, 1, 9, 5),
        Cirurgia(10, 2, 1, 1, 10, 5),
        Cirurgia(11, 2, 1, 1, 10, 5),
        Cirurgia(12, 2, 1, 1, 10, 5)
    ]

    set_surgery_by_id(cirurgias, 0, 1, 23, 32, 2)
    set_surgery_by_id(cirurgias, 1, 1, 35, 44, 2)
    set_surgery_by_id(cirurgias, 2, 1, 1, 20, 3)
    set_surgery_by_id(cirurgias, 3, 1, 1, 20, 2)
    set_surgery_by_id(cirurgias, 4, 1, 23, 42, 1)
    set_surgery_by_id(cirurgias, 5, 1, 1, 20, 1)
    set_surgery_by_id(cirurgias, 6, 1, 23, 32, 3)
    set_surgery_by_id(cirurgias, 7, 1, 35, 44, 3)
    set_surgery_by_id(cirurgias, 8, 1, 1, 5, 4)
    set_surgery_by_id(cirurgias, 9, 1, 8, 12, 4)
    set_surgery_by_id(cirurgias, 10, 1, 15, 19, 4)
    set_surgery_by_id(cirurgias, 11, 1, 22, 26, 4)

    return cirurgias, None


def set_toy2_original_solution_withmanysurgeons(wc5=10):
    cirurgias = [
        Cirurgia(1, 1, 1, 1, 1, 5),
        Cirurgia(2, 1, 1, 1, 2, 13),
        Cirurgia(3, 1, 1, 1, 3, 8),
        Cirurgia(4, 1, 1, 1, 4, 11),
        Cirurgia(5, 2, wc5, 2, 5, 10),
        Cirurgia(6, 3, 9, 2, 6, 14),
        Cirurgia(7, 2, 8, 2, 7, 11),
        Cirurgia(8, 3, 5, 2, 8, 5)
    ]

    salas = [Sala(1), Sala(2)]

    cirurgias[0].sala = 1
    cirurgias[0].tc_inicio = 1
    cirurgias[0].tc_fim = 5
    cirurgias[0].dia = 1
    cirurgias[0].semana = 1
    cirurgias[1].sala = 1
    cirurgias[1].tc_inicio = 8
    cirurgias[1].tc_fim = 20
    cirurgias[1].dia = 1
    cirurgias[1].semana = 1
    cirurgias[2].sala = 2
    cirurgias[2].tc_inicio = 1
    cirurgias[2].tc_fim = 8
    cirurgias[2].dia = 1
    cirurgias[2].semana = 1
    cirurgias[3].sala = 2
    cirurgias[3].tc_inicio = 11
    cirurgias[3].tc_fim = 21
    cirurgias[3].dia = 1
    cirurgias[3].semana = 1

    cirurgias[4].sala = 1
    cirurgias[4].tc_inicio = 1
    cirurgias[4].tc_fim = 10
    cirurgias[4].dia = 2
    cirurgias[4].semana = 1
    cirurgias[6].sala = 1
    cirurgias[6].tc_inicio = 13
    cirurgias[6].tc_fim = 23
    cirurgias[6].dia = 2
    cirurgias[6].semana = 1

    cirurgias[5].sala = 2
    cirurgias[5].tc_inicio = 1
    cirurgias[5].tc_fim = 14
    cirurgias[5].dia = 2
    cirurgias[5].semana = 1
    cirurgias[7].sala = 2
    cirurgias[7].tc_inicio = 17
    cirurgias[7].tc_fim = 23
    cirurgias[7].dia = 2
    cirurgias[7].semana = 1

    return cirurgias, salas


def set_toy2_original_solution(wc5=10):
    cirurgias = [
        Cirurgia(1, 1, 1, 1, 1, 5),
        Cirurgia(2, 1, 1, 1, 1, 13),
        Cirurgia(3, 1, 1, 1, 1, 8),
        Cirurgia(4, 1, 1, 1, 1, 11),
        Cirurgia(5, 2, wc5, 2, 2, 10),
        Cirurgia(6, 3, 9, 2, 2, 14),
        Cirurgia(7, 2, 8, 2, 2, 11),
        Cirurgia(8, 3, 5, 2, 2, 5)
    ]
    salas = [Sala(1), Sala(2)]

    cirurgias[0].sala = 1
    cirurgias[0].tc_inicio = 1
    cirurgias[0].tc_fim = 5
    cirurgias[0].dia = 1
    cirurgias[0].semana = 1
    cirurgias[1].sala = 1
    cirurgias[1].tc_inicio = 8
    cirurgias[1].tc_fim = 20
    cirurgias[1].dia = 1
    cirurgias[1].semana = 1

    cirurgias[2].sala = 1
    cirurgias[2].tc_inicio = 1
    cirurgias[2].tc_fim = 8
    cirurgias[2].dia = 2
    cirurgias[2].semana = 1
    cirurgias[3].sala = 1
    cirurgias[3].tc_inicio = 11
    cirurgias[3].tc_fim = 21
    cirurgias[3].dia = 2
    cirurgias[3].semana = 1

    cirurgias[4].sala = 2
    cirurgias[4].tc_inicio = 1
    cirurgias[4].tc_fim = 10
    cirurgias[4].dia = 1
    cirurgias[4].semana = 1
    cirurgias[6].sala = 2
    cirurgias[6].tc_inicio = 13
    cirurgias[6].tc_fim = 23
    cirurgias[6].dia = 1
    cirurgias[6].semana = 1

    cirurgias[5].sala = 2
    cirurgias[5].tc_inicio = 1
    cirurgias[5].tc_fim = 14
    cirurgias[5].dia = 2
    cirurgias[5].semana = 1
    cirurgias[7].sala = 2
    cirurgias[7].tc_inicio = 17
    cirurgias[7].tc_fim = 23
    cirurgias[7].dia = 2
    cirurgias[7].semana = 1

    return cirurgias, salas


def set_toy1_original_solution(surgery5_w=10):
    cirurgias = [
        Cirurgia(1, 1, 1, 1, 1, 5),
        Cirurgia(2, 1, 1, 1, 1, 13),
        Cirurgia(3, 1, 1, 1, 2, 8),
        Cirurgia(4, 1, 1, 1, 2, 11),
        Cirurgia(5, 2, surgery5_w, 2, 3, 10),
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


def test_fo_toy4_delayc4():
    cirurgias, salas = set_toy4_original_solution()

    set_surgery_by_id(cirurgias, 0, 1, 23, 32, 4)
    set_surgery_by_id(cirurgias, 1, 1, 35, 44, 2)
    set_surgery_by_id(cirurgias, 2, 1, 1, 20, 3)
    set_surgery_by_id(cirurgias, 3, 1, 1, 20, 4)
    set_surgery_by_id(cirurgias, 4, 1, 23, 42, 1)
    set_surgery_by_id(cirurgias, 5, 1, 1, 20, 1)
    set_surgery_by_id(cirurgias, 6, 1, 23, 32, 3)
    set_surgery_by_id(cirurgias, 7, 1, 35, 44, 3)
    set_surgery_by_id(cirurgias, 8, 1, 1, 5, 2)
    set_surgery_by_id(cirurgias, 9, 1, 8, 12, 2)
    set_surgery_by_id(cirurgias, 10, 1, 15, 19, 2)
    set_surgery_by_id(cirurgias, 11, 1, 22, 26, 2)

    return FO(cirurgias, salas)


if __name__ == '__main__':
    test = 1
    print(f"Test {test}")
    print(test_fo_toy1_original())

    test += 1
    print(f"Test {test}")
    print(test_fo_toy1_urgency_delay())
    test += 1

    print(f"Test {test}")
    print(test_fo_toy1_original(wc5=20))
    test += 1

    print(f"Test {test}")
    print(test_fo_toy2_original_2rooms())
    test += 1

    print(f"Test {test}")
    print(test_fo_toy2_manysurgeons())
    test += 1

    print(f"Test {test}")
    print(test_fo_toy2_original_manysurgeons_wc5())
    test += 1

    print(f"Test {test}")
    print(test_fo_toy4_original())
    test += 1

    print(f"Test {test}")
    print(test_fo_toy4_boosted_solution())
    test += 1

    print(f"Test {test}")
    print(test_fo_toy4_delayc4())
    test += 1
