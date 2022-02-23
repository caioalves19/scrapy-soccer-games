import scrapy
from scrapy.loader import ItemLoader
from soccer_games.items import SoccerGamesItem
from datetime import date


def tratar_hora(hora):
    # Deixar data no padrão do projeto
    if not hora:
        return '00:00'
    return hora


def tratar_data(data):
    if not data:
        return '00/00/0000'
    return data


def rodada_jogo(nome_campeonato, numero_jogo, numero_jogos=10):
    # Usa o número do jogo para descobrir de qual rodada é. O numero_jogos é quantidade de jogos por rodada do campeonato.
    if 'Copa do Nordeste' in nome_campeonato:
        numero_jogos = 8
    if 'Série D' in nome_campeonato:
        numero_jogos = 32
    rodada = numero_jogo // numero_jogos
    if numero_jogo % numero_jogos != 0:
        rodada += 1
    return rodada


def tratar_local(local):
    local = local[0].split(' - ')
    if 'a definir' in local[0].lower():
        local *= 3
    return local


def tratar_nome_campeonato(link_nome):
    if link_nome == 'campeonato-brasileiro-serie-a':
        return 'Campeonato Brasileiro - Série A'
    if link_nome == 'campeonato-brasileiro-serie-b':
        return 'Campeonato Brasileiro - Série B'
    if link_nome == 'campeonato-brasileiro-serie-c':
        return 'Campeonato Brasileiro - Série C'
    if link_nome == 'campeonato-brasileiro-serie-d':
        return 'Campeonato Brasileiro - Série D'
    if link_nome == 'copa-nordeste-masculino':
        return 'Copa do Nordeste - Única'


data_hoje = date.today()

serie_a = [
    f'https://www.cbf.com.br/amp/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/2022/00{i+1}'
    for i in range(380)
]
serie_b = [
    f'https://www.cbf.com.br/amp/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-b/2022/00{i+1}'
    for i in range(380)
]
serie_c = [
    f'https://www.cbf.com.br/amp/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-c/2022/00{i+1}'
    for i in range(190)
]

serie_d = [f'https://www.cbf.com.br/amp/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-d/2022/00{i+25}'
    for i in range(10)]
copa_ne = [
    f'https://www.cbf.com.br/amp/futebol-brasileiro/competicoes/copa-nordeste-masculino/2022/00{i+1}'
    for i in range(68)
]


class CbfGamesSpider(scrapy.Spider):
    name = 'cbf_games'
    allowed_domains = ['cbf.com.br']
    start_urls = serie_d

    def parse(self, response):
        """
        @url https://www.cbf.com.br/amp/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/2022/1
        @returns items 1
        @scrapes time_mandante time_visitante data_jogo hora_jogo
        @scrapes estadio_jogo cidade_jogo estado_jogo numero_jogo
        """
        jogo = ItemLoader(item=SoccerGamesItem(), response=response)

        local_jogo = tratar_local(
            response.css('.col-xs-12 span::text').getall()
        )
        data_jogo = tratar_data(response.css('.col-xs-6 span::text').get())
        data_partida = data_jogo.strip().split('/')
        
        try:
            data_partida = date(int(data_partida[2]), int(data_partida[1]), int(data_partida[0]))
        except Exception:
            data_partida = date(2023, 1, 1)
        
        if data_partida < data_hoje:
                return
        hora_jogo = tratar_hora(response.css('.col-xs-6 .text-6::text').get())
        numero_jogo = int(response.url[-3::])
        nome_campeonato = tratar_nome_campeonato(response.url.split('/')[-3])

        jogo.add_css(
            'time_mandante', '.jogo-equipe-nome-completo::text', lambda v: v[0]
        )
        jogo.add_css(
            'time_visitante',
            '.jogo-equipe-nome-completo::text',
            lambda v: v[1],
        )
        jogo.add_value('estadio_jogo', local_jogo[0])
        jogo.add_value('cidade_jogo', local_jogo[1])
        jogo.add_value('estado_jogo', local_jogo[2])
        jogo.add_value('data_jogo', data_jogo.replace('/', '-'))
        jogo.add_value('hora_jogo', hora_jogo)
        jogo.add_value(
            'rodada_jogo', rodada_jogo(nome_campeonato, numero_jogo)
        )
        jogo.add_value('nome_campeonato', nome_campeonato)

        return jogo.load_item()
