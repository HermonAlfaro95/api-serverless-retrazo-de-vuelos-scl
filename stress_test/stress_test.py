# imports

# intern
import os

# extern
from locust import HttpUser, task, between


class StressTestUser(HttpUser):
    wait_time = between(0.1, 1)  # Intervalo de espera entre solicitudes
    api_key = os.environ.get("API_KEY", None)
    base_url = "https://dz3vt0hqt5.execute-api.us-east-1.amazonaws.com/Prod/prob_delay"

    @task
    def make_request(self):
        # Definir los parámetros de la solicitud
        params = {
            "dia": "1",
            "mes": "5",
            "temporada_alta": "1",
            "opera": "American Airlines",
            "siglades": "Miami",
            "dianom": "Sabado",
            "periodo_dia": "noche",
            "tipovuelo": "I"
        }

        headers = {
            "x-api-key": self.api_key
        }

        # Realizar una solicitud GET a la API con la API key y los parámetros
        self.client.get(self.base_url, params=params, headers=headers)
