from datetime import date
from time import sleep


import scrapy
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from selenium.webdriver import Chrome, ChromeOptions

from soccer_games.items import SoccerGamesItem


def obter_fase_jogo(numero_jogo, nome_campeonato):
    # Obtém a fase a qual o jogo pertence de acordo com o número do jogo.

    fases = []
    if 'Paulista - A1' in nome_campeonato:
        fases = ['Fase de Grupos', 'Quartas de Final', 'Semifinais', 'Final']
        numero_fases = [96, 104, 108, 110]

    elif 'Paulista - A2' in nome_campeonato:
        fases = ['1ª Fase', 'Quartas de Final', 'Semifinais', 'Final']
        numero_fases = [120, 128, 132, 134]

    elif 'Paulista - A3' in nome_campeonato:
        fases = ['1ª Fase', '2ª Fase', 'Semifinais', 'Final']
        numero_fases = [120, 144, 148, 150]

    elif 'Paulista - 2ª Divisão' in nome_campeonato:
        fases = ['1ª Fase', '2ª Fase', '3ª Fase']
        numero_fases = [180, 252, 300]

    elif 'Copa Paulista - Única' in nome_campeonato:
        fases = ['1ª Fase', 'Quartas de Final', 'Semifinais', 'Final']
        numero_fases = [90, 98, 102, 104]

    elif 'Paulista Sub-15' in nome_campeonato or 'Paulista Sub-17' in nome_campeonato:
        fases = ['1ª Fase', '2ª Fase', '3ª Fase']
        numero_fases = [370, 466]

    elif 'Paulista Sub-20' in nome_campeonato:
        fases = ['1ª Fase', '2ª Fase', '3ª Fase']
        numero_fases = [390, 486]

    elif 'Paulista Feminino Sub-17' in nome_campeonato:
        fases = ['1ª Fase', 'Quartas de Final', 'Semifinais', 'Final']
        numero_fases = [72, 80, 84, 86]
    
    elif 'Paulista Feminino' in nome_campeonato:
        fases = ['1ª Fase']
        numero_fases = [66]

    elif 'Copa São Paulo Júnior' in nome_campeonato:
        fases = ['Fase de Grupos']
        numero_fases = [192]

    for i in range(len(fases)):
        if numero_jogo <= numero_fases[i]:
            return fases[i]

    return 'Única'


def tratar_locais(locais):
    for local in locais:
        if 'Youtube' in local or 'Paulistão Play' in local or 'Eleven' in local or 'SporTV' in local or 'FPF TV' in local or 'Premiere' in local or 'TNT' in local or 'HBO' in local or 'Record TV' in local or 'HBO Max' in local or 'TV Cultura' in local or 'YouTube Paulistão' in local or 'YouTube Futebol Paulista' in local or 'Estádio TNT Sports' in local or 'Centauro' in local:
            locais.remove(local)

    for i in range(len(locais)):
        locais[i] = locais[i].strip()

    locais = [value for value in locais if value != '']
    estadios = []
    cidades = []

    for i in range(0, len(locais), 2):
        estadios.append(locais[i])
        cidades.append(locais[i + 1])
    return estadios, cidades


data_hoje = date.today()
options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.add_argument('--headless')
driver = Chrome('C:\chromedriver.exe', options=options)
driver.maximize_window()


class FpfGamesSpider(scrapy.Spider):
    name = 'fpf_games'
    # allowed_domains = ['futebolpaulista.com.br']
    start_urls = [
        'https://futebolpaulista.com.br/Competicoes/Tabela.aspx'
    ]

    def __init__(self):
        f = open(
            'D:\Caio\Projetos-Python\scrapy-soccer-games\\futebol_interior\\fpf_games.json', 'w').close()
        driver.get('https://futebolpaulista.com.br/Competicoes')
        sleep(2)
        btn_aceitar = driver.find_element_by_css_selector('.js-aceitar')
        btn_aceitar.click()

        campeonatos = [
            # {
            #     'nome_campeonato_fpf': 'Paulistão Sicredi',
            #     'nome_campeonato_correto': 'Paulista - A1',
            #     'numero_rodadas': 12,
            # },
            # {
            #     'nome_campeonato_fpf': 'Paulistão A2 Kia',
            #     'nome_campeonato_correto': 'Paulista - A2',
            #     'numero_rodadas': 15,
            # },
            # {
            #     'nome_campeonato_fpf': 'Paulistão A3',
            #     'nome_campeonato_correto': 'Paulista - A3',
            #     'numero_rodadas': 2,
            # },
            {
                'nome_campeonato_fpf': 'Paulista Sub-23 2ª Divisão',
                'nome_campeonato_correto': 'Paulista - 2ª Divisão',
                'numero_rodadas': 1,
            },
            # {
            #     'nome_campeonato_fpf': 'Copa Paulista',
            #     'nome_campeonato_correto': 'Copa Paulista - Única',
            #     'numero_rodadas': 10,
            # },
            # {
            #     'nome_campeonato_fpf': 'Paulista Sub-15',
            #     'nome_campeonato_correto': 'Paulista Sub-15 - Paulista Sub-15 -',
            #     'numero_rodadas': 6,
            # },
            # {
            #     'nome_campeonato_fpf': 'Paulista Sub-17',
            #     'nome_campeonato_correto': 'Paulista Sub-17 - Paulista Sub-17 -',
            #     'numero_rodadas': 6,
            # },
            # {
            #     'nome_campeonato_fpf': 'Feminino Sub-17',
            #     'nome_campeonato_correto': 'Paulista Feminino Sub-17 - Paulista Feminino Sub-17 -',
            #     'numero_rodadas': 14,
            # },
            # {
            #     'nome_campeonato_fpf': 'Paulista - SUB20',
            #     'nome_campeonato_correto': 'Paulista Sub-20 - 1ª Divisão',
            #     'numero_rodadas': 6,
            # },
            # {
            #     'nome_campeonato_fpf': 'Feminino Sub-15',
            #     'nome_campeonato_correto': 'Paulista Sub-15 Feminino - Única',
            #     'numero_rodadas': 6,
            # },
            # {
            #     'nome_campeonato_fpf': 'Paulistão Feminino',
            #     'nome_campeonato_correto': 'Paulista Feminino - Paulista Feminino -',
            #     'numero_rodadas': 11,
            # },
            # {
            #     'nome_campeonato_fpf': 'Copa São Paulo Jr.',
            #     'nome_campeonato_correto': 'Copa São Paulo Júnior - Única',
            #     'numero_rodadas': 3,
            # },
            
        ]
        self.html_lista = []
        self.nomes_campeonatos = []
        for campeonato in campeonatos:
            input('posso?')
            btn_campeonatos = driver.find_elements_by_css_selector(
                '.bt-selecione-comp'
            )[0]
            btn_campeonatos.click()
            sleep(2)
            while True:
                opcoes_campeonatos = driver.find_element_by_xpath(
                f"//a[@class='itemCampeonatoTabela' and contains(text(), '{campeonato['nome_campeonato_fpf']}')]"
                )
                break
            opcoes_campeonatos.click()
            sleep(2)
            
            btn_anos = driver.find_element_by_css_selector('.bt.campeonatoData')
            btn_anos.click()
            sleep(2)

            opcoes_anos = driver.find_element_by_xpath(
                f"//a[@class='itemDataCampeonatoTabela' and contains(text(), '2023')]"
            )
            opcoes_anos.click()
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
                rodadas = rodadas[-campeonato['numero_rodadas']::]

                rodadas[i].click()
                sleep(2)

                while True:
                    try:
                        btn_impressao = driver.find_element_by_css_selector(
                        '.lnk-impressao'
                        )
                        btn_impressao.click()
                        break
                    except Exception:
                        continue
                sleep(2)
                self.html_lista.append(driver.page_source)

                btn_fechar = driver.find_element_by_css_selector(
                    '.close-modal'
                )
                btn_fechar.click()
                sleep(2)
        driver.close()

    def parse(self, response):
        def ajuste_rodada(nome_campeonato):
            if nome_campeonato == 'Paulista Sub-15 - Paulista Sub-15 -' or nome_campeonato == 'Paulista Sub-17 - Paulista Sub-17 -' or nome_campeonato == 'Paulista Sub-20 - 1ª Divisão':
                return 10
            elif nome_campeonato == 'Paulista - 2ª Divisão':
                return 16
            elif nome_campeonato == 'Paulista Feminino Sub-17 - Paulista Feminino Sub-17 -':
                return 14
            return 0
        
        for i in range(len(self.html_lista)):
            resp = Selector(text=self.html_lista[i])
            times_mandantes = resp.css(
                '.tabela-placar .text-right::text'
            ).getall()
            print(i)
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

            for i in range(len(times_mandantes)):
                data_jogo = datas[i].split('/')
                data_jogo = date(
                    int(data_jogo[2]), int(data_jogo[1]), int(data_jogo[0])
                )
                if data_jogo < data_hoje or 'FOLGA POR DESISTÊNCIA' in times_mandantes[i].upper() or 'FOLGA POR DESISTÊNCIA' in times_visitantes[i].upper():
                    continue

                jogo = ItemLoader(item=SoccerGamesItem(), selector=resp)

                time_mandante = times_mandantes[i].strip()
                if time_mandante == "Comercial FC (Tietê)":
                    time_mandante = "Comercial Tietê"
                try:
                    time_mandante = time_mandante.split(' (')
                    time_mandante = f'{time_mandante[0].strip()} - {time_mandante[1][:-1]}'
                except Exception:
                    time_mandante = f"{time_mandante[0]} - SP"
                
                time_visitante = times_visitantes[i].strip()
                if time_visitante == "Comercial FC (Tietê)":
                    time_visitante = "Comercial Tietê"
                try:
                    time_visitante = time_visitante.split(' (')
                    time_visitante = f'{time_visitante[0].strip()} - {time_visitante[1][:-1]}'
                except Exception:
                    time_visitante = f"{time_visitante[0]} - SP"

                jogo.add_value('nome_campeonato', nome_campeonato)

                jogo.add_value(
                    'time_mandante', time_mandante
                )
                jogo.add_value(
                    'time_visitante', time_visitante
                )
                jogo.add_value('estadio_jogo', locais[0][i].strip())
                jogo.add_value('cidade_jogo', locais[1][i])
                jogo.add_value('estado_jogo', 'SP')
                jogo.add_value('data_jogo', datas[i].replace('/', '-'))
                jogo.add_value('hora_jogo', horarios[i].replace('h', ':'))

                jogo.add_value('jogo_adiado', False)

                numeros_jogos = resp.css('.jogo::text').getall()
                numeros_jogos.pop(0)
                for n in range(len(numeros_jogos)):
                    numeros_jogos[n] = int(
                        numeros_jogos[n].split('nº')[1].strip())
                numero_jogo = numeros_jogos[i]
                jogo.add_value('numero_jogo', numeros_jogos[i])

                jogo.add_value('rodada_jogo', rodada - ajuste_rodada(nome_campeonato))
                jogo.add_value('fase_jogo', obter_fase_jogo(
                    numero_jogo, nome_campeonato))
                
                yield jogo.load_item()

