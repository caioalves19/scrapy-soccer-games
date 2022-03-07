# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from ast import ExceptHandler
import json
from itemloaders.processors import Compose, TakeFirst
from scrapy import Field, Item


def tratar_time(time):
    # Tratar nomes dos times para a forma necessária ao projeto
    # Os ajustes estão organizados no arquivo tratar_nomes_times.json

    time = time.split(' - ')
    if 'a definir' in time[0].lower():
        return 'Selecione um clube'
    
    with open('tratar_nomes_times.json', 'r') as f:
        nomes_times = json.load(f)

    if time[0] in nomes_times:
        try:
            return nomes_times[time[0]] + ' - ' + time[1]
        except Exception:
            return nomes_times[time[0]]

    try:
        return time[0] + ' - ' + time[1]
    except Exception:
        return time[0]


def tratar_cidade(cidade):
    # Tratar nomes dos times para a forma necessária ao projeto
    # Os ajustes estão organizados no arquivo tratar_nomes_cidades.json

    with open('tratar_nomes_cidades.json', 'r') as f:
        nomes_cidades = json.load(f)

    if cidade in nomes_cidades:
        return nomes_cidades[cidade]

    return cidade


def tratar_estadio(estadio):
    # Tratar nomes dos times para a forma necessária ao projeto
    # Os ajustes estão organizados no arquivo tratar_nomes_estadios.json

    estadio = estadio.replace('Estádio ', '')
    estadio = estadio.replace('Estadio ', '')
    estadio = estadio.replace('Municipal ', '')
    estadio = estadio.replace('Mun. ', '')
    estadio = estadio.replace('Dr. ', '')
    estadio = estadio.replace('Doutor ', '')
    
    with open('tratar_nomes_estadios.json', 'r') as f:
        nomes_estadios = json.load(f)

    if estadio in nomes_estadios:
        return nomes_estadios[estadio]

    return estadio


class SoccerGamesItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nome_campeonato = Field(output_processor=Compose(TakeFirst(), str.strip))
    
    time_mandante = Field(
        output_processor=Compose(TakeFirst(), str.strip, tratar_time)
    )
    
    time_visitante = Field(
        output_processor=Compose(TakeFirst(), str.strip, tratar_time)
    )
    
    estadio_jogo = Field(
        output_processor=Compose(TakeFirst(), str.strip, tratar_estadio)
    )
    
    cidade_jogo = Field(
        output_processor=Compose(TakeFirst(), str.strip, tratar_cidade)
    )
    
    estado_jogo = Field(output_processor=Compose(TakeFirst(), str.strip))
    data_jogo = Field(output_processor=Compose(TakeFirst(), str.strip))
    hora_jogo = Field(output_processor=Compose(TakeFirst(), str.strip))
    jogo_adiado = Field(output_processor=TakeFirst())
    numero_jogo = Field(output_processor=TakeFirst())
    rodada_jogo = Field(output_processor=TakeFirst())
    fase_jogo = Field(output_processor=TakeFirst())
