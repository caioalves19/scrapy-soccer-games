from datetime import date, datetime
from time import sleep
from xmlrpc.client import DateTime

import scrapy
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from selenium.webdriver import Chrome, ChromeOptions

from soccer_games.items import SoccerGamesItem

def obter_fase_jogo(numero_jogo, nome_campeonato):
    # Obtém a fase a qual o jogo pertence de acordo com o número do jogo.

    fases = []
    if 'Campeonato Paulista - Série A1' in nome_campeonato:
        fases = ['Primeira Fase', 'Quartas de Final', 'Semifinais', 'Final']
        numero_fases = [96, 104, 108, 110]
    
    elif 'Campeonato Paulista - Série A2' in nome_campeonato or 'Campeonato Paulista - Série A3' in nome_campeonato:
        fases = ['Primeira Fase', 'Quartas de Final', 'Semifinais', 'Final']
        numero_fases = [120, 128, 132, 134]

    for i in range(len(fases)):
        if numero_jogo <= numero_fases[i]:
            return fases[i]

    return 'Única'

def tratar_locais(locais):
    for i in range(len(locais)):
        locais[i] = locais[i].strip()
    locais = [value for value in locais if value != '']
    estadios = []
    cidades = []
    for i in range(0, len(locais), 3):
        estadios.append(locais[i])
        cidades.append(locais[i + 1])
    return estadios, cidades


data_hoje = date.today()
options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--headless')
driver = Chrome('c:\chromedriver.exe', options=options)
driver.maximize_window()


class FpfGamesSpider(scrapy.Spider):
    name = 'fpf_games'
    allowed_domains = ['futebolpaulista.com.br']
    start_urls = [
        'https://futebolpaulista.com.br/Competicoes/Tabela.aspx?idCampeonato=76&ano=2022&nav=1'
    ]


    def __init__(self):
        f = open('D:\Caio\Projetos-Python\scrapy-soccer-games\\futebol_interior\\fpf_games.json', 'w').close()
        driver.get('https://futebolpaulista.com.br/Competicoes')
        sleep(2)
        btn_aceitar = driver.find_element_by_css_selector('.js-aceitar')
        btn_aceitar.click()

        campeonatos = [
            {
                'nome_campeonato_fpf': 'Paulistão A2',
                'nome_campeonato_correto': 'Campeonato Paulista - Série A2',
                'numero_rodadas': 15,
            }
        ]
        self.html_lista = []
        self.nomes_campeonatos = []
        for campeonato in campeonatos:
            btn_campeonatos = driver.find_elements_by_css_selector(
                '.bt-selecione-comp'
            )[0]
            btn_campeonatos.click()
            sleep(2)
            opcoes_campeonatos = driver.find_element_by_xpath(
                f"//a[@class='itemCampeonatoTabela' and contains(text(), '{campeonato['nome_campeonato_fpf']}')]"
            )
            opcoes_campeonatos.click()
            sleep(2)
            for i in range(campeonato['numero_rodadas']):
            # for i in range(1):
                self.nomes_campeonatos.append(
                    campeonato['nome_campeonato_correto']
                )
                btn_rodadas = driver.find_elements_by_css_selector(
                    '#combo-rodadas .bt'
                )[1]
                btn_rodadas.click()
                sleep(1)

                rodadas = driver.find_elements_by_css_selector(
                    '#combo-rodadas a'
                )
                rodadas = rodadas[-campeonato['numero_rodadas'] : :]

                rodadas[i].click()
                sleep(2)

                btn_impressao = driver.find_element_by_css_selector(
                    '.lnk-impressao'
                )
                btn_impressao.click()
                sleep(2)
                self.html_lista.append(driver.page_source)

                btn_fechar = driver.find_element_by_css_selector(
                    '.close-modal'
                )
                btn_fechar.click()
                sleep(2)
        driver.close()

    def parse(self, response):
        for i in range(len(self.html_lista)):
            resp = Selector(text=self.html_lista[i])

            times_mandantes = resp.css(
                '.tabela-placar .text-right::text'
            ).getall()
            times_visitantes = resp.css(
                '.tabela-placar .text-center+ .time::text'
            ).getall()
            datas = resp.css('.tabela-placar .data::text').getall()
            horarios = resp.css('.tabela-placar .horario::text').getall()
            locais = resp.css('.mais-informacoes::text').getall()
            rodada = resp.css('.titulo-rodada strong::text').getall()
            rodada = int(rodada[0].split('Rodada ')[1])

            locais = tratar_locais(locais)

            nome_campeonato = self.nomes_campeonatos[i]
            print(nome_campeonato)

            for i in range(len(times_mandantes)):
                data_jogo = datas[i].split('/')
                data_jogo = date(
                    int(data_jogo[2]), int(data_jogo[1]), int(data_jogo[0])
                )
                if data_jogo < data_hoje:
                    continue
                
                jogo = ItemLoader(item=SoccerGamesItem(), selector=resp)
                
                jogo.add_value('nome_campeonato', nome_campeonato)
                
                jogo.add_value(
                    'time_mandante', times_mandantes[i].strip() + ' - SP'
                )
                jogo.add_value(
                    'time_visitante', times_visitantes[i].strip() + ' - SP'
                )
                jogo.add_value('estadio_jogo', locais[0][i])
                jogo.add_value('cidade_jogo', locais[1][i])
                jogo.add_value('estado_jogo', 'SP')
                jogo.add_value('data_jogo', datas[i].replace('/', '-'))
                jogo.add_value('hora_jogo', horarios[i].replace('h', ':'))

                jogo.add_value('jogo_adiado', False)
                
                numeros_jogos = resp.css('.jogo::text').getall()
                numeros_jogos.pop(0)
                for n in range(len(numeros_jogos)):
                    numeros_jogos[n] = int(numeros_jogos[n].strip()[-2::])
                numero_jogo = numeros_jogos[i]
                jogo.add_value('numero_jogo', numeros_jogos[i])
                
                jogo.add_value('rodada_jogo', rodada)
                jogo.add_value('fase_jogo', obter_fase_jogo(numero_jogo, nome_campeonato))

                yield jogo.load_item()
