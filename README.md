# scrapy-soccer-games
Esse projeto tem por finalidade pegar informação de tabelas de jogos de futebol de diversos sites. 

As informações incluem nomes dos times, data, hora, local, rodada, entre outros. 

O objetivo inicial não é informações de placar e, sim, para controlar qualquer alteração em datas, horários e locais de jogos futuros.

Spiders:
cbf_games - Pega informações de campeonatos presentes no site da Confederação Brasileira de Futebol (CBF).
fpf_games - Pega informações de campeonatos presentes no site da Federação Paulista de Futebol (FPF).


Exemplo de resultado de um spider:

{
'cidade_jogo': 'Curitiba' <br/>
 'data_jogo': '30/05/2021' <br/>
 'estadio_jogo': 'Arena da Baixada' <br/>
 'estado_jogo': 'PR', #state_game <br/>
 'hora_jogo': '18:15', #hour_game <br/>
 'nome_campeonato': 'Campeonato Brasileiro Série A' <br/>
 'numero_jogo': 8 <br/>
 'rodada_jogo': 1 <br/>
 'time_mandante': 'Athletico - PR' <br/>
 'time_visitante': 'América - MG' <br/>
 }

 INSTRUÇÕES
 O projeto foi criado no Python 3.9.6 e necessita do Scrapy e do Selenium

 O Selinium é usado apenas no fpf_games para lidar com conteúdo gerado por JavaScript

 Para instalação, basta digitar o comando "pip install -r requirements.txt

 Depois, entre na pasta do projeto com "cd soccer_games"

 Para executar um spider basta digitar o comando "scrapy crawl {nome_do_spider}"
