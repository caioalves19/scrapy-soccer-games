import json
import scrapy
from scrapy.loader import ItemLoader
from soccer_games.items import SoccerGamesItem
from soccer_games.modulos.modulos import *

class CbfGamesSpider(scrapy.Spider):
    name = 'cbf_games'
    allowed_domains = ['cbf.com.br']
    start_urls = links_cbf

    def parse(self, response):
        f = open(
            'D:\Caio\Projetos-Python\scrapy-soccer-games\\futebol_interior\cbf_games.json', 'w').close()
        # Entra na página inicial de cada campeonato e obtém links de jogos que ainda não aconteceram
        links = response.css('.btn-info::attr(href)').getall()

        for link in links:
            # Ajusta o link para aversão amp, página mais organizada para pegar as informações
            link_num = int(link.split('?')[0].split('/')[-1])
            if link_num > 0:
                link = link.split('br/')
                link = link[0] + 'br/amp/' + link[1]
            yield scrapy.Request(link, callback=self.parse_jogos)

    def parse_jogos(self, response):
        data_jogo = tratar_data(response.css('.col-xs-6 span::text').get())

        jogo = ItemLoader(item=SoccerGamesItem(), response=response)

        nome_campeonato = obter_nome_campeonato(response)
        
        id_campeonato = obter_id_campeonato(nome_campeonato)
        
        jogo.add_value('nome_campeonato', nome_campeonato)
        jogo.add_value('id_campeonato', id_campeonato)

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
        jogo.add_value('estado_jogo', local_jogo[-1])

        numero_jogo = int(response.url.split('/')[-1].split('?')[0])
        rodada_jogo = obter_rodada_jogo(nome_campeonato, numero_jogo)

        hora_jogo = tratar_hora(response.css(
            '.col-xs-6 .text-6::text').get())
        jogo.add_value('hora_jogo', hora_jogo)

        jogo.add_value('jogo_adiado', False)

        

        jogo.add_value('data_jogo', data_jogo)

        jogo.add_value('numero_jogo', numero_jogo)

        jogo.add_value(
            'rodada_jogo', rodada_jogo
        )

        jogo.add_value(
            'fase_jogo', obter_fase_jogo(numero_jogo, nome_campeonato)
        )


        return jogo.load_item()