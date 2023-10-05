import json


with open("soccer_games/data/ids_campeonatos.json", "r", encoding="utf-8") as f:
    ids_campeonatos = json.load(f)

# Links com todos os campeonatos necessários para scraping da CBF
def criar_link(link):
    return f"https://www.cbf.com.br/futebol-brasileiro/competicoes/{link}/"


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
fem_sub20 = criar_link("campeonato-brasileiro-feminino-sub20")
copa_br = criar_link("copa-brasil-masculino")
copa_br_sub17 = criar_link("copa-brasil-sub17")
copa_br_sub20 = criar_link("copa-brasil-sub20")
copa_ne = criar_link("copa-nordeste-masculino")
copa_verde = criar_link("copa-verde")

links_cbf = [
    copa_br,
    serie_a,
    serie_b,
    serie_c,
    serie_d,
    br_sub17,
    br_sub20,
    copa_br_sub20,
]
# links_cbf = [serie_d]


def obter_rodada_jogo(nome_campeonato, numero_jogo):
    # Usa o número do jogo para descobrir de qual rodada é.
    # [qntde_jogos_rodada, jogos_já_realizados]

    campeonatos = {
        "Copa do Nordeste - Copa do Nordeste -": [1, 70],
        "Brasileirão - Série D": [1, 508],
        "Brasileirão - Série C": [4, 190],
        "Brasileirão - Aspirantes": [2, 56],
        "Brasileirão - Sub-20": [1, 102],
        "Brasileirão - Sub-17": [2, 98],
        "Copa do Brasil - Copa do Brasil -": [1, 120],
        "Brasileirão Feminino - A1": [1, 132],
        "Brasileirão Feminino - A2": [1, 68],
        "Brasileirão Feminino - A3": [1, 60],
        "Brasileirão Feminino - Sub-20": [1, 108],
        "Copa do Brasil Sub-17 - Única": [10, 0],
        "Copa do Brasil Sub-20 - Única": [2, 40],
        "Copa Verde - Única": [1, 29],
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
        "copa-nordeste-masculino": "Copa do Nordeste - Copa do Nordeste -",
        "copa-brasil-masculino": "Copa do Brasil - Copa do Brasil -",
        "campeonato-brasileiro-feminino-a1": "Brasileirão Feminino - A1",
        "campeonato-brasileiro-feminino-a2": "Brasileirão Feminino - A2",
        "campeonato-brasileiro-feminino-a3": "Brasileirão Feminino - A3",
        "campeonato-brasileiro-feminino-sub20": "Brasileirão Feminino - Sub-20",
        "copa-brasil-sub17": "Copa do Brasil Sub-17 - Única",
        "copa-brasil-sub20": "Copa do Brasil Sub-20 - Única",
        "campeonato-brasileiro-sub20": "Brasileirão - Sub-20",
        "campeonato-brasileiro-sub17": "Brasileirão - Sub-17",
        "copa-verde": "Copa Verde - Única",
    }
    return campeonatos.get(link_nome)


def obter_id_campeonato(nome_campeonato):
    id_campeonato = ids_campeonatos.get(nome_campeonato)
    return id_campeonato


def obter_local(response):
    locais_especiais = {
        "Marmudão": ["Marmudão", "Governador Valadares", "MG"],
        "Nogueirão": ["Nogueirão", "Mossoró", "RN"],
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


def tratar_data(data):
    # Deixar data no padrão do projeto
    if not data:
        return "00-00-0000"
    return data.replace("/", "-")


def obter_fase_jogo(numero_jogo, nome_campeonato):
    fases = []

    if "Copa do Brasil Sub-17" in nome_campeonato:
        fases = [
            "1ª Fase",
            "Oitavas de Final",
            "Quartas de Final",
            "Semifinais",
            "Final",
        ]
        numero_fases = [16, 32, 40, 44, 45]

    elif "Copa do Brasil Sub-20" in nome_campeonato:
        fases = [
            "1ª Fase",
            "Oitavas de Final",
            "Quartas de Final",
            "Semifinais",
            "Final",
        ]
        numero_fases = [16, 32, 40, 44, 46]

    elif "Copa do Brasil" in nome_campeonato:
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
        numero_fases = [90, 98, 102, 103]

    elif "Brasileirão - Sub-17" in nome_campeonato:
        fases = ["1ª Fase", "Quartas de Final", "Semifinais", "Final"]
        numero_fases = [90, 98, 102, 104]

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

    elif "Feminino - Sub-20" in nome_campeonato:
        fases = ["1ª Fase", "Quartas de Final", "Semifinais", "Final"]
        numero_fases = [100, 104, 108, 109]

    elif "Campeonato Paulista - Série A1" in nome_campeonato:
        fases = ["1ª Fase", "Quartas de Final", "Semifinais", "Final"]
        numero_fases = [96, 104, 108, 110]

    elif "Série D" in nome_campeonato:
        fases = [
            "1ª Fase",
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
        numero_fases = [8, 16, 25, 29, 31]

    else:
        fases = ["Única"]
        numero_fases = [380]

    for i in range(len(fases)):
        if numero_jogo <= numero_fases[i]:
            return fases[i]
