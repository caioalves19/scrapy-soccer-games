# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import json
from itemloaders.processors import Compose, TakeFirst
from scrapy import Field, Item


class SoccerGamesItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    nome_campeonato = Field(output_processor=TakeFirst())
    id_campeonato = Field(output_processor=TakeFirst())
    time_mandante = Field(output_processor=TakeFirst())
    time_visitante = Field(output_processor=TakeFirst())
    estadio_jogo = Field(output_processor=TakeFirst())
    cidade_jogo = Field(output_processor=TakeFirst())
    estado_jogo = Field(output_processor=TakeFirst())
    data_jogo = Field(output_processor=TakeFirst())
    hora_jogo = Field(output_processor=TakeFirst())
    jogo_adiado = Field(output_processor=TakeFirst())
    numero_jogo = Field(output_processor=TakeFirst())
    rodada_jogo = Field(output_processor=TakeFirst())
    fase_jogo = Field(output_processor=TakeFirst())
