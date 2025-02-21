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
    user_name.send_keys("jogosteste16@gmail.com") # Login: Email do usuario no Prenota
    password.send_keys("MyPassword") # Senha: Senha do usuario no Prenota
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

    botao_escolha_visita = chrome.find_element_by_xpath(".//*[@name='ctl00$ContentPlaceHolder1$rpServizi$ctl01$btnNomeServizio']")
    botao_escolha_visita.click()
    print("Escolhida a opcao Visita.")
    time.sleep(1.5)

    passaporte = chrome.find_element_by_xpath(".//*[@name='ctl00$ContentPlaceHolder1$acc_datiAddizionali1$mycontrol1']")
    passaporte.send_keys("AB123456") # Passaporte do requerente
    validade = chrome.find_element_by_xpath(".//*[@name='ctl00$ContentPlaceHolder1$acc_datiAddizionali1$mycontrol2']")
    validade.send_keys("10/10/2025") # Data de validade do passaporte do requerente no formato DD/MM/AA
    endereco = chrome.find_element_by_xpath(".//*[@name='ctl00$ContentPlaceHolder1$acc_datiAddizionali1$mycontrol3']")
    endereco.send_keys("R: Quarenta e Sete N: 30") # Enderço do requerente
    celular = chrome.find_element_by_xpath(".//*[@name='ctl00$ContentPlaceHolder1$acc_datiAddizionali1$mycontrol4']")
    celular.send_keys("11994953124")  # Celular do requerente
    visto = chrome.find_element_by_xpath(".//*[@name='ctl00$ContentPlaceHolder1$acc_datiAddizionali1$mycontrol5']")
    visto.send_keys("1") # Vistos necessários
    cidadania = chrome.find_element_by_xpath(".//*[@name='ctl00$ContentPlaceHolder1$acc_datiAddizionali1$mycontrol6']")
    cidadania.send_keys("Brasileiro")  # Cidadania
    profissao = chrome.find_element_by_xpath(".//*[@name='ctl00$ContentPlaceHolder1$acc_datiAddizionali1$mycontrol7']")
    profissao.send_keys("Carpinteiro")  # Profissão
    time.sleep(1.5)
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
    chrome.get('https://prenotaonline.esteri.it/login.aspx?cidsede=100001&returnUrl=%2F%2F')
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
