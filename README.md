# scrapy-soccer-games
Esse projeto tem por finalidade pegar informação de tabela de jogos de futebol de diversos sites. As informações incluem nomes dos times, data, hora, local, rodada, entre outros. O objetivo incial não é informações de placar e, sim, para controlar qualquer alteração em datas, horários e locais.

Spiders:

cbf_games - Pega informações de campeonatos presentes no site da Confederação Brasileira de Futebol (CBF).


ENGLISH

This project has the goal to scraping information about soccer games (teams, date, hour, local and so on) from a few websites. The initial intent is control changes on the schedule and not on score. Focused on brazilian soccer games.

Spiders:

cbf_games - Information about games of championships organised by Brazilian Confederation Soccer (CBF, in portuguese).

EXAMPLE OF A GAME SCRAPED FROM cbf_games:

{
'cidade_jogo': 'Curitiba', #city_game<br />
 'data_jogo': '30/05/2021', #date_game<br />
 'estadio_jogo': 'Arena da Baixada', #stadium_game<br />
 'estado_jogo': 'PR', #state_game<br />
 'hora_jogo': '18:15', #hour_game<br />
 'nome_campeonato': 'Campeonato Brasileiro Série A', #name_championship<br />
 'numero_jogo': 8, #number_game<br />
 'rodada_jogo': 1, #round_game<br />
 'time_mandante': 'Athletico - PR', #home_team<br />
 'time_visitante': 'América - MG' #away_team<br />
 }
