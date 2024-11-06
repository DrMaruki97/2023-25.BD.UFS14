import azure.functions as func
import datetime
import json
import logging
import requests as req
from bs4 import BeautifulSoup

app = func.FunctionApp()

@app.route(route="get_main", auth_level=func.AuthLevel.ANONYMOUS)
def get_main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    ingredient_name = req.params.get('ingredient_name')

    if not ingredient_name:

        return func.HttpResponse('Inserire il nome dell\'ingrediente da ricercare nel databse CIR')
        


    if ingredient_name:

        link = ''

        with open('cir_db.json', 'r') as file:
            table = json.load(file)

        for el in table['results'][0]:

            if el['pcpc_ingredientname'] == ingredient_name or el['pcpc_ciringredientname'] == ingredient_name:

                link = f'https://cir-reports.cir-safety.org/cir-ingredient-status-report/?id={el["pcpc_ingredientid"]}'
                payload = {'ingredient_name': ingredient_name,
                           'cir_name': el['pcpc_ciringredientname'],
                           'main_link': link}
                return func.HttpResponse(json.dump(payload),mimetype= 'application/json')
            
            else:
                continue

        if not link:

            return func.HttpResponse({},mimetype='application/json')


    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
    

@app.route(route="get_pdf_link", auth_level=func.AuthLevel.ANONYMOUS)
def get_pdf_link(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}
    url_base = 'https://cir-reports.cir-safety.org/'

    web_page = req.get(req,headers=header)
    page = BeautifulSoup(web_page.text,'html.parser')

    # I link relativi alle fonti sono salvati in tag 'tr' che compongono una tabella, per cui estraiamo solo quelli

    righe = page.find_all('tr')

    # Il primo tr è sempre riservato all'intestazione della tabella, per cui se è presente un solo tr significa
    # che non è presente alcuna fonte per l'ingrediente in esame

    if len(righe)>1:

        # Poichè alcune righe sono popolate da link deprecati, cicliamo su tutte le righe per trovare la prima
        # che presenti un link valido, ovvero iniziante con '../'

        for i in range(1,len(righe)):
            riga = i      
            report = righe[i].a['href']
            if report[0] == '.':
                break

        # Controlliamo che un link valido sia stato trovato

        if report[0] == '.':
                
                # Se in una riga è presente un link valido, componiamo il link definitivo alla fonte e ci salviamo
                # anche la data in cui questa è stata rilasciata e il suo "nome proprio"

                final_url = url_base + report[report.index('/')+1:]
                date = righe[riga].find_all('td')[-1].text
                pdf_name = righe[riga].find_all('td')[-2].text
        else:
            final_url = ''
            date = ''
            pdf_name = ''
    else:
        final_url = ''
        date = ''
        pdf_name = ''

    

    return func.HttpResponse(final_url)


@app.route(route="get_values", auth_level=func.AuthLevel.ANONYMOUS)
def get_values(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

@app.route(route="load_values", auth_level=func.AuthLevel.ANONYMOUS)
def load_values(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')