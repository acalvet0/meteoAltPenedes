#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 15:42:37 2022

@author: albert,angels
"""
#################################################################################################################
############################################  VARIABLES A MODIFICAR  ############################################
#################################################################################################################
estacions = "Sant Sadurní d'Anoia,Sant Martí Sarroca,Canaletes,la Granada,Font-rubí" # Estacions on realitzar l'scraping
dia_inici = '01.01.2017' # Data inicial on començar el web scraping
dia_final = '31.12.2021' # Data final on acabar el web scraping
driver_path = '' # Directori al webdriver de Chrome
# Per descarregar el webdriver de Chrome: https://chromedriver.chromium.org/
path_results = '' # Directori on volem guardar els resultats
#################################################################################################################
#################################################################################################################

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Tractament de dates
from datetime import datetime, timedelta
import pandas as pd


def web_scraping(met_station,day):
        
    ### Eliminar estació seleccionada del buscador
    WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#nom.ui-autocomplete-input'))).clear()
    ### Eliminar data seleccionada del buscador
    WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#datepicker.hasDatepicker'))).clear()
    
    ### Inspeccionant el camp estació, veig que guarda un codi de l'última estació. Aquest codi únicament desapareix en clicar la casella per
    ### seleccionar l'estació, si no la cliquem, sempre busca l'estació del codi intern per molt que modifiquem l'estació en el cercador.
    ### El codi amagat coincideix amb la clau entre [] que es veu a la llista d'estacions de la web
    WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#nom.ui-autocomplete-input'))).click()
    ### Escriu l'estació que volem
    WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#nom.ui-autocomplete-input'))).send_keys(met_station)
    
    ### Solucionat!! Després de cada selecció, s'ha de pressionar el botó enter
    ### Escriu la data que volem i pressionem ENTER per confirmar
    WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#datepicker.hasDatepicker'))).send_keys(day + Keys.ENTER)
    
    ### Fem click al cercador
    WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button#cercaEstacioButton'))).click()
    
    if 'display: block' in  driver.find_element_by_xpath("/html/body/main/div/section/div[1]/div/div/fieldset/div[3]").get_attribute('outerHTML'):
        webtable_df = 'Estació no vàlida'
    else:
        # Quan he corregut la líni em demanava: ImportError: lxml not found, please install it [ho dic per posar-ho com a requeriments]
        webtable_df = pd.read_html(driver.find_element_by_xpath("/html/body/main/div/section/div[2]/div[1]/div/div/table").get_attribute('outerHTML'))[0]
        webtable_df = webtable_df.set_index(0)
    return webtable_df


#################################################################################################################
################################################  MAIN PROGRAM  #################################################
#################################################################################################################
met_stations = estacions.split(',')
time1 = datetime.strptime(dia_inici, "%d.%m.%Y")
time2 = datetime.strptime(dia_final, "%d.%m.%Y")

# Opcions de navegació (per poder inicialitzar el navegador amb extencions deshabilitades, mode incògnit...)
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

driver = webdriver.Chrome(driver_path, chrome_options=options)

# Inicialitzem el navegador
driver.get('https://www.meteo.cat/observacions/xema/dades')

data = pd.DataFrame(index=pd.MultiIndex(levels=[[],[]], codes=[[],[]], names=['Estació meteorològica','Dia']), columns=[])
for met_station in met_stations:
    time = time1
    while time <= time2:
        print("Extraient dades de l'estació de "+met_station+' dia '+time.strftime("%d.%m.%Y"))
        # Extreu els valors de la web (funció web_scripting)
        webtable_df = web_scraping(met_station,time.strftime("%d.%m.%Y"))
        if not isinstance(webtable_df, pd.DataFrame):
            print(webtable_df)
        else:
            # Itera a través de les diferents mesures
            for measure, values in webtable_df.iterrows():
                if "m)" in measure:
                    measure = measure.split('(')[0].strip()
                data.loc[(met_station, time.strftime("%Y.%m.%d")), measure] = values.iloc[0] # omple el dataframe general
                # En el cas que existeixi hora en la mesura:
                if values.iloc[0] != values.iloc[1]:
                    data.loc[(met_station, time.strftime("%Y.%m.%d")), "HORA d'obtenció de " + measure] = values.iloc[1]
        time = time + timedelta(days=1)

data=data.replace(r'^\s*$', 'NA', regex=True)
data.to_csv(path_results+'/dades_meteorologiques.csv')
            
