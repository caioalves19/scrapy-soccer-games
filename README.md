# scrapy-soccer-games
Esse projeto tem por finalidade pegar informação de tabelas de jogos de futebol de diversos sites. 

As informações incluem nomes dos times, data, hora, local, rodada, entre outros. 

O objetivo inicial não é informações de placar e, sim, para controlar qualquer alteração em datas, horários e locais de jogos futuros.

Spiders:
cbf_games - Pega informações de campeonatos presentes no site da Confederação Brasileira de Futebol (CBF).
fpf_games - Pega informações de campeonatos presentes no site da Federação Paulista de Futebol (FPF).
flashscore_games - Pega informações de campeonatos presentes no site Flashscore (antigo resultados.com).


Exemplo de resultado de um spider:

{
'cidade_jogo': 'Curitiba',
 'data_jogo': '30/05/2021',
 'estadio_jogo': 'Arena da Baixada',
 'estado_jogo': 'PR',
 'hora_jogo': '18:15',
 'nome_campeonato': 'Campeonato Brasileiro Série A',
 'numero_jogo': 8,
 'rodada_jogo': 1,
 'time_mandante': 'Athletico - PR',
 'time_visitante': 'América - MG'
 }

 INSTRUÇÕES
 
 O projeto foi criado no Python 3.9.6 e necessita do Scrapy e do Selenium

 O Selenium é usado no fpf_games e flashscore_games para lidar com conteúdo gerado por JavaScript

 Para instalação, basta digitar o comando "pip install -r requirements.txt

 Depois, entre na pasta do projeto com "cd soccer_games"

 Para executar um spider basta digitar o comando "scrapy crawl {nome_do_spider}"
