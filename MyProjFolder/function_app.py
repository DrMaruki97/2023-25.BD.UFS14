import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
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
                return func.HttpResponse(f'Pagina CIR dell\'ingrediente richiesto: {link}')
            
            else:
                continue

        if not link:

            return func.HttpResponse(f'Impossibile trovare una pagine per l\'ingrediente {ingredient_name}')


    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )