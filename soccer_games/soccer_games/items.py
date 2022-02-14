# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item
from itemloaders.processors import TakeFirst, Compose

def tratar_time(time):
    time = time.split(' - ')
    if 'a definir' in time[0].lower():
        return 'Selecione um clube'
    # Tratar nomes para ficar de acordo com o projeto
    # Corrigir erros gramaticais
    nomes_times = {'America': 'América', 'Sampaio Correa': 'Sampaio Corrêa',
                   'Boa': 'Boa Esporte',
                   'Clube de Esportes Uniao': 'União ABC',
                   'Minas Brasilia': 'Minas Brasília',
                   'CEU ABC': 'União ABC',
                   'Goianesia': 'Goianésia', 'Marilia': 'Marília',
                   'Athletico Paranaense': 'Athletico',
                   'Jc Futebol Clube': 'JC', 'Audax': 'Osasco Audax',
                   'Atlético Mineiro': 'Atlético', 'Porto Vitória F. C.': 'Porto Vitória', 'Sociedade Desportiva Paraense Ltda': 'Desportiva', 'Palmas Ltda': 'Palmas', 'Liga Presidente M\u00e9dici': 'Presidente Médici', 'Confianca': 'Confiança', 'Boca Junior': 'Boca Júnior'}

    if time[0] in nomes_times:
        return nomes_times[time[0]] + ' - ' + time[1]

    return time[0] + ' - ' + time[1]


def tratar_cidade(cidade):
    # Corrigir erros gramaticais
    nomes_cidades = {'Sao Paulo': 'São Paulo',
                     'Bento Goncalves': 'Bento Gonçalves',
                     'Itajai': 'Itajaí',
                     'Braganca Paulista': 'Bragança Paulista',
                     'Goiania': 'Goiânia',
                     'Uberlandia': 'Uberlândia',
                     'Goianesia': 'Goianésia',
                     'Florianopolis': 'Florianópolis',
                     'Maceio': 'Maceió', 'São Luis': 'São Luís',
                     'Ribeirao Preto': 'Ribeirão Preto', 'Chapeco': 'Chapecó',
                     'Nova Iguacu': 'Nova Iguaçu', 'Niteroi': 'Niterói',
                     'Macapa': 'Macapá', 'Xanxere': 'Xanxerê',
                     'Maracanau': 'Maracanaú',
                     'Criciuma': 'Criciúma',
                     'Pocos de Caldas': 'Poços de Caldas', 'Rondonopolis':
                     'Rondonópolis', 'Joao Pessoa': 'João Pessoa', 'Belem': 'Belém', 'Brasilia': 'Brasília', 'Cacador': 'Caçador', 'Gravatai': 'Gravataí',
                     'Sao Jose dos Campos': 'São José dos Campos',
                     'Sao Leopoldo': 'São Leopoldo',
                     'Vitoria da Conquista': 'Vitória da Conquista', 'Jarinú': 'Jarinu',
                     'Cuiaba': 'Cuiabá', 'Sao Luis': 'São Luís',
                     'Sao Mateus do Maranhao': 'Sao Mateus do Maranhão',
                     'Patrocinio': 'Patrocínio', 'Jaragua': 'Jaraguá',
                     'Aparecida de Goiania': 'Aparecida de Goiânia', 'Paranagua': 'Paranaguá',
                     'Jaragua do Sul': 'Jaraguá do Sul', 'Paraiso do Tocantins': 'Paraíso do Tocantins', 'Ceara-Mirim': 'Ceará-Mirim', 'Varzea Grande': 'Várzea Grande',
                     'Sao Bernardo do Campo': 'São Bernardo do Campo', 'Tocantinopolis': 'Tocantinópolis'}

    if cidade in nomes_cidades:
        return nomes_cidades[cidade]

    return cidade


def tratar_estadio(estadio):
    # Tratar nomes para ficar de acordo com o projeto
    # Corrigir erros gramaticais
    nomes_estadios = {'Manoel Barradas': 'Barradão',
                      'Ct Rei Pelé': 'CT Rei Pelé',
                      'CAT do Cajú': 'CAT do Caju', 'SESC Alterosas': 'Sesc Alterosas', 'CEFAT': 'Cefat',
                      'Estádio da Gávea': 'Gávea', 'SESC Campestre': 'Sesc Campestre', 'Do Café': 'Estádio do Café', 'Manoel Barretto': 'Barrettão',
                      'Ninho D´águia': "Ninho d'Águia",
                      'Jardim Inamar': 'Distrital do Inamar',
                      'Olimpio Perim': 'Olímpio Perim',
                      'Leão da Estradinha': 'Estradinha', 'Boca do Jacaré / Serejão': 'Serejão',
                      '1º de Maio': 'Primeiro de Maio', 'Jóia da Princesa': 'Joia da Princesa'}

    if estadio in nomes_estadios:
        return nomes_estadios[estadio]

    return estadio


class SoccerGamesItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nome_campeonato = Field(output_processor = Compose(TakeFirst(), str.strip))
    time_mandante = Field(output_processor = Compose(TakeFirst(), str.strip, tratar_time))
    time_visitante = Field(output_processor = Compose(TakeFirst(), str.strip, tratar_time))
    estadio_jogo = Field(output_processor = Compose(TakeFirst(), str.strip, tratar_estadio))
    cidade_jogo = Field(output_processor = Compose(TakeFirst(), str.strip, tratar_cidade))
    estado_jogo = Field(output_processor = Compose(TakeFirst(), str.strip))
    data_jogo = Field(output_processor = Compose(TakeFirst(), str.strip))
    hora_jogo = Field(output_processor = Compose(TakeFirst(), str.strip))
    numero_jogo = Field(output_processor = TakeFirst())
    rodada_jogo = Field(output_processor = TakeFirst())
