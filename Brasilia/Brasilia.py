import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import ctypes
from datetime import datetime
from random import randint
import sys


def page_wait_chrome_refresh(min, seg, chrome):
    today = datetime.now()
    current_hor = int(today.hour)
    current_min = int(today.minute)
    current_seg = int(today.second)
    horalimite = current_hor

    while (current_min != min or current_seg < seg):
        today = datetime.now()
        current_hor = int(today.hour)
        current_min = int(today.minute)
        current_seg = int(today.second)
        hora = str(current_hor) + ":" + str(current_min) + ":" + str(current_seg)
        print(hora)
        if (current_hor > horalimite):
            print("\nAtingido o horario limite. Esperando data disponivel.\n")
            return
        time.sleep(0.5)

    print("\nRefresh em " + str(current_hor) + ":" + str(current_min) + ":" + str(current_seg) + ".\n")
    chrome.refresh()


def work_in_calendar(chrome):
    if (len(sys.argv) > 1):
        dia_agendamento = int(sys.argv[1])
    else:
        dia_agendamento = input('Digite o dia do agendamento: ')
        dia_agendamento = int(dia_agendamento)

    print("Sera realizada a tentativa de agendamento no dia " + str(dia_agendamento) + ".\n")
    x_path_find = "//*[@value='" + str(dia_agendamento) + "']"

    if (len(sys.argv) > 2):
        rand_seg = int(sys.argv[2])
    else:
        rand_seg = input('Tempo de atualizacao da pagina (s): ')

    rand_seg = int(rand_seg)
    if (rand_seg > 0):
        rand_seg = 60 - rand_seg
        today = datetime.now()
        current_hor = int(today.hour)
        current_min = int(today.minute)
        current_seg = int(today.second)
        print("A pagina ira atualizar em " + str(current_hor) + ":59:" + str(rand_seg) + ".\n")
        page_wait_chrome_refresh(59, rand_seg, chrome)
    else:
        if (rand_seg == 0):
            print("\nRefresh AGORA.\n")
            chrome.refresh()
        else:
            print("\nEsperando data disponivel.\n")

    calendario_list = WebDriverWait(chrome, 900).until(ec.visibility_of_element_located(
        (By.XPATH, x_path_find)));
    today = datetime.now()
    print("Clicado na Data escolhida (" + str(dia_agendamento) + ") em " + str(int(today.hour)) + ":" + str(int(today.minute)) + ":" + str(int(today.second)) + ".")
    calendario_list.click()


def go_to_calendar(chrome):
    botao_login = chrome.find_element_by_id('BtnLogin')
    botao_login.click()
    time.sleep(0.9)

    user_name = chrome.find_element_by_xpath(".//*[@id='UserName']")
    password = chrome.find_element_by_xpath(".//*[@id='Password']")
    captcha = chrome.find_element_by_xpath(".//*[@id='loginCaptcha']")
    user_name.send_keys("jogosteste155@gmail.com") # Login: Email do usuario no Prenota
    password.send_keys("Jogos9495") # Senha: Senha do usuario no Prenota
    captcha.click()
    print("\nDigite o captcha no Prenota! (tempo para digitar: 10s)")
    time.sleep(10)
    botao_confirma = chrome.find_element_by_xpath(".//*[@id='BtnConfermaL']")
    botao_confirma.click()
    time.sleep(1.5)

    botao_escolha_servico = chrome.find_element_by_xpath(".//*[@name='ctl00$repFunzioni$ctl00$btnMenuItem']")
    botao_escolha_servico.click()
    print("Usuario logado com Sucesso.")
    time.sleep(1.5)

    botao_escolha_cidadania = chrome.find_element_by_xpath(
        ".//*[@name='ctl00$ContentPlaceHolder1$rpServizi$ctl02$btnNomeServizio']")
    botao_escolha_cidadania.click()
    print("Escolhida a opcao Cidadania.")
    time.sleep(1.5)

    #botao_escolha_reconhecimento = chrome.find_element_by_xpath(
    #    ".//*[@name='ctl00$ContentPlaceHolder1$rpServizi$ctl01$btnNomeServizio']")
    #botao_escolha_reconhecimento.click()
    #print("Escolhida a opcao Reconhecimento por Descendencia.")
    #time.sleep(1.5)

    #cidade = chrome.find_element_by_xpath(".//*[@name='ctl00$ContentPlaceHolder1$acc_datiAddizionali1$mycontrol1']")
    #cidade.send_keys("511.008.090-90") # Cidade de residencia do requerente
    #nascimento = chrome.find_element_by_xpath(".//*[@name='ctl00$ContentPlaceHolder1$acc_datiAddizionali1$mycontrol2']")
    #nascimento.send_keys("15/06/13") # Data de nascimento do requerente no formato DD/MM/AA
    #parentesco = chrome.find_element_by_xpath(".//*[@name='ctl00$ContentPlaceHolder1$acc_datiAddizionali1$mycontrol3']")
    #parentesco.send_keys("Outro") # Grau de parentesco do requerente com o Dante Causa
    #observacoes = chrome.find_element_by_xpath(".//*[@name='ctl00$ContentPlaceHolder1$acc_datiAddizionali1$txtNote']")
    #observacoes.send_keys("") # Observacoes
    #time.sleep(2)
    botao_continua = chrome.find_element_by_xpath(".//*[@name='ctl00$ContentPlaceHolder1$acc_datiAddizionali1$btnContinua']")
    botao_continua.click()
    print("Preenchidos os campos da Cidadania por Descendencia.\n")

    work_in_calendar(chrome)

    botao_confirma = WebDriverWait(chrome, 900).until(ec.visibility_of_element_located(
        (By.XPATH, "//*[@name='ctl00$ContentPlaceHolder1$acc_Calendario1$repFasce$ctl01$btnConferma']")));
    today = datetime.now()
    print("Clicado no Confirmar em " + str(int(today.hour)) + ":" + str(int(today.minute)) + ":" + str(int(today.second)) + ".\n")
    botao_confirma.click()

    while (1):
        ocupado = WebDriverWait(chrome, 1200).until(
            ec.visibility_of_element_located((By.XPATH, "//h1[contains(text(),'Ocupada por outro')]")));
        today = datetime.now()
        current_hor = int(today.hour)
        current_min = int(today.minute)
        current_seg = int(today.second)
        print("Ocupado! Foi clicado no Confirmar novamente em " + str(current_hor) + ":" + str(current_min) + ":" + str(current_seg) + ".")
        if (len(ocupado.text) > 0):
            botao_confirma = WebDriverWait(chrome, 1200).until(ec.visibility_of_element_located(
                (By.XPATH, "//*[@name='ctl00$ContentPlaceHolder1$acc_Calendario1$repFasce$ctl01$btnConferma']")));
            botao_confirma.click()
        ocupado = None


def open_prenota():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-notifications')
    chrome = webdriver.Chrome(chrome_options=options)
    chrome.maximize_window()
    chrome.get('https://prenotaonline.esteri.it/Login.aspx?cidsede=100060&returnUrl=//')
    return chrome


def main():
    today = datetime.now()
    print("\nAgendamento Prenota Online! " + str(int(today.hour)) + ":" + str(int(today.minute)) + ":" + str(int(today.second)) + "\n")
    chrome = open_prenota()
    go_to_calendar(chrome)

    today = datetime.now()
    print("\nFim do Agendamento em " + str(int(today.hour)) + ":" + str(int(today.minute)) + ":" + str(int(today.second)) + ".\n")
    time.sleep(10000)


main()
