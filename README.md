# API - Retrazo de vuelos Santiago de Chile

Este repositorio contiene todos los archivos necesarios para poner en producción una API serverless para interactuar con un modelo de predicción de atraso de vuelos con origen Santiago de Chile.

Esto en el contexto del 'Challenge Machine Learning Engineer - NeuralWorks'
## Objetivo

El objetivo principal de este proyecto es poner en producción una API para interactuar con un modelo de machine learning para predecir si un vuelo desde Santiago de Chile experimentará un retraso superior a 15 minutos con base en diferentes variables relacionadas con la fecha, la aerolínea y el tipo de vuelo.

## 

## Índice de Contenido

1. [Selección de Variables](#selección-de-variables)
2. [Variable Target](#variable-target)
3. [Modelación](#modelación)
4. [Puesta en Producción](#puesta-en-producción)
5. [Pruebas de Estrés](#pruebas-de-estrés)
6. [Mejoras](#mejoras)

## Desarrollo del Modelo

### Selección de Variables

Se seleccionaron las siguientes variables del dataset:

- **DIA**: Día del mes.
- **MES OPERA**: Mes de operación del vuelo.
- **SIGLADES**: Sigla de la aerolínea.
- **DIANOM**: Día de la semana.
- **TIPOVUELO**: Tipo de vuelo.

Además, se crearon las siguientes variables sintéticas y se almacenaron bajo la ruta  `datos/features/synthetic_features.csv`:

- **temporada_alta**: Variable que indica si el vuelo se encuentra en temporada alta.
- **periodo_dia**: Variable que indica el período del día en que se realiza el vuelo.

### Variable Target

Se creó la variable target **atraso_15**, que toma el valor de 0 si el vuelo llega dentro de los siguientes 15 minutos a la hora supuesta y 1 si se pasa de 15 minutos.

### Modelación

Se replicó el trabajo del Data Scientist Juan y se siguieron los siguientes pasos para seleccionar el modelo:

1. Modelación Base con Regresión Logística.
2. Modelación con XGBoost, RandomForest y Gradient Boosting.
**Nota: Se testearon los modelos RandomForest y Gradient Boostingdebido a su fama en problemas con clases desbalanceadas**
4. Se seleccionó el modelo RandomForest basado en el mejor rendimiento de F1.
5. Re-entrenamiento del modelo RandomForest con oversampling.
6. Optimización de hiperparámetros mediante RandomSearchCV para abordar el overfitting.
7. Serialización del modelo y compresión para su almacenamiento en la carpeta `lambda_handler/modelos`.
**Nota: Se comprimió el modelo porque github no permitía el tamaño original**

Toda la información de la modelación y selección del modelo se encuentra bajo la ruta `notebooks/Modelo de predicción de retrazo de vuelos.ipynb`

## Puesta en Producción

Se implementó una API serverless en AWS utilizando el AWS Serverless Application Model (SAM) y se automatizó la implementación mediante GitHub Actions. 
Para el desarrollo y puesta en producción de la API se hizo uso del siguiente tutorial: [SAM](https://aws.amazon.com/es/blogs/compute/using-github-actions-to-deploy-serverless-applications/)

El detalle de la configuración de la API se encuentra bajo la ruta ```template.yml``` y el detalle de la configuración de las accciones GitHub ```.github/workflows/sam-pipeline.yml```

El consumo de la API está bajo API Key.

### Parámetros de entrada
| Parámetro          | Descripción                                           |
|--------------------|--------------------------------------------------|
| dia                | Día programado del vuelo             |
| mes          | Mes programado del vuelo               |
| opera           | Nombre de la areolínea        |
| siglades           | Nombre ciudad de destino         |
| dianom             | Nombre del día de la semana del vuelo        |
| tipovuelo          | Tipo de vuelo (N: Nacional o I: Internacional). |
| temporada_alta     | Variable que indica si el vuelo está en temporada alta. |
| periodo_dia        | Variable que indica el período del día en que se realiza el vuelo. |


### Ejemplo consulta
```bash
curl --location --request GET 'https://dz3vt0hqt5.execute-api.us-east-1.amazonaws.com/Prod/prob_delay/?dia=1&mes=5&temporada_alta=1&opera=American Airlines&siglades=Miami&dianom=Sabado&periodo_dia=noche&tipovuelo=I' \
--header 'x-api-key: API_KEY'
```

### Ejemplo respuesta
```bash
{
    "predicción": 0,
    "probabilidad": 0.57,
    "etiqueta": "a la hora"
}
```


## Pruebas de Estrés

Se realizaron pruebas de estrés utilizando Locust en Python para evaluar el rendimiento de la API en condiciones de carga.
El detalle de los resultados están en el reporte bajo la ruta ```stress_test/reportes/reporte_stress_test.pdf ```
**Nota: Utilicé locust porque wrk no funcionó por temas de compatibilidad de configuración con mi PC**

## Mejoras
Se puede seguir mejorando el proyecto bajo los siguientes 3 puntos

### Modelación
Exigir una probabilidad más alta que 0.5 para predicir la clase mayoritaria (sin atraso), y evaluar si eso mejora el score f-1


### Puesta en producción
Usar AWS Organisations para tener un ambiente de desarrollo y un ambiente de producción para el deploy de la API

### Stress test
El stress test arrojó una tasa de falla del 79 %. Habría que realizar una investigación más exhaustiva bajo los siguientes puntos:
- Errores 500
- Optimización de la API usando caché
- Pruebas de estrés incrementales
- Control de errores
- Monitorización continua



---
**Autor**: [Hermon Alfaro]
**Fecha**: [24-09-2023]
