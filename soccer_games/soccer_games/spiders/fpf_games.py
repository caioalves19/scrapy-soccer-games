from scrapy.selector import Selector
import scrapy
from selenium.webdriver import Chrome, ChromeOptions
from time import sleep
from soccer_games.items import SoccerGamesItem
from scrapy.loader import ItemLoader


def tratar_locais(locais):
    for i in range(len(locais)):
        locais[i] = locais[i].strip()
    locais = [value for value in locais if value != '']
    estadios = []
    cidades = []
    for i in range(0, len(locais), 3):
        estadios.append(locais[i])
        cidades.append(locais[i+1])
    return estadios, cidades

def rodada_jogo(numero_jogo, nome_campeonato):
    ...


options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = Chrome("C:/chromedriver.exe", options=options)
driver.maximize_window()

class FpfGamesSpider(scrapy.Spider):
    name = 'fpf_games'
    allowed_domains = ['futebolpaulista.com.br']
    start_urls = ['https://futebolpaulista.com.br/Competicoes/Tabela.aspx?idCampeonato=76&ano=2022&nav=1']

    def __init__(self):
        driver.get('https://futebolpaulista.com.br/Competicoes')
        sleep(2)
        btn_aceitar = driver.find_element_by_css_selector('.js-aceitar')
        btn_aceitar.click()

        campeonatos = ['Paulistão Sicredi', 'Paulistão A2', 'Paulistão A3']
        
        for campeonato in campeonatos:
            btn_campeonatos = driver.find_elements_by_css_selector('.bt-selecione-comp')[0]
            btn_campeonatos.click()
            sleep(2)
            opcoes_campeonatos = driver.find_element_by_xpath(f"//a[@class='itemCampeonatoTabela' and contains(text(), '{campeonato}')]")
            opcoes_campeonatos.click()
            input('deu certo?')
            sleep(2)
            self.html_lista = []
            for i in range(1):
                btn_rodadas = driver.find_elements_by_css_selector('#combo-rodadas .bt')[1]
                btn_rodadas.click()
                sleep(1)

                rodadas = driver.find_elements_by_css_selector('#combo-rodadas a')
                rodadas = rodadas[-10::]

                rodadas[i].click()
                sleep(2)

                btn_impressao = driver.find_element_by_css_selector('.lnk-impressao')
                btn_impressao.click()
                sleep(2)
                self.html_lista.append(driver.page_source)

                btn_fechar = driver.find_element_by_css_selector('.close-modal')
                btn_fechar.click()
                sleep(2)
        driver.close()

    def parse(self, response):
        # for local in resp.css('.tabela-placar .text-right'):
        #     yield{
        #         'local': local.css('::text').get().strip()
        #     }
        for i in range(len(self.html_lista)):
            resp = Selector(text=self.html_lista[i])
            

            times_mandantes = resp.css('.tabela-placar .text-right::text').getall()
            times_visitantes = resp.css('.tabela-placar .text-center+ .time::text').getall()
            datas = resp.css('.tabela-placar .data::text').getall()
            horarios = resp.css('.tabela-placar .horario::text').getall()
            locais = resp.css('.mais-informacoes::text').getall()
            numeros = resp.css('.tabela-placar .jogo::text').getall()
            rodada = resp.css('.titulo-rodada strong::text').getall()
            rodada = int(rodada[0].split('Rodada ')[1])

            locais = tratar_locais(locais)
            
            for i in range(8):
                jogo = ItemLoader(item=SoccerGamesItem(), selector=resp)
                jogo.add_value('time_mandante', times_mandantes[i].strip() + ' - SP')
                jogo.add_value('time_visitante', times_visitantes[i].strip() + ' - SP')
                jogo.add_value('estadio_jogo', locais[0][i])
                jogo.add_value('cidade_jogo', locais[1][i])
                jogo.add_value('estado_jogo', 'SP')
                jogo.add_value('data_jogo', datas[i].replace('/', '-'))
                jogo.add_value('hora_jogo', horarios[i].replace('h', ':'))
                jogo.add_value('numero_jogo', int(numeros[i].split('nº')[1].strip()))
                jogo.add_value('rodada_jogo', rodada)
                
                
                yield jogo.load_item()