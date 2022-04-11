# meteoAltPenedes

## Descripció

Aquesta pràctica s'ha realitzat sota el context de l'assignatura Tipologia i cicle de vida de les dades del màster universitari Ciència de Dades de la UOC.
En ella es treballa la tècnica de web scraping per extreure dades d'una pàgina web i generar un dataset.

En el nostre cas, s'extreuran dades de la pàgina web del Servei Meteorològic de Catalunya, també conegut com ‘meteocat’, la qual proporciona dades diaries capturades desde estacions meteorològiques distribuïdes a tot el territori català.
El dataset generat conté diferents variables meteorològiques registrades diàriament per les estacions situades al Alt Penedes (Sant Sadurní d’Anoia, Sant Martí Sarroca, Canaletes, la Granada i Font Rubí) entre els anys 2017 i 2021.

## Membres del grup
La pràctica ha estat realitzada per l'Albert Estadella Valls i l'Àngels Calvet i Mirabent.

## Codi (meteo_scraping.py)
El codi implementat en Python esta preparat per extreure les dades meteorològiques especificades per l'usuari en funció de l'estació o estacions meteorològiques i el període de temps.

### Requeriments
Instal·lar el webdriver de Chrome, el qual es pot trobar a la pàgina següent: https://chromedriver.chromium.org/

### Variables a modificar
estacions = "" # nom de les estacions desitjades separades per comes, ex: "Sant Sadurní d'Anoia,Sant Martí Sarroca,Canaletes,la Granada,Font-rubí"
dia_inici = '' # data inicial en format DD.MM.AAAA
dia_final = '' # data final en format DD.MM.AAAA
driver_path = '' # directori al webdriver de Chrome
path_results = '' # directori on volem guardar els resultats
