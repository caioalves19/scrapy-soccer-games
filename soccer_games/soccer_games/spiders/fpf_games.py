from lib2to3.pgen2 import driver
from tracemalloc import start
from webbrowser import Chrome
from scrapy.selector import Selector
import scrapy
from selenium.webdriver import Chrome
from shutil import which
from time import sleep


class FpfGamesSpider(scrapy.Spider):
    name = 'fpf_games'
    allowed_domains = ['futebolpaulista.com.br']
    start_urls = ['https://futebolpaulista.com.br/Competicoes/Tabela.aspx?idCampeonato=76&ano=2022&nav=1']

    def __init__(self):
        driver = Chrome("C:/chromedriver.exe")
        driver.get("https://futebolpaulista.com.br/Competicoes/Tabela.aspx?idCampeonato=76&ano=2022&nav=1")
        input('Posso?')

        self.html = driver.page_source
        driver.close()

    def parse(self, response):
        resp = Selector(text=self.html)
        for local in resp.css('#placarEstadio'):
            yield{
                'local': local.css('::text').get()
            }
