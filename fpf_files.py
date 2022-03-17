from time import sleep
from selenium.webdriver import Chrome, ChromeOptions

options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--headless')
driver = Chrome('c:\chromedriver.exe', options=options)
driver.maximize_window()
 
driver.get('https://futebolpaulista.com.br/Competicoes')
sleep(2)
btn_aceitar = driver.find_element_by_css_selector('.js-aceitar')
btn_aceitar.click()

campeonatos = [
    {
        'nome_campeonato_fpf': 'Paulistão A2',
        'nome_campeonato_correto': 'Campeonato Paulista - Série A2',
        'numero_rodadas': 15,
    }
]
for campeonato in campeonatos:
    btn_campeonatos = driver.find_elements_by_css_selector(
        '.bt-selecione-comp'
    )[0]
    btn_campeonatos.click()
    sleep(2)
    opcoes_campeonatos = driver.find_element_by_xpath(
        f"//a[@class='itemCampeonatoTabela' and contains(text(), '{campeonato['nome_campeonato_fpf']}')]"
    )
    opcoes_campeonatos.click()
    sleep(2)
    # for i in range(1):
    for i in range(campeonato['numero_rodadas']):
        btn_rodadas = driver.find_elements_by_css_selector(
            '#combo-rodadas .bt'
        )[1]
        btn_rodadas.click()
        sleep(1)

        rodadas = driver.find_elements_by_css_selector(
            '#combo-rodadas a'
        )
        rodadas = rodadas[-campeonato['numero_rodadas'] : :]

        rodadas[i].click()
        sleep(2)

        btn_impressao = driver.find_element_by_css_selector(
            '.lnk-impressao'
        )
        btn_impressao.click()
        sleep(2)
        
        with open(f'D:\Caio\Projetos-Python\scrapy-soccer-games\\futebol_interior\\fpf_paginas_html\{i}.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)

        btn_fechar = driver.find_element_by_css_selector(
            '.close-modal'
        )
        btn_fechar.click()
        sleep(2)
driver.close()


