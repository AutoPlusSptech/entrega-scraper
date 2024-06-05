from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import sys
import analise_sentimentos
import levenshtein_g1

if len(sys.argv) > 1:
    flag_trigger = sys.argv[1]
else:
    flag_trigger = False 

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'

class Scrapper:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument(f'user-agent={user_agent}')
        #self.options.add_argument('window-size=1920x1080')
        self.driver = webdriver.Chrome(options=self.options)
    
    def login(self, email, senha, usuario):

        print("Iniciando Scrapper...")

        self.driver.get("https://x.com/")

        time.sleep(3)

        ActionChains(self.driver).scroll_by_amount(0, 500).perform()

        time.sleep(2)

        btnLogin = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div/div/div[3]/div[4]')
        btnLogin.click()

        time.sleep(2)

        campoEmail = self.driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input')
        campoEmail.send_keys(email)

        time.sleep(3)

        avancarSenha = self.driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]')
        avancarSenha.click()

        time.sleep(3)

        campoValidacaoBot = self.driver.find_element(By.XPATH, '//*[@id="modal-header"]/span/span')

        if len(campoValidacaoBot.get_attribute("innerHTML")) > 0:
            print("Bot detectado!")
            time.sleep(3)
            print("Burlando sistema...")
            campoUsuario = self.driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
            campoUsuario.send_keys(usuario)
            time.sleep(3)
            btnAvancar = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button").click()

            print("Sistema burlado com sucesso!")

            time.sleep(2)

        campoSenha = self.driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        campoSenha.send_keys(senha)

        time.sleep(1)

        btnAvancar = self.driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button')
        btnAvancar.click()

        print("Login realizado com sucesso!")

        time.sleep(10)

        print("Redirecionado para o usuário...")

        return self.driver


scp = Scrapper()

driver = scp.login("danylo.gomes@sptech.school", "senhaautoplus", "roberto_aux_scp")

def search_user(driver, user, qtdeTweets = 10):

    driver.get(f'https://twitter.com/{user}')

    time.sleep(8)

    print(f'Coletando {qtdeTweets} tweets do usuário {user}...')

    list_tweets = []
    list_tweets_json = []
    contador_tweets = 0
    texto_ultimo_tweet = ""

    while contador_tweets < qtdeTweets:

        time.sleep(5)

        section_tweets = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/section/div/div/div')

        for index_x, x in enumerate(section_tweets):
            #print(f'Index: {index_x}')
            try:
                texto_tweet = x.find_element(By.XPATH, f'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/section/div/div/div[{index_x + 1}]/div/div/article/div/div/div[2]/div[2]/div[2]/div')
                texto_raw = texto_tweet.get_attribute("innerText")
                texto = texto_raw.replace("\n", "")
                #print(f'{texto}')
                if texto in list_tweets or contador_tweets >= qtdeTweets:
                    #print("Tweet já coletado, ou limite atingido, passando para o próximo...")
                    if contador_tweets >= qtdeTweets:
                        print("Limite de tweets atingido!")
                        break
                    continue
                usuario_tweet = x.find_element(By.XPATH, f'/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div[{index_x + 1}]/div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[1]').get_attribute("innerText")
                #print(f'Usuário: {usuario_tweet}')
                list_tweets.append(texto)
                tweet_json = {
                    "usuario": usuario_tweet,
                    "tweet": texto
                }
                list_tweets_json.append(tweet_json)
                contador_tweets += 1
                texto_ultimo_tweet = texto
            except:
                #print("Erro ao coletar tweet, passando para o próximo...")
                continue

            time.sleep(0.5)

        if contador_tweets < qtdeTweets:
            print("Quantidade de tweets menor que a quantidade solicitada! descendo a página...")

            time.sleep(5)

            try:
                inicial_atual = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div[1]/div/div/article/div/div/div[2]/div[2]/div[2]').get_attribute("innerText").replace("\n", "")
                #print(f'Teste inicial atual {inicial_atual}')
            except:
                #print("Erro ao coletar tweet inicial atual!")
                driver.execute_script("window.scrollBy(0, 300);")
                inicial_atual = ""
                continue

            while texto_ultimo_tweet != inicial_atual:
                driver.execute_script("window.scrollBy(0, 200);")

                try:
                    inicial_atual = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/section/div/div/div[1]/div/div/article/div/div/div[2]/div[2]/div[2]/div').get_attribute("innerText").replace("\n", "")
                except:
                    #print("Erro ao coletar tweet inicial atual!")
                    inicial_atual = ""
                    continue

                time.sleep(1)

    print(f'Quantidade de tweets coletados: {len(list_tweets)}')

    with open('tweets.json', 'w') as file:
        json.dump(list_tweets_json, file, ensure_ascii=False, indent=4)
        
    time.sleep(5)

    driver.quit()

    print("Scrapper encerrado com sucesso!")

    if flag_trigger:
        analise_sentimentos.main()
        levenshtein_g1.main()
    else:
        print("Flag de análise de sentimentos não acionada, encerrando programa...")

search_user(driver, "CETSP_", 20)