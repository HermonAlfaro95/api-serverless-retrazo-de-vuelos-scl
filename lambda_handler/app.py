# imports

# intern
import os
import json
import logging

# extern
import joblib
import numpy as np
import pandas as pd

# SET LOGS
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# CRAGAMOS MODELO FUERA DE LA FUNCIÓN OPTIMIZA EL TIEMPO EN SOLICITUDES RECURRENTES
path_modelo = os.path.join("modelos/modelo_rf.pkl.gz")
modelo = joblib.load(path_modelo)


def lambda_handler(event, context):

    logger.info("AQUI:")
    logger.info(f"event: {type(event)} valores: {event}")
    logger.info(f"context: {type(context)} valores: {context}")

    # init variable de respuesta
    response = {}

    # parametros de entrada para el modelo
    dia = event['queryStringParameters'].get('dia', None)
    mes = event['queryStringParameters'].get('mes', None)
    temporada_alta = event['queryStringParameters'].get('temporada_alta', None)
    tipovuelvo = event['queryStringParameters'].get('tipovuelo', None)
    opera = event['queryStringParameters'].get('opera', None)
    siglades = event['queryStringParameters'].get('siglades', None)
    dianom = event['queryStringParameters'].get('dianom', None)
    periodo_dia = event['queryStringParameters'].get('periodo_dia', None)

    # dataframe para consultar el modelo
    data = pd.DataFrame(
        {
            "DIA": dia,
            "MES": mes,
            "temporada_alta": temporada_alta,
            "TIPOVUELO": tipovuelvo,
            "OPERA": opera,
            "SIGLADES": siglades,
            "DIANOM": dianom,
            "periodo_dia": periodo_dia
        },
        index=[0]
    )

    # predicción
    try:

        # Prediccion
        pred = modelo.predict(data)[0]
        pred_proba = np.max(modelo.predict_proba(data))
        pred_etiqueta = "atrasado" if pred==1 else 0

        # Respuesta modelo
        response = {
            'statusCode': 200,
            'body': json.dumps({'prediccion': int(pred), 'probabilidad': float(pred_proba), 'etiqueta': pred_etiqueta})
        }

    except Exception as e:
        # Hubo algún error durante la predicción
        logger.info(f"Error para los parámetros: {event['queryStringParameters']}: {e}")

        response = {
            'statusCode': 400,
            'body': json.dumps("Bad request check the logs")
        }


    return response
