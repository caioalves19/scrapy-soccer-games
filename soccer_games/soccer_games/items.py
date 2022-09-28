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
        "AD Centro Olimpico": "Centro Olímpico",
        "Futebol Feminino Campinas": "Campinas",
        "Jundiaí EC": "Jundiaí",
        "AA Flamengo": "Flamengo",
        "AA Portuguesa": "Portuguesa Santista",
        "Abc": "ABC",
        "AC Milan": "Milan",
        "Amazonas Fc": "Amazonas",
        "Andradina EC": "Andradina",
        "A. Lima": "Alianza Lima",
        "AS Roma": "Roma",
        "America": "América",
        "América-MG": "América - MG",
        "América FC SAF": "América",
        "América Fc Saf": "América",
        "Arsenal Sarandí": "Arsenal de Sarandí",
        "Athletico-PR": "Athletico - PR",
        "Associação Atlética Esmac Ananindeua": "Esmac",
        "Associação Desportiva Taubaté": "AD Taubaté",
        "A. A. Esmac": "Esmac",
        "Atlético-MG": "Atlético - MG",
        "Ath. Bilbao": "Athletic Bilbao",
        "Athletico Paranaense": "Athletico",
        "Atl. Madrid": "Atlético de Madrid",
        "Atl. Tucuman": "Atlético Tucumán",
        "Atlético Cearense": "Atlético",
        "Atlético Mineiro": "Atlético",
        "Audax": "Osasco Audax",
        "Bandeirante EC": "Bandeirante",
        "Barcelona SC": "Barcelona",
        "Bayern": "Bayern de Munique",
        "Bielefeld": "Arminia Bielefeld",
        "Boa": "Boa Esporte",
        "Boca Junior": "Boca Júnior",
        "Brasilis FC Ltda": "Brasilis",
        "Bremen": "Werder Bremen",
        "Bétis": "Betis",
        "CEU ABC": "União ABC",
        "CA Joseense": "Joseense",
        "Catanduva FC": "Catanduva",
        "Celta de Vigo": "Celta",
        "Central Cordoba": "Central Córdoba",
        "Cerro Porteno": "Cerro Porteño",
        "Clube de Esportes Uniao": "União ABC",
        "Comercial RP": "Comercial",
        "Comercial FC (Tietê)": "Comercial Tietê",
        "Confianca": "Confiança",
        "Cruzeiro Saf": "Cruzeiro",
        "Cruzeiro SAF": "Cruzeiro",
        "Cuiabá Saf": "Cuiabá",
        "Dep. Cali": "Deportivo Cali",
        "Dep. Tachira": "Deportivo Táchira",
        "Deportivo La Guaira": "La Guaira",
        "Dortmund": "Borussia Dortmund",
        "Esmac Ananindeua": "Esmac",
        "Ec Flamengo de São Pedro": "Flamengo de São Pedro",
        "FC Porto": "Porto",
        "Famalicao": "Famalicão",
        "Ferreira": "Paços de Ferreira",
        "Figueirense Futebol Clube S.a.f": "Figueirense",
        "Figueirense Futebol Clube S.A.F": "Figueirense",
        "Figueirense FC S.A.F": "Figueirense",
        "Figueirense Fc S.a.f": "Figueirense",
        "Frankfurt": "Eintracht Frankfurt",
        "Ge Juventus": "Juventus",
        "GE Osasco": "Grêmio Osasco",
        "General Caballero JLM": "General Caballero",
        "Gimnasia L.P.": "Gimnasia y Esgrima",
        "Gloria": "Glória",
        "Goianesia": "Goianésia",
        "Gremio Anapolis": "Grêmio Anápolis",
        "Grêmio Novorizontino": "Novorizontino",
        "Grêmio São-Carlense": "São-Carlense",
        "Guairena FC": "Guaireña",
        "Hertha": "Hertha Berlin",
        "Ibrachina FC": "Ibrachina",
        "Ind. del Valle": "Independiente del Valle",
        "Ind. Medellín": "Independiente Medellín",
        "Independiente Petroleros": "Independiente Petrolero",
        "Inter": "Internazionale",
        "Inter Bebedouro": "Inter de Bebedouro",
        "Inter Limeira": "Inter de Limeira",
        "Ipora": "Iporá",
        "Jc Futebol Clube": "JC",
        "J. Wilstermann": "Jorge Wilstermann",
        "José Pinheiro Borda": "Beira-Rio",
        "Köln": "Colônia",
        "La Guaira": "Deportivo La Guaira",
        "Leeds": "Leeds United",
        "Legião Futebol Clube": "Legião",
        "Leicester": "Leicester City",
        "Leverkusen": "Bayer Leverkusen",
        "LDU Quito": "LDU",
        "Liga Presidente Médici": "Presidente Médici",
        "Manchester Utd": "Manchester United",
        "Marica": "Maricá",
        "Marilia": "Marília",
        "Maritimo": "Marítimo",
        "Marseille": "Olympique de Marselha",
        "Mauá Futebol": "Mauá",
        "Metropolitano FC": "Metropolitano",
        "Minas Brasilia": "Minas Brasília",
        "Monchengladbach": "Borussia Monchengladbach",
        "Nautico": "Náutico",
        "Nautico Futebol Clube": 'Náutico',
        "Norwich": "Norwich City",
        "Nova Venecia F. C.": "Nova Venécia",
        "Nueve de Octubre": "9 de Outubro",
        "Olimpia Asuncion": "Olimpia",
        "Palmas Ltda": "Palmas",
        "Paraíso Esporte Clube": "Paraíso",
        "Penarol": "Peñarol",
        "Porto Vitória F. C.": "Porto Vitória",
        "Portuguesa Desp": "Portuguesa",
        "Propria": "Propriá",
        "Prospera": "Próspera",
        "Pinda SC": "Pinda",
        "Real Noroeste F. C.": "Real Noroeste",
        "Real Noroeste Capixaba F. C.": "Real Noroeste",
        "Referência FC": "Referência",
        "Salto FC": "Salto",
        "Sampaio Correa": "Sampaio Corrêa",
        "Sant German Academy": "PSG Academy",
        "Sarmiento Junin": "Sarmiento",
        "São Carlos FL": "São Carlos",
        "Schalke": "Schalke 04",
        "Sharjah FC": "Sharjah Brasil",
        "Sheffield Utd": "Sheffield United",
        "Sociedade Desportiva Paraense Ltda": "Desportiva",
        "St. Etienne": "Saint-Etienne",
        "Suzano": "União Suzano",
        "São Bernardo FC": "São Bernardo",
        "Sao Bernardo Fc": "São Bernardo",
        "São José EC": "São José",
        "Talleres Córdoba": "Talleres",
        "Taubaté Futebol Feminino": "AD Taubaté",
        "UA Barbarense": "União Barbarense",
        "Union La Calera": "Unión La Calera",
        "Union Santa Fe": "Unión",
        "U. Católica": "Universidad Católica",
        "Vasco da Gama": "Vasco",
        "Vasco da Gama S.a.f.": "Vasco",
        "Verona": "Hellas Verona",
        "Vitória SC": "Vitória de Guimarães",
        "Vila Nova F. C.": "Vila Nova",
        "Wanderers": "Montevideo Wanderers",
        "Wolves": "Wolverhampton",
        "Ypiranga Clube": "Ypiranga",
        "XV Jaú": "XV de Jaú",
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
        "Anapolis": "Anápolis",
        "Aparecida de Goiania": "Aparecida de Goiânia",
        "Belem": "Belém",
        "Bento Goncalves": "Bento Gonçalves",
        "Braganca": "Bragança",
        "Braganca Paulista": "Bragança Paulista",
        "Brasilia": "Brasília",
        "Cacador": "Caçador",
        "Ceara-Mirim": "Ceará-Mirim",
        "Chapeco": "Chapecó",
        "Criciuma": "Criciúma",
        "Cuiaba": "Cuiabá",
        "Do Trabalhador": "Estádio do Trabalhador",
        "Florianopolis": "Florianópolis",
        "Goianesia": "Goianésia",
        "Goiania": "Goiânia",
        "Gravatai": "Gravataí",
        "Itajai": "Itajaí",
        "Ipora": "Iporá",
        "Jaragua": "Jaraguá",
        "Jaragua do Sul": "Jaraguá do Sul",
        "Jarinú": "Jarinu",
        "Joao Pessoa": "João Pessoa",
        "Macapa": "Macapá",
        "Maceio": "Maceió",
        "Maracanau": "Maracanaú",
        "Mata de Sao Joao": "Mata de São João",
        "Monte Azul": "Monte Azul Paulista",
        "Muriae": "Muriaé",
        "Niteroi": "Niterói",
        "Nova Iguacu": "Nova Iguaçu",
        "Nova Venecia": "Nova Venécia",
        "Paraiso do Tocantins": "Paraíso do Tocantins",
        "Paranagua": "Paranaguá",
        "Patrocinio": "Patrocínio",
        "Pocos de Caldas": "Poços de Caldas",
        "Riachao do Jacuipe": "Riachão do Jacuípe",
        "Ribeirao Preto": "Ribeirão Preto",
        "Rondonopolis": "Rondonópolis",
        "Sao Bernardo do Campo": "São Bernardo do Campo",
        "Sao Jose dos Campos": "São José dos Campos",
        "Sao Leopoldo": "São Leopoldo",
        "Sao Luis": "São Luís",
        "Sao Mateus do Maranhao": "São Mateus do Maranhão",
        "Sao Paulo": "São Paulo",
        "São Luis": "São Luís",
        "Taubate": "Taubaté",
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
        "Alberto J. Armando": "La Bombonera",
        "Antônio Carneiro": "Carneirão",
        "Antonio Gomes Martins": "Fortaleza",
        "Antonio Soares de Oliveira": "Antônio Soares de Oliveira",
        "Antonio Vespucio Liberti": "Monumental de Núñez",
        "Arena Allianz Parque": "Allianz Parque",
        "Boca do Jacaré / Serejão": "Serejão",
        "Brinco de Ouro": "Brinco de Ouro da Princesa",
        "CAT do Cajú": "CAT do Caju",
        "CEFAT": "Cefat",
        "Centro de Treinamento do Guarani F.C.": "CT Guarani",
        "Centro de Formação de Atletas do Red Bull Brasil": "CFA Red Bull Brasil",
        "Ct Rei Pelé": "CT Rei Pelé",
        "Cícero Pompeu de Toledo": "Morumbi",
        "Cidade de Lanús": "La Fortaleza",
        "da Liga Deportiva Universitaria": "Rodrigo Paz Delgado",
        "de El Alto": "El Alto",
        "Do Café": "Estádio do Café",
        "da Gávea": "Gávea",
        "Da Gávea": "Gávea",
        "do Morumbi": "Morumbi",
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
        "Maria Abadia": "Abadião",
        "Ninho D´águia": "Ninho d'Águia",
        "Olimpio Perim": "Olímpio Perim",
        "Orlando Batista Novelli": "Arena Barueri",
        "Oswaldo Teixeira Duarte": "Canindé",
        "Polideportivo de Pueblo Nuevo": "Pueblo Nuevo",
        "Raimundo Sampaio": "Independência",
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
        output_processor=Compose(TakeFirst(), tratar_estadio)
    )

    cidade_jogo = Field(
        output_processor=Compose(TakeFirst(), tratar_cidade)
    )

    estado_jogo = Field(output_processor=Compose(TakeFirst()))
    data_jogo = Field(output_processor=Compose(TakeFirst(), str.strip))
    hora_jogo = Field(output_processor=Compose(TakeFirst(), str.strip))
    jogo_adiado = Field(output_processor=TakeFirst())
    numero_jogo = Field(output_processor=TakeFirst())
    rodada_jogo = Field(output_processor=TakeFirst())
    fase_jogo = Field(output_processor=TakeFirst())
