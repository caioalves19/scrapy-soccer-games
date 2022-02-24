import json

import scrapy
from scrapy.loader import ItemLoader

from soccer_games.items import SoccerGamesItem


def tratar_hora(hora):
    # Deixar data no padrão do projeto
    if not hora:
        return '00:00'
    return hora


def tratar_data(data):
    # Deixar data no padrão do projeto
    if not data:
        return '00-00-0000'
    return data.replace('/', '-')


def rodada_jogo(nome_campeonato, numero_jogo, quantidade_jogos_rodada=10):
    # Usa o número do jogo para descobrir de qual rodada é. O quantidade_jogos_rodada é quantidade de jogos por rodada do campeonato.
    if 'Copa do Nordeste' in nome_campeonato:
        quantidade_jogos_rodada = 8
    if 'Série D' in nome_campeonato:
        quantidade_jogos_rodada = 32
    rodada = numero_jogo // quantidade_jogos_rodada
    if numero_jogo % quantidade_jogos_rodada != 0:
        rodada += 1
    return rodada


def obter_local(response):
    local = response.css('.col-xs-12 span::text').get()
    local = local.split(' - ')
    print(local)
    if 'a definir' in local[0].lower():
        local *= 3
    return local


def obter_nome_campeonato(response):
    link_nome = response.url.split('/')[-3]
    # Deixar o nome do campeonato no padrão necessário. "Nome do Campeonato - Divisão do Campeonato"
    campeonatos = {
        'campeonato-brasileiro-serie-a': 'Campeonato Brasileiro - Série A',
        'campeonato-brasileiro-serie-b': 'Campeonato Brasileiro - Série B',
        'campeonato-brasileiro-serie-c': 'Campeonato Brasileiro - Série C',
        'campeonato-brasileiro-serie-d': 'Campeonato Brasileiro - Série D',
        'copa-nordeste-masculino': 'Copa do Nordeste - Única',
        'copa-brasil-masculino': 'Copa do Brasil - Única'
    }
    return campeonatos.get(link_nome)


# Links com todos os campeonatos necessários para scraping da CBF
with open('links_cbf.json', 'r') as f:
    links_cbf = json.load(f)


class CbfGamesSpider(scrapy.Spider):
    name = 'cbf_games'
    allowed_domains = ['cbf.com.br']
    start_urls = links_cbf[-2::]

    def parse(self, response):
        # Entra na página inicial de cada campeonato e obtém links de jogos que ainda não aconteceram
        links = response.css('.btn-info::attr(href)').getall()
        
        for link in links:
            # Ajusta o link para aversão amp, página mais organizada para pegar as informações
            link = link.split('br/')
            link = link[0] + 'br/amp/' + link[1]
            yield scrapy.Request(link, callback=self.parse_jogos)

    def parse_jogos(self, response):
        jogo = ItemLoader(item=SoccerGamesItem(), response=response)

        nome_campeonato = obter_nome_campeonato(response)
        jogo.add_value('nome_campeonato', nome_campeonato)

        jogo.add_css(
            'time_mandante', '.jogo-equipe-nome-completo::text', lambda v: v[0]
        )

        jogo.add_css(
            'time_visitante',
            '.jogo-equipe-nome-completo::text',
            lambda v: v[1],
        )

        local_jogo = obter_local(response)
        jogo.add_value('estadio_jogo', local_jogo[0])
        jogo.add_value('cidade_jogo', local_jogo[1])
        jogo.add_value('estado_jogo', local_jogo[2])

        data_jogo = tratar_data(response.css('.col-xs-6 span::text').get())
        jogo.add_value('data_jogo', data_jogo)

        hora_jogo = tratar_hora(response.css('.col-xs-6 .text-6::text').get())
        jogo.add_value('hora_jogo', hora_jogo)

        numero_jogo = int(response.url.split('/')[-1].split('?')[0])
        jogo.add_value(
            'rodada_jogo', rodada_jogo(nome_campeonato, numero_jogo)
        )

        return jogo.load_item()
