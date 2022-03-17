import json
from time import sleep

import scrapy
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By

from soccer_games.items import SoccerGamesItem


def obter_data_hora(data_hora):
    # 05.03. 11:30
    # "19.03. 12:00 - Adiado"
    jogo_adiado = False
    if 'Adiado' in data_hora:
        jogo_adiado = True

    data_hora = data_hora.split(' - ')[0]

    data, hora = data_hora.split(' ')

    data = data.split('.')
    data.remove('')

    if int(data[1]) < 7:
        ano = 2022
    else:
        ano = 2021

    data = f'{data[0]}-{data[1]}-{ano}'
    return data, hora, jogo_adiado

# Configuração do campeonato de acordo com o site Flashscore: 
# {'país do campeonato': [nome do campeonato no flashscore, nome do campeonato desejado - série do campeonato desejado]}
campeonatos = [
    {'alemanha': ['bundesliga', 'Campeonato Alemão - Campeonato Alemão -']},
    {'argentina': ['liga-profissional', 'Campeonato Argentino - Única']},
    {'espanha': ['laliga', 'Campeonato Espanhol - Campeonato Espanhol -']},
    {'franca': ['ligue-1', 'Campeonato Francês - Campeonato Francês -']},
    {'inglaterra': ['campeonato-ingles', 'Campeonato Inglês - Única']},
    {'italia': ['serie-a', 'Campeonato Italiano - Campeonato Italiano -']},
    {
        'portugal': [
            'liga-portugal',
            'Campeonato Português - Campeonato Português -',
        ]
    },
]
campeonatos = [
    {'inglaterra': ['campeonato-ingles', 'Campeonato Inglês - Única']}
]

links = []
nomes_campeonatos = []
for campeonato in campeonatos:
    for k, v in campeonato.items():
        links.append(
            f'https://www.flashscore.com.br/futebol/{k}/{v[0]}/calendario'
        )
        nomes_campeonatos.append(v[1])

options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--headless')
driver = Chrome('c:\chromedriver.exe', options=options)
driver.maximize_window()


class FlashscoresGamesSpider(scrapy.Spider):
    name = 'flashscores_games'
    allowed_domains = ['www.flashscore.com.br']
    start_urls = ['https://www.flashscore.com.br']
    f = open('D:\Caio\Projetos-Python\scrapy-soccer-games\\futebol_interior\\flashscore_games.json', 'w').close()
    def __init__(self):
        self.html_lista = []
        for link in links:
            driver.get(link)
            sleep(2)

            try:
                botao_popup = driver.find_element(
                    By.ID, 'onetrust-accept-btn-handler'
                )
                botao_popup.click()
            except:
                pass

            while True:
                sleep(2)
                try:
                    botao_mais_jogos = driver.find_element(
                        By.CLASS_NAME, 'event__more'
                    )
                    botao_mais_jogos.click()
                except:
                    break

            self.html_lista.append(driver.page_source)
        driver.close()

    def parse(self, response):

        for i in range(len(self.html_lista)):
            resp = Selector(text=self.html_lista[i])
            nome_campeonato = nomes_campeonatos[i]

            jogos_site = resp.xpath(
                "//div[@class='sportName soccer']//div[@class='event__round event__round--static' or @class='event__time' or @class='event__participant event__participant--home' or @class='event__participant event__participant--away']//text()"
            ).getall()

            todos_jogos = []
            for i in range(len(jogos_site)):
                if 'Adiado' in jogos_site[i]:
                    continue
                try:
                    if 'Adiado' in jogos_site[i + 1]:
                        jogos_site[i] = f'{jogos_site[i]} - Adiado'
                except Exception:
                    pass
                todos_jogos.append(jogos_site[i])

            c = 0
            while c < len(todos_jogos):
                jogo = ItemLoader(item=SoccerGamesItem(), selector=resp)
                jogo.add_value('nome_campeonato', nome_campeonato)

                if 'RODADA' in todos_jogos[c].upper():
                    rodada = int(todos_jogos[c][-2::])
                    c = c + 1
                    continue

                jogo.add_value('time_mandante', todos_jogos[c + 1])
                jogo.add_value('time_visitante', todos_jogos[c + 2])

                jogo.add_value('estadio_jogo', ' ')
                jogo.add_value('cidade_jogo', ' ')
                jogo.add_value('estado_jogo', ' ')

                data, hora, jogo_adiado = obter_data_hora(todos_jogos[c])
                jogo.add_value('data_jogo', data)
                jogo.add_value('hora_jogo', hora)

                jogo.add_value('jogo_adiado', jogo_adiado)

                jogo.add_value('rodada_jogo', rodada)
                jogo.add_value('fase_jogo', 'Única')

                c = c + 3
                yield jogo.load_item()
