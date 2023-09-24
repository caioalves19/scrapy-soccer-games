# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

with open('soccer_games/data/nomes_times.json', 'r', encoding='utf-8') as file:
        nomes_times = json.load(file)

with open('soccer_games/data/nomes_cidades.json', 'r', encoding='utf-8') as file:
        nomes_cidades = json.load(file)

with open('soccer_games/data/nomes_estadios.json', 'r', encoding='utf-8') as file:
        nomes_estadios = json.load(file)

def tratar_time(time):
    # Tratar nomes dos times para a forma necessária ao projeto
    # Os ajustes estão organizados no arquivo tratar_nomes_times.json
    time = time.lower()
    time = time.split(' - ')
    
    if 'a definir' in time[0]:
        return 'Selecione um clube'

    nome_tratado = nomes_times.get(time[0], time[0])

    if len(time) == 1:
        return nome_tratado
    
    return f"{nome_tratado} - {time[1]}"

def tratar_cidade(cidade):
    # Tratar nomes dos times para a forma necessária ao projeto
    # Os ajustes estão organizados no arquivo tratar_nomes_cidades.json

    return nomes_cidades.get(cidade, cidade)

def tratar_estadio(estadio):
    # Tratar nomes dos times para a forma necessária ao projeto
    # Os ajustes estão organizados no arquivo tratar_nomes_estadios.json

    palavras_comuns = ['Estádio', 'Estadio', 'Municipal', 'Mun.', 'Dr.', 'Doutor', 'Prefeito', 'Deputado', 'Prof.', 'Comendador', 'Professor']

    for palavra in palavras_comuns:
        estadio = estadio.replace(palavra, '').strip()

    return nomes_estadios.get(estadio, estadio)

class SoccerGamesPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        
        for field_name in field_names:
            value = adapter.get(field_name)
            
            if field_name not in ['jogo_rodada', 'numero_jogo', 'rodada_jogo', 'jogo_adiado', 'id_campeonato']:
                adapter[field_name] = value.strip()
        
            if field_name in ['time_mandante', 'time_visitante']:
                 adapter[field_name] = tratar_time(value)

            elif field_name == 'cidade_jogo':
                adapter[field_name] = tratar_cidade(value)
            
            elif field_name == 'estadio_jogo':
                adapter[field_name] = tratar_estadio(value)
        
        return item
