import scrapy
from scrapy.loader import ItemLoader
from soccer_games.items import SoccerGamesItem

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
    for i in range(380)
]


def tratar_hora(hora):
    # Deixar data no padrão do projeto
    if not hora:
        return '00:00'
    return hora


def tratar_data(data):
    if not data:
        return '00/00/0000'
    return data


def rodada_jogo(numero_jogo):
    rodada = numero_jogo // 10
    if numero_jogo % 10 != 0:
        rodada += 1
    return rodada


def tratar_local(local):
    local = local[0].split(' - ')
    if 'a definir' in local[0].lower():
        local *= 3
    return local


class CbfGamesSpider(scrapy.Spider):
    name = 'cbf_games'
    allowed_domains = ['cbf.com.br']
    start_urls = serie_a + serie_b + serie_c

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
        hora_jogo = tratar_hora(response.css('.col-xs-6 .text-6::text').get())
        numero_jogo = int(response.url[-3::])
        nome_campeonato = (
            response.url.split('/')[-3]
            .replace('-', ' ')
            .replace('serie', 'série')
            .title()
        )

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
        jogo.add_value('numero_jogo', numero_jogo)
        jogo.add_value('rodada_jogo', rodada_jogo(numero_jogo))
        jogo.add_value('nome_campeonato', nome_campeonato)

        return jogo.load_item()
