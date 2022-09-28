# Links com todos os campeonatos necessários para scraping da CBF
def criar_link(link):
    return f'https://www.cbf.com.br/futebol-brasileiro/competicoes/{link}/2022'

serie_a = criar_link("campeonato-brasileiro-serie-a")
serie_b = criar_link("campeonato-brasileiro-serie-b")
serie_c = criar_link("campeonato-brasileiro-serie-c")
serie_d = criar_link("campeonato-brasileiro-serie-d")
br_sub20 = criar_link('campeonato-brasileiro-sub20')
br_sub17 = criar_link('campeonato-brasileiro-sub17')
br_aspirantes = criar_link('campeonato-brasileiro-aspirantes')
fem_a1 = criar_link('campeonato-brasileiro-feminino-a1')
fem_a2 = criar_link('campeonato-brasileiro-feminino-a2')
fem_a3 = criar_link('campeonato-brasileiro-feminino-a3')
copa_br = criar_link('copa-brasil-masculino')
copa_br_sub17 = criar_link('copa-brasil-sub17')
copa_ne = criar_link('copa-nordeste-masculino')

links_cbf = [serie_a]

def rodada_jogo(nome_campeonato, numero_jogo):
    # Usa o número do jogo para descobrir de qual rodada é. O quantidade_jogos_rodada é quantidade de jogos por rodada do campeonato.

    campeonatos = {
        'Copa do Nordeste - Copa do Nordeste -': [1, 70],
        'Campeonato Brasileiro - Série D': [2, 504],
        'Campeonato Brasileiro - Série C': [4, 190],
        'Campeonato Brasileiro - Aspirantes': [2, 56],
        'Campeonato Brasileiro - Sub-20': [2, 98],
        'Copa do Brasil - Copa do Brasil -': [2, 116],
        'Campeonato Brasileiro Feminino - A1': [2, 128],
        'Campeonato Brasileiro Feminino - A2': [1, 60],
        'Campeonato Brasileiro Feminino - A3': [1, 60],
        'Copa do Brasil Sub-17 - Única': [16, 16]
    }

    quantidade_jogos_rodada = campeonatos.get(nome_campeonato, [10, 0])[0]

    contagem_jogos_inicial = campeonatos.get(nome_campeonato, [10, 0])[1]

    rodada = (numero_jogo - contagem_jogos_inicial) // quantidade_jogos_rodada

    if (numero_jogo - contagem_jogos_inicial) % quantidade_jogos_rodada != 0:
        rodada += 1

    return rodada

def obter_nome_campeonato(response):
    # Deixar o nome do campeonato no padrão necessário. "Nome do Campeonato - Divisão do Campeonato"
    link_nome = response.url.split('/')[-3]
    campeonatos = {
        'campeonato-brasileiro-aspirantes': 'Campeonato Brasileiro - Aspirantes',
        'campeonato-brasileiro-serie-a': 'Campeonato Brasileiro - Série A',
        'campeonato-brasileiro-serie-b': 'Campeonato Brasileiro - Série B',
        'campeonato-brasileiro-serie-c': 'Campeonato Brasileiro - Série C',
        'campeonato-brasileiro-serie-d': 'Campeonato Brasileiro - Série D',
        'copa-nordeste-masculino': 'Copa do Nordeste - Copa do Nordeste -',
        'copa-brasil-masculino': 'Copa do Brasil - Copa do Brasil -',
        'campeonato-brasileiro-feminino-a1': 'Campeonato Brasileiro Feminino - A1',
        'campeonato-brasileiro-feminino-a2': 'Campeonato Brasileiro Feminino - A2',
        'campeonato-brasileiro-feminino-a3': 'Campeonato Brasileiro Feminino - A3',
        'copa-brasil-sub17': 'Copa do Brasil Sub-17 - Única',
        'campeonato-brasileiro-sub20': 'Campeonato Brasileiro - Sub-20',
        'campeonato-brasileiro-sub17': 'Campeonato Brasileiro - Sub-17',
    }
    return campeonatos.get(link_nome)

def obter_local(response):
    local = response.css('.col-xs-12 span::text').get()
    local = local.split(' - ')
    print(local)
    if 'a definir' in local[0].lower():
        local *= 3
    return local

def tratar_hora(hora):
    # Deixar data no padrão do projeto
    if not hora or 'a definir' in hora.lower():
        return '00:00'
    return hora

def tratar_data(data):
    # Deixar data no padrão do projeto
    if not data:
        return '00-00-0000'
    return data.replace('/', '-')

def obter_fase_jogo(numero_jogo, nome_campeonato):
    fases = []

    if 'Copa do Brasil Sub-17' in nome_campeonato:
        fases = ['Primeira Fase', 'Oitavas de Final',
                 'Quartas de Final', 'Semifinais', 'Final']
        numero_fases = [16, 48, 56, 60, 62]

    elif 'Copa do Brasil' in nome_campeonato:
        fases = [
            'Primeira Fase',
            'Segunda Fase',
            'Terceira Fase',
            'Oitavas de Final',
            'Quartas de Final',
            'Semifinais',
            'Final',
        ]
        numero_fases = [40, 60, 92, 108, 116, 120, 122]

    elif 'Série C' in nome_campeonato:
        fases = ['Primeira Fase', 'Segunda Fase', 'Final']
        numero_fases = [190, 214, 216]

    elif 'Aspirantes' in nome_campeonato:
        fases = ['Fase de Grupos', 'Quartas de Final', 'Semifinais', 'Final']
        numero_fases = [48, 56, 60, 62]

    elif 'Brasileiro - Sub-20' in nome_campeonato:
        fases = ['Fase de Grupos', 'Quartas de Final', 'Semifinais', 'Final']
        numero_fases = [90, 98, 102, 104]

    elif 'Brasileiro - Sub-17' in nome_campeonato:
        fases = ['Primeira Fase']
        numero_fases = [90]

    elif 'Feminino - A1' in nome_campeonato:
        fases = ['Primeira Fase', 'Quartas de Final', 'Semifinais', 'Final']
        numero_fases = [120, 128, 132, 134]

    elif 'Feminino - A2' in nome_campeonato:
        fases = ['Fase de Grupos', 'Quartas de Final', 'Semifinais', 'Final']
        numero_fases = [48, 56, 60, 62]

    elif 'Feminino - A3' in nome_campeonato:
        fases = ['Primeira Fase', 'Oitavas de Final',
                 'Quartas de Final', 'Semifinais', 'Final']
        numero_fases = [32, 48, 56, 60, 62]

    elif 'Campeonato Paulista - Série A1' in nome_campeonato:
        fases = ['Primeira Fase', 'Quartas de Final', 'Semifinais', 'Final']
        numero_fases = [96, 104, 108, 110]

    elif 'Série D' in nome_campeonato:
        fases = ['Fase de Grupos', 'Segunda Fase', 'Oitavas de Final',
                 'Quartas de Final', 'Semifinais', 'Final']
        numero_fases = [448, 480, 496, 504, 508, 510]

    elif 'Copa do Nordeste' in nome_campeonato:
        fases = ['Fase de Grupos', 'Quartas de Final', 'Semifinais', 'Final']
        numero_fases = [64, 68, 70, 72]

    else:
        fases = ['Única']
        numero_fases = [380]

    for i in range(len(fases)):
        if numero_jogo <= numero_fases[i]:
            return fases[i]

