################################################################################# 
# OBJETIVOS DO PROJETO 
################################################################################# 
#Vamos fazer uma raspagem de preços pesquisados no site da OLX e alimentar um arquivo CSV com  
#o título, preço anunciado e o link do anúncio. 
 
##################################################################################  
# 1) Requerimentos do projeto  
##################################################################################  
# from ast import arguments  
from datetime import date 
import pyautogui 
# from tkinter import Radiobutton  
from selenium import webdriver #selenium 4 -   
from selenium.webdriver.chrome.service import Service as ChromeService #utilizado para podermos  
from time import sleep #para pausar a operação 
from webdriver_manager.chrome import ChromeDriverManager # Para não termos ue ficar gerenciando as atualizações do google chrome - ESSENCIAL!  
from selenium.webdriver.chrome.options import Options #estabelecimento de parâmetros para o navegador a ser aberto  
from selenium.webdriver.common.by import By #para a funcionalidade de identificação de elemento pelo ID.  
# import os  
from selenium.webdriver.support.wait import WebDriverWait as ww
from selenium.webdriver.support import expected_conditions as ec

##################################################################################  
# 2) Configurações do Browser - DRIVER  
##################################################################################  
  
#2.1) Definindo as configurações do browser que serão utilizadas  
  
# --start-maximized # Inicia maximizado  
# --lang=pt-BR # Define o idioma de inicialização, # en-US , pt-BR  
# --incognito # Usar o modo anônimo  
# --window-size=800,800 # Define a resolução da janela em largura e altura  
# --headless # Roda em segundo plano(com a janela fechada)  
# --disable-notifications # Desabilita notificações  
# --disable-gpu # Desabilita renderização com GPU  
  
#Estrutura do Driver  
def iniciar_driver():  
    chrome_options = Options()  
    arguments = ['--lang=pt-BR', '--window-size=1400,1100', '--incognito']# 'headless'    
    #Adicionando ao chrome_options os argumentos parametrizados  
    for argument in arguments:  
        chrome_options.add_argument(argument)  
  
    #2.2) Adicionalmente, vamos inserir algumas configurações experimentais:  
    chrome_options.add_experimental_option('prefs', {  
        # Alterar o local padrão de download de arquivos - não será mais na pasta download  
        'download.default_directory': 'C:\\Users\\chico\\Projetos_DS\\Mestre_automacao\\Projetos_Selenium\\Downloads_projetos',  
        # notificar o google chrome sobre essa alteração acima realizada - deve ser utilizado em conjunto com a função acima.  
        'download.directory_upgrade': True,  
        # Desabilitar a confirmação de download - funções essenciais para evitar quebras de automação  
        'download.prompt_for_download': False,  
        # Desabilitar notificações do navegador - funções essenciais para evitar quebras de automação  
        'profile.default_content_setting_values.notifications': 2,  
        # Permitir multiplos downloads - para fazer webscraping de sites - imagens ou elementos  
        'profile.default_content_setting_values.automatic_downloads': 1,  
    })  
    #Inicializando o webdriver, que é um simulador de navegador - e fazendo a instalação das dependências - simulador motorista  
    driver = webdriver.Chrome(service=ChromeService(  
        ChromeDriverManager().install()), options=chrome_options) #com isso estamos indo até as dependências do google chrome e fazendo a instalação do webdriver para a versão correta do chrome que temos instalada  
  
    return driver  
  
##################################################################################  
# 3) Execução do projeto - raspagem no site da OLX - passo a passo 
##################################################################################  
 
# criando a feature data_atual para utilizar na nomeação do arquivo 
data_atual = date.today() 
 
#Caixa de armazenamento do item e do estado a ser pesquisado 
pesquisa_item = pyautogui.prompt(text='O que você deseja pesquisar?', title='Item a ser pesquisado') 
pesquisa_estado = pyautogui.prompt(text='Em qual estado você deseja realizar a pesquisa? Use As iniciais maiúsculas. Ex: São Paulo', title='Estado da pesquisa') 

#iniciando o driver 
driver = iniciar_driver()  
 
#3.1) Abrindo o navegador e indo até a seguinte página - olx 
driver.get('https://www.olx.com.br') 

#3.2) Encontrando o campo de pesquisa e clicando
pesquisa_campo = ww(driver, 10).until(ec.presence_of_element_located((By.ID, 'searchtext-input')))
pesquisa_campo.send_keys(pesquisa_item) 
sleep(1) 
botao_pesquisa = driver.find_element(By.XPATH, '//button[@class="search-button-submit"]' )
botao_pesquisa.click() 
sleep(1) 
 
# Selecionando a localidade
local = ww(driver, 10).until(ec.presence_of_element_located((By.XPATH, f'//a[text()="{pesquisa_estado}"]')))
local.click()

# LAÇO DE REPETIÇÃO PARA TODAS AS PÁGINAS 
while True: 
    #3.4)Carregar e fazer com que o site desça até o final e suba até o início para a leitura de todo o site 
    #Descer 
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') 
    sleep(1) 

    #3.5) Encontrar os títulos dos anúncios - procurei os elementos em comum e testei eles com o ctrl+f montando o xpath 
    #Essa é a parte mais importante desse projeto. Temos que encontrar o xpath em comum de todos os itens a serem raspados, INCLLUSIVE OS ANÚNCIOS EM DESTAQUE NO CASO DA OLX 
    titulo = driver.find_elements(By.XPATH, "//div[@class='sc-12rk7z2-7 kDVQFY']//h2")
    
    titulo = driver.find_elements(By.XPATH, "//div[@class='sc-12rk7z2-7 kDVQFY']//div//h2") 
   
    #3.6) Encontrar os preços - procurei os elementos em comum e testei eles com o ctrl+f montando o xpath 
    preco = driver.find_elements(By.XPATH, "//div[@class='sc-1kn4z61-1 dGMPPn']//span") 
    
    #3.7) Encontrar os links - procurei os elementos em comum e testei eles com o ctrl+f montando o xpath 
    link = driver.find_elements(By.XPATH, "//a[@data-lurker-detail='list_id']")
    sleep(1) 
    #3.8) Guardar o resultado da raspagem em um arquivo .csv = a função zip é para trabalhar com várias listas ao mesmo tempo 
    for titulo, preco, link in zip(titulo, preco, link): 
        with open(f'Preços - {pesquisa_item + " - " + pesquisa_estado + " - " + str(data_atual)}.csv', 'a', encoding='utf-8', newline='') as arquivo:#'a' - para acrescentar, 'newline='' para não atribuirmos nenhum espaço entre linhas' 
            link_processado = link.get_attribute('href')#para pegarmos os links usamos o get_attribute 
            arquivo.write(f'{titulo.text};{preco.text};{link_processado}{os.linesep}')# gerando o arquivo com o ; para separar - o text é para qque peguemos apenas o que é texto no elemento - os-linesep para dar a quebra das linhas a cada linha (exige import os) 
    
    sleep(1) 
 
    #3.9) Fazer esse processo para todas as páginas que contenham resultado de pesquisa 
    # clicando nos botões ao final das páginas para ir até a próxima página 
    #tratando exceção para quando chegar na última página e não tiver mais a próxima página 
    try: 
        proxima_pagina = driver.find_element(By.XPATH, "//span[text()='Próxima pagina']")
        sleep(1)
        proxima_pagina.click() 
    except: 
        break #pausando o looping 
     
# Encerrando o projeto 
driver.close()