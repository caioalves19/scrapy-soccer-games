import json


with open("soccer_games/data/ids_campeonatos.json", "r", encoding="utf-8") as f:
    ids_campeonatos = json.load(f)


# Links com todos os campeonatos necessários para scraping da CBF
def criar_link(link):
    link_completo = f"https://www.cbf.com.br/futebol-brasileiro/competicoes/{link}/"
    print(f'"{link_completo}",')
    return link_completo


serie_a = criar_link("campeonato-brasileiro-serie-a")
serie_b = criar_link("campeonato-brasileiro-serie-b")
serie_c = criar_link("campeonato-brasileiro-serie-c")
serie_d = criar_link("campeonato-brasileiro-serie-d")
br_sub20 = criar_link("campeonato-brasileiro-sub20")
br_sub17 = criar_link("campeonato-brasileiro-sub17")
br_aspirantes = criar_link("campeonato-brasileiro-aspirantes")
fem_a1 = criar_link("campeonato-brasileiro-feminino-a1")
fem_a2 = criar_link("campeonato-brasileiro-feminino-a2")
fem_a3 = criar_link("campeonato-brasileiro-feminino-a3")
fem_sub17 = criar_link("campeonato-brasileiro-feminino-sub17")
fem_sub20 = criar_link("campeonato-brasileiro-feminino-sub20")
copa_br = criar_link("copa-brasil-masculino")
copa_br_sub17 = criar_link("copa-brasil-sub17")
copa_br_sub20 = criar_link("copa-brasil-sub20")
copa_ne = criar_link("copa-nordeste-masculino")
copa_verde = criar_link("copa-verde")
supercopa_fem = criar_link("supercopa-feminina")

links_cbf = [
    serie_a,
    # serie_b,
    # serie_c,
    # serie_d,
    # br_sub17,
    # br_sub20,
    # copa_br,
    # copa_ne,
    # copa_br_sub17,
    # fem_sub20,
    # copa_verde,
    # fem_a1,
    # fem_a2,
    # fem_a3,
]

# links_cbf = [
#     serie_a,
#     serie_b,
#     serie_c,
#     serie_d,
# ]

# links_cbf = [
#     br_sub17,
#     br_sub20,
#     copa_br,
#     copa_br_sub17,
#     fem_sub20,
#     fem_a1,
#     fem_a2,
#     fem_a3,
# ]


def obter_rodada_jogo(nome_campeonato, numero_jogo):
    # Usa o número do jogo para descobrir de qual rodada é.
    # [qntde_jogos_rodada, jogos_já_realizados]

    campeonatos = {
        "Copa do Nordeste - Única": [2, 70],
        "Brasileirão - Série D": [16, 448],
        "Brasileirão - Série C": [10, 0],
        "Brasileirão - Aspirantes": [2, 0],
        "Brasileirão - Sub-20": [10, 0],
        "Brasileirão - Sub-17": [10, 0],
        "Brasileirão Feminino - A1": [8, 0],
        "Brasileirão Feminino - A2": [1, 68],
        "Brasileirão Feminino - A3": [1, 60],
        "Brasileirão Feminino - Sub-17": [2, 0],
        "Brasileirão Feminino - Sub-20": [2, 108],
        "Copa do Brasil - Única": [8, 92],
        "Copa do Brasil - Sub-17": [1, 44],
        "Copa do Brasil - Sub-20": [1, 0],
        "Copa Verde - Única": [1, 28],
        "Supercopa Feminina - Única": [1, 6],
    }

    quantidade_jogos_rodada = campeonatos.get(nome_campeonato, [10, 0])[0]

    contagem_jogos_inicial = campeonatos.get(nome_campeonato, [10, 0])[1]

    rodada = (numero_jogo - contagem_jogos_inicial) // quantidade_jogos_rodada

    if (numero_jogo - contagem_jogos_inicial) % quantidade_jogos_rodada != 0:
        rodada += 1

    return rodada


def obter_nome_campeonato(response):
    # Deixar o nome do campeonato no padrão necessário. "Nome do Campeonato - Divisão do Campeonato"
    link_nome = response.url.split("/")[-3]
    campeonatos = {
        "campeonato-brasileiro-aspirantes": "Campeonato Brasileiro - Aspirantes",
        "campeonato-brasileiro-serie-a": "Brasileirão - Série A",
        "campeonato-brasileiro-serie-b": "Brasileirão - Série B",
        "campeonato-brasileiro-serie-c": "Brasileirão - Série C",
        "campeonato-brasileiro-serie-d": "Brasileirão - Série D",
        "copa-nordeste-masculino": "Copa do Nordeste - Única",
        "copa-brasil-masculino": "Copa do Brasil - Única",
        "campeonato-brasileiro-feminino-a1": "Brasileirão Feminino - A1",
        "campeonato-brasileiro-feminino-a2": "Brasileirão Feminino - A2",
        "campeonato-brasileiro-feminino-a3": "Brasileirão Feminino - A3",
        "campeonato-brasileiro-feminino-sub17": "Brasileirão Feminino - Sub-17",
        "campeonato-brasileiro-feminino-sub20": "Brasileirão Feminino - Sub-20",
        "copa-brasil-sub17": "Copa do Brasil - Sub-17",
        "copa-brasil-sub20": "Copa do Brasil - Sub-20",
        "campeonato-brasileiro-sub20": "Brasileirão - Sub-20",
        "campeonato-brasileiro-sub17": "Brasileirão - Sub-17",
        "copa-verde": "Copa Verde - Única",
        "supercopa-feminina": "Supercopa Feminina - Única",
    }
    return campeonatos.get(link_nome)


def obter_id_campeonato(nome_campeonato):
    id_campeonato = ids_campeonatos.get(nome_campeonato)
    return id_campeonato


def obter_local(response):
    locais_especiais = {
        "Marmudão": ["Marmudão", "Governador Valadares", "MG"],
        "Nogueirão": ["Nogueirão", "Mossoró", "RN"],
        "Simões Filho": ["Reitor Edgard Santos", "Simões Filho", "BA"],
    }

    local = response.css(".col-xs-12 span::text").get()

    if local in locais_especiais:
        return locais_especiais[local]

    local = local.split(" - ")
    if "a definir" in local[0].lower():
        local *= 3
    return local


def tratar_hora(hora):
    # Deixar data no padrão do projeto
    if not hora or "a definir" in hora.lower():
        return "00:00"
    return hora


def tratar_data(data, rodada_jogo):
    # Deixar data no padrão do projeto
    if not data:
        datas = {
            # 1: "28/04",
            # 2: "04/05",
            # 3: "16/04",
            # 4: "23/04",
            5: "30/07",
            6: "06/08",
            7: "13/08",
            8: "20/08",
            9: "27/08",
            # 10: "18/06",
            # 11: "25/06",
            # 12: "02/07",
            # 13: "09/07",
            # 14: "16/07",
            # 15: "23/07",
            # 16: "30/07",
            # 17: "06/08",
            # 18: "13/08",
            # 19: "21/08",
            # 20: "27/07",
            # 21: "03/08",
            # 22: "10/08",
            # 23: "17/08",
            # 24: "24/08",
            # 25: "31/08",
            # 26: "14/09",
            # 27: "21/09",
            # 28: "28/09",
            # 29: "04/10",
            # 30: "19/10",
            # 31: "25/10",
            # 32: "06/11",
            # 33: "13/11",
            # 34: "20/11",
            # 35: "23/11",
            # 36: "30/11",
            # 37: "04/12",
            # 38: "08/12",
        }
        return "01/01/0001"
        return f"{datas[rodada_jogo]}/2024"
    return data


def obter_fase_jogo(numero_jogo, nome_campeonato):
    fases = []

    if "Copa do Brasil - Sub-17" in nome_campeonato:
        fases = [
            "1ª Fase",
            "Oitavas de Final",
            "Quartas de Final",
            "Semifinais",
            "Final",
        ]
        numero_fases = [16, 32, 40, 44, 45]

    elif "Copa do Brasil - Sub-20" in nome_campeonato:
        fases = [
            "1ª Fase",
            "Oitavas de Final",
            "Quartas de Final",
            "Semifinais",
            "Final",
        ]
        numero_fases = [16, 32, 40, 44, 45]

    elif "Supercopa Feminina" in nome_campeonato:
        fases = [
            "Quartas de Final",
            "Semifinais",
            "Final",
        ]
        numero_fases = [4, 6, 7]

    elif "Copa do Brasil - Única" in nome_campeonato:
        fases = [
            "1ª Fase",
            "2ª Fase",
            "3ª Fase",
            "Oitavas de Final",
            "Quartas de Final",
            "Semifinais",
            "Final",
        ]
        numero_fases = [40, 60, 92, 108, 116, 120, 122]

    elif "Série C" in nome_campeonato:
        fases = ["1ª Fase", "2ª Fase", "Final"]
        numero_fases = [190, 214, 216]

    elif "Aspirantes" in nome_campeonato:
        fases = ["Fase de Grupos", "Quartas de Final", "Semifinais", "Final"]
        numero_fases = [48, 56, 60, 62]

    elif "Brasileirão - Sub-20" in nome_campeonato:
        fases = ["1ª Fase", "Quartas de Final", "Semifinais", "Final"]
        numero_fases = [190, 194, 196, 198]

    elif "Brasileirão - Sub-17" in nome_campeonato:
        fases = ["1ª Fase", "Quartas de Final", "Semifinais", "Final"]
        numero_fases = [90, 98, 102, 103]

    elif "Feminino - A1" in nome_campeonato:
        fases = ["1ª Fase", "Quartas de Final", "Semifinais", "Final"]
        numero_fases = [120, 128, 132, 134]

    elif "Feminino - A2" in nome_campeonato:
        fases = ["1ª Fase", "Quartas de Final", "Semifinais", "Final"]
        numero_fases = [56, 64, 68, 70]

    elif "Feminino - A3" in nome_campeonato:
        fases = [
            "1ª Fase",
            "Oitavas de Final",
            "Quartas de Final",
            "Semifinais",
            "Final",
        ]
        numero_fases = [32, 48, 56, 60, 62]

    elif "Feminino - Sub-17" in nome_campeonato:
        fases = ["1ª Fase", "Semifinais", "Final"]
        numero_fases = [24, 28, 29]

    elif "Feminino - Sub-20" in nome_campeonato:
        fases = ["1ª Fase", "Quartas de Final", "Semifinais", "Final"]
        numero_fases = [100, 108, 112, 113]

    elif "Campeonato Paulista - Série A1" in nome_campeonato:
        fases = ["1ª Fase", "Quartas de Final", "Semifinais", "Final"]
        numero_fases = [96, 104, 108, 110]

    elif "Série D" in nome_campeonato:
        fases = [
            "Fase de Grupos",
            "2ª Fase",
            "Oitavas de Final",
            "Quartas de Final",
            "Semifinais",
            "Final",
        ]
        numero_fases = [448, 480, 496, 504, 508, 510]

    elif "Copa do Nordeste" in nome_campeonato:
        fases = ["Fase de Grupos", "Quartas de Final", "Semifinais", "Final"]
        numero_fases = [64, 68, 70, 72]

    elif "Copa Verde" in nome_campeonato:
        fases = [
            "1ª Fase",
            "Oitavas de Final",
            "Quartas de Final",
            "Semifinais",
            "Final",
        ]
        numero_fases = [8, 16, 24, 28, 30]

    else:
        fases = ["Única"]
        numero_fases = [380]

    for i in range(len(fases)):
        if numero_jogo <= numero_fases[i]:
            return fases[i]
