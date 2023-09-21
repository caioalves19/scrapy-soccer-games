import json
from re import A
from time import sleep
from selenium.webdriver.common.keys import Keys

import scrapy
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from soccer_games.items import SoccerGamesItem
from soccer_games.modulos.modulos import obter_id_campeonato


def nome_time_libertadores(nome_time):
    nomes_times = {'América-MG': 'América - MG', 'Athletico-PR': 'Athletico - PR', 'Atlético-GO': 'Atlético - GO', 'Atlético-MG': 'Atlético - MG', 'Corinthians': 'Corinthians - SP', 'Ceará': 'Ceará - CE', 'Cuiabá': 'Cuiabá - MT',
                   'Flamengo': 'Flamengo - RJ', 'Fluminense': 'Fluminense - RJ', 'Fortaleza': 'Fortaleza - CE', 'Internacional': 'Internacional - RS', 'Palmeiras': 'Palmeiras - SP', 'Red Bull Bragantino': 'Red Bull Bragantino - SP', 'Santos': 'Santos - SP', 'São Paulo': 'São Paulo - SP'}

    if nome_time in nomes_times:
        return nomes_times[nome_time], nomes_times[nome_time].split(' - ')[1]
    return nome_time, ' '


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
        ano = 2024
    else:
        ano = 2023

    data = f'{data[0]}-{data[1]}-{ano}'
    return data, hora, jogo_adiado

# Configuração do campeonato de acordo com o site Flashscore:
# {'país do campeonato': [nome do campeonato no flashscore, nome do campeonato desejado - série do campeonato desejado]}
campeonatos = [
    # {'alemanha': ['bundesliga', 'Alemão - Alemão -']},
    # {'espanha': ['laliga', 'Espanhol - Espanhol -']},
    # {'franca': ['ligue-1', 'Francês - Francês -']},
    # {'inglaterra': ['campeonato-ingles', 'Inglês - Inglês -']},
    {'italia': ['serie-a', 'Italiano - Italiano -']},
    # {
    #     'portugal': [
    #         'liga-portugal',
    #         'Português - Português -',
    #     ]
    # },
    # {'arabia-saudita': ['primeira-liga', 'Saudita - Única']},
]


# campeonatos = [{'america-do-sul': ['copa-sul-americana',
#                                    'Copa Sul-Americana - Única']}]

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
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
driver = Chrome('c:\chromedriver.exe', options=options)
driver.maximize_window()


class FlashscoresGamesSpider(scrapy.Spider):
    name = 'flashscores_games'
    allowed_domains = ['www.flashscore.com.br']
    start_urls = ['https://www.flashscore.com.br']

    def __init__(self):
        f = open(
            'D:\Caio\Projetos-Python\scrapy-soccer-games\\futebol_interior\\flashscore_games.json', 'w').close()
        self.html_lista = []
        self.jogos_detalhados = []
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
            if 'libertadores' in link or 'sul-americana' in link:
                jogos = driver.find_elements(By.CSS_SELECTOR, '.event__match')
                # jogos = jogos[10:15]
                for jogo in jogos:
                    id_jogo = jogo.get_attribute("id").split('g_1_')[1]
                    link = f"https://www.flashscore.com.br/jogo/{id_jogo}"

                    # open tab
                    driver.execute_script(f"window.open('', '_blank');")

                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(link)
                    sleep(4)
                    self.jogos_detalhados.append(driver.page_source)

                    # close the tab
                    # (Keys.CONTROL + 'w') on other OSs.
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

            else:
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
                jogo.add_value('id_campeonato', obter_id_campeonato(nome_campeonato))
            
                if 'RODADA' in todos_jogos[c].upper():
                    rodada = int(todos_jogos[c][-2::])
                    c = c + 1
                    continue

                jogo.add_value('time_mandante', f"{todos_jogos[c + 1]}")
                jogo.add_value('time_visitante', f"{todos_jogos[c + 2]}")

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

        for i in range(len(self.jogos_detalhados)):

            resp = Selector(text=self.jogos_detalhados[i])
            nomes_campeonatos.append(nomes_campeonatos[0])
            nome_campeonato = nomes_campeonatos[i]
            jogo = ItemLoader(item=SoccerGamesItem(), selector=resp)

            times = resp.css('.participant__participantName::text').getall()
            data, hora = resp.css('.duelParticipant__startTime div::text').get().replace(
                '.', '-').split(' ')
            local = resp.css('.mi__item__val::text').getall()
            if local:
                local = local[-1]
                try:
                    local = local.split('Estádio ')[1]
                except Exception:
                    pass
                estadio = local.split(' (')[0]
                cidade = local.split(' (')[1]
                cidade = cidade[:-1]
                pais = times[0].split(' (')[1].upper()
                if pais != 'BRA)':
                    cidade = f"{cidade} ({pais}"
            else:
                estadio = 'A definir'
                cidade = 'A definir'

            time_mandante, estado = nome_time_libertadores(
                times[0].split(' (')[0])
            time_visitante, nada = nome_time_libertadores(
                times[1].split(' (')[0])

            rodada = resp.css(
                '.tournamentHeader__country a::text').get().strip()

            rodada = int(rodada.split('Rodada ')[1].strip())

            jogo.add_value('nome_campeonato', nome_campeonato)
            jogo.add_value('time_mandante', time_mandante)
            jogo.add_value('time_visitante', time_visitante)
            jogo.add_value('estadio_jogo', estadio)
            jogo.add_value('cidade_jogo', cidade)
            jogo.add_value('estado_jogo', estado)
            jogo.add_value('data_jogo', data)
            jogo.add_value('hora_jogo', hora)
            jogo.add_value('fase_jogo', 'Fase de Grupos')
            jogo.add_value('rodada_jogo', rodada)
            jogo.add_value('jogo_adiado', False)

            yield jogo.load_item()
