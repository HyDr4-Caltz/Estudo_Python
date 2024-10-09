from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from modulos import nascimento, nome, email
import re
from time import sleep
from transformers import pipeline

navegador = None


def inicializar_navegador():
    """Função para inicializar o navegador do Selenium."""
    global navegador
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("user-data-dir=C:/Users/Administrador/AppData/Local/Google/Chrome/User Data")
    chrome_options.add_argument("profile-directory=Default")

    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico, options=chrome_options)
    wait = WebDriverWait(navegador, 200)

    return navegador, wait


def encerrar_bot():
    """Função para encerrar o navegador."""
    global navegador
    if navegador is not None:
        navegador.quit()
        navegador = None
        print("Bot encerrado com sucesso.")
    else:
        print("O bot não está em execução.")


def executar_bot(contato_alvo, subir):
    """Função principal do bot para extrair dados de conversas do WhatsApp."""
    global navegador
    verificar_data = set(open('nascimento.txt', 'r').read().splitlines())
    verificar_email = set(open('emails.txt', 'r').read().splitlines())
    verificar_nomes = set(open('nomes.txt', 'r').read().splitlines())

    nlp = pipeline("ner", model="Davlan/bert-base-multilingual-cased-ner-hrl")

    navegador, wait = inicializar_navegador()

    try:
        alvo = f'"{contato_alvo}"'
        padrao_data = r'\b\d{1,2}/\d{1,2}/\d{4}\b'
        padrao_email = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

        navegador.get("https://web.whatsapp.com")

        caminho_contato = f'//span[contains(@title,{alvo})]'
        contact = wait.until(ec.presence_of_element_located((By.XPATH, caminho_contato)))
        contact.click()

        def rolar_pagina(navegador, subir):
            navegador.find_element(By.TAG_NAME, value="body").click()
            for _ in range(subir):
                navegador.find_element(By.TAG_NAME, value="body").send_keys(Keys.PAGE_UP)
                sleep(2)

        rolar_pagina(navegador, subir)

        messages = navegador.find_elements(By.XPATH, '//div[contains(@class,"message-in")]')
        for message in messages:
            text = message.text
            resultado_data = re.findall(padrao_data, text)
            if resultado_data:
                data_nascimento = resultado_data[0]
                if data_nascimento not in verificar_data:
                    nascimento(data_nascimento)
                    print(f'Data extraída: {data_nascimento}')

            resultado_email = re.findall(padrao_email, text)
            if resultado_email:
                email_encontrado = resultado_email[0]
                if email_encontrado not in verificar_email:
                    email(email_encontrado)
                    print(f'Email extraído: {email_encontrado}')

            resultado = nlp(text)
            for ent in resultado:
                if ent['entity'] == 'PER':
                    nome_detectado = ent['word']
                    if nome_detectado not in verificar_nomes:
                        nome(nome_detectado)
                        print(f'Nome encontrado: {nome_detectado}')

    except Exception as e:
        print(f"Ocorreu um erro durante a execução do bot: {e}")
    finally:
        encerrar_bot()