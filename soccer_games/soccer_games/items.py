# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from itemloaders.processors import Compose, TakeFirst
from scrapy import Field, Item


def tratar_time(time):
    # Tratar nomes dos times para a forma necessária ao projeto
    # Os ajustes estão organizados no arquivo tratar_nomes_times.json

    time = time.split(' - ')
    if 'a definir' in time[0].lower():
        return 'Selecione um clube'
    
    nomes_times = {
    "AA Portuguesa": "Portuguesa Santista",
    "AC Milan": "Milan",
    "AS Roma": "Roma",
    "America": "América",
    "Arsenal Sarandí": "Arsenal de Sarandí",
    "Associação Atlética Esmac Ananindeua": "Esmac",
    "Ath. Bilbao": "Athletic Bilbao",
    "Athletico Paranaense": "Athletico",
    "Atl. Madrid": "Atlético de Madrid",
    "Atl. Tucuman": "Atlético Tucumán",
    "Atlético Mineiro": "Atlético",
    "Audax": "Osasco Audax",
    "Bandeirante EC": "Bandeirante",
    "Bayern": "Bayern de Munique",
    "Bielefeld": "Arminia Bielefeld",
    "Boa": "Boa Esporte",
    "Boca Junior": "Boca Júnior",
    "Bremen": "Werder Bremen",
    "Bétis": "Betis",
    "CEU ABC": "União ABC",
    "Celta de Vigo": "Celta",
    "Central Cordoba": "Central Córdoba",
    "Clube de Esportes Uniao": "União ABC",
    "Comercial RP": "Comercial",
    "Confianca": "Confiança",
    "Cruzeiro Saf": "Cruzeiro",
    "Cuiabá Saf": "Cuiabá",
    "Dortmund": "Borussia Dortmund",
    "Esmac Ananindeua": "Esmac",
    "FC Porto": "Porto",
    "Famalicao": "Famalicão",
    "Ferreira": "Paços de Ferreira",
    "Figueirense Futebol Clube S.a.f": "Figueirense",
    "Frankfurt": "Eintracht Frankfurt",
    "Gimnasia L.P.": "Gimnasia y Esgrima",
    "Gloria": "Glória",
    "Goianesia": "Goianésia",
    "Gremio Anapolis": "Grêmio Anápolis",
    "Grêmio Novorizontino": "Novorizontino",
    "Hertha": "Hertha Berlin",
    "Inter": "Internazionale",
    "Inter Limeira": "Inter de Limeira",
    "Jc Futebol Clube": "JC",
    "Köln": "Colônia",
    "Leeds": "Leeds United",
    "Leicester": "Leicester City",
    "Leverkusen": "Bayer Leverkusen",
    "Liga Presidente Médici": "Presidente Médici",
    "Manchester Utd": "Manchester United",
    "Marica": "Maricá",
    "Marilia": "Marília",
    "Maritimo": "Marítimo",
    "Marseille": "Olympique de Marselha",
    "Minas Brasilia": "Minas Brasília",
    "Monchengladbach": "Borussia Monchengladbach",
    "Nacional": "Nacional da Madeira",
    "Norwich": "Norwich City",
    "Nova Venecia F. C.": "Nova Venécia",
    "Palmas Ltda": "Palmas",
    "Porto Vitória F. C.": "Porto Vitória",
    "Portuguesa Desp": "Portuguesa",
    "Real Noroeste F. C.": "Real Noroeste",
    "Sampaio Correa": "Sampaio Corrêa",
    "Sarmiento Junin": "Sarmiento",
    "Schalke": "Schalke 04",
    "Sheffield Utd": "Sheffield United",
    "Sociedade Desportiva Paraense Ltda": "Desportiva",
    "St. Etienne": "Saint-Etienne",
    "Suzano": "União Suzano",
    "São Bernardo FC": "São Bernardo",
    "São José EC": "São José",
    "Talleres Córdoba": "Talleres",
    "Union Santa Fe": "Unión",
    "Vasco da Gama": "Vasco",
    "Verona": "Hellas Verona",
    "Vitória SC": "Vitória de Guimarães",
    "Wolves": "Wolverhampton",
    "XV Piracicaba": "XV de Piracicaba"
}

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

    nomes_cidades = {
    "Aguia Branca": "Águia Branca",
    "Aparecida de Goiania": "Aparecida de Goiânia",
    "Belem": "Belém",
    "Bento Goncalves": "Bento Gonçalves",
    "Braganca Paulista": "Bragança Paulista",
    "Brasilia": "Brasília",
    "Cacador": "Caçador",
    "Ceara-Mirim": "Ceará-Mirim",
    "Chapeco": "Chapecó",
    "Criciuma": "Criciúma",
    "Cuiaba": "Cuiabá",
    "Florianopolis": "Florianópolis",
    "Goianesia": "Goianésia",
    "Goiania": "Goiânia",
    "Gravatai": "Gravataí",
    "Itajai": "Itajaí",
    "Jaragua": "Jaraguá",
    "Jaragua do Sul": "Jaraguá do Sul",
    "Jarinú": "Jarinu",
    "Joao Pessoa": "João Pessoa",
    "Macapa": "Macapá",
    "Maceio": "Maceió",
    "Maracanau": "Maracanaú",
    "Monte Azul": "Monte Azul Paulista",
    "Niteroi": "Niterói",
    "Nova Iguacu": "Nova Iguaçu",
    "Nova Venecia": "Nova Venécia",
    "Paraiso do Tocantins": "Paraíso do Tocantins",
    "Paranagua": "Paranaguá",
    "Patrocinio": "Patrocínio",
    "Pocos de Caldas": "Poços de Caldas",
    "Ribeirao Preto": "Ribeirão Preto",
    "Rondonopolis": "Rondonópolis",
    "Sao Bernardo do Campo": "São Bernardo do Campo",
    "Sao Jose dos Campos": "São José dos Campos",
    "Sao Leopoldo": "São Leopoldo",
    "Sao Luis": "São Luís",
    "Sao Mateus do Maranhao": "Sao Mateus do Maranhão",
    "Sao Paulo": "São Paulo",
    "São Luis": "São Luís",
    "Tocantinopolis": "Tocantinópolis",
    "Uberlandia": "Uberlândia",
    "Varzea Grande": "Várzea Grande",
    "Vitoria da Conquista": "Vitória da Conquista",
    "Xanxere": "Xanxerê"
}

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
    
    nomes_estadios = {
    "1º de Maio": "Primeiro de Maio",
    "Ademar Pereira de Barros": "Arena Fonte Luminosa",
    "Antonio Gomes Martins": "Fortaleza",
    "Arena Allianz Parque": "Allianz Parque",
    "Boca do Jacaré / Serejão": "Serejão",
    "CAT do Cajú": "CAT do Caju",
    "CEFAT": "Cefat",
    "Ct Rei Pelé": "CT Rei Pelé",
    "Cícero Pompeu de Toledo": "Morumbi",
    "Do Café": "Estádio do Café",
    "Estádio Beira Rio": "Beira-Rio",
    "Estádio da Gávea": "Gávea",
    "Florestão": "Arena da Floresta",
    "Fonte Luminosa": "Arena Fonte Luminosa",
    "Jardim Inamar": "Distrital do Inamar",
    "Jose Batista Pereira Fernandes": "Arena Inamar",
    "Jóia da Princesa": "Joia da Princesa",
    "Leão da Estradinha": "Estradinha",
    "Manoel Barradas": "Barradão",
    "Manoel Barretto": "Barrettão",
    "Ninho D´águia": "Ninho d'Águia",
    "Olimpio Perim": "Olímpio Perim",
    "Orlando Batista Novelli": "Arena Barueri",
    "Oswaldo Teixeira Duarte": "Canindé",
    "SESC Alterosas": "Sesc Alterosas",
    "SESC Campestre": "Sesc Campestre",
    "Urbano Caldeira": "Vila Belmiro"
}

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
