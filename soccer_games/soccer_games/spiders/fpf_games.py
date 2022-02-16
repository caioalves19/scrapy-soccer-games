from tracemalloc import start
from webbrowser import Chrome
from scrapy.selector import Selector
import scrapy
from selenium.webdriver import Chrome, ChromeOptions
from shutil import which
from time import sleep

options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = Chrome("C:/chromedriver.exe", options=options)
driver.maximize_window()

class FpfGamesSpider(scrapy.Spider):
    name = 'fpf_games'
    allowed_domains = ['futebolpaulista.com.br']
    start_urls = []

    def __init__(self):
        campeonatos_links = [f'https://futebolpaulista.com.br/Competicoes/Tabela.aspx?idCampeonato={i}&ano=2022&nav=1' for i in [73, 74, 76]]
        
        for campeonato_link in campeonatos_links:
            input('pode? ')
            driver.get(campeonato_link)
            sleep(2)
            try:
                btn_aceitar = driver.find_element_by_css_selector('.js-aceitar')
                btn_aceitar.click()
                sleep(2)
            except Exception:
                pass
            
            # lista_rodadas = driver.find_elements_by_css_selector('.conteudo #combo-rodadas  li')
            
            self.html = driver.page_source
            # for i in range(len(lista_rodadas)):
            #     botao_rodadas.click()
            #     sleep(2)
            #     lista_rodadas[i+1].click()
            #     sleep(2)
            #     btn_impressao = driver.find_element_by_css_selector('.lnk-impressao')
            #     btn_impressao.click()
            #     sleep(2)
            #     self.html = driver.page_source
            #     print('Passei aqui --------------------------------')
        driver.close()

    def parse(self, response):
        resp = Selector(text=self.html)
        for local in resp.css('#placarEstadio'):
            yield{
                'local': local.css('::text').get().strip()
            }
