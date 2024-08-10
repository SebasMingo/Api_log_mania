import requests  # Importa la librería requests para hacer solicitudes HTTP
from datetime import datetime, timezone  # Importa datetime para manejar fechas y horas
import random  # Importa random para seleccionar aleatoriamente elementos de una lista
import time  # Importa time para hacer pausas entre envíos de logs

# Configuración para cada servicio
SERVICES = [  # Lista de diccionarios, cada uno representando un servicio con su nombre y token
    {"name": "service1", "token": "token1"},  # Servicio 1 con su nombre y token
    {"name": "service2", "token": "token2"},  # Servicio 2 con su nombre y token
    {"name": "service3", "token": "token3"}   # Servicio 3 con su nombre y token
]

URL = "http://localhost:5000/logs"  # URL del servidor central donde se envían los logs

def generate_log(service_name):
    severities = ["INFO", "ERROR", "DEBUG"]  # Lista de niveles de severidad posibles para los logs
    log = {  # Crea un diccionario con los datos del log
        "timestamp": datetime.now(timezone.utc).isoformat(),  # Fecha y hora actual en formato ISO
        "service_name": service_name,  # Nombre del servicio que genera el log
        "severity": random.choice(severities),  # Selecciona aleatoriamente un nivel de severidad
        "message": f"This is a test log message from {service_name}."  # Mensaje del log
    }
    return log  # Devuelve el diccionario con los datos del log

def send_log(service):
    log_data = generate_log(service["name"])  # Genera un log para el servicio dado
    headers = {"Authorization": service["token"]}  # Configura el encabezado de autorización con el token del servicio
    response = requests.post(URL, headers=headers, json=log_data)  # Envía el log al servidor usando una solicitud POST
    print(f"{service['name']} sent log: {log_data} - Response: {response.status_code}")  # Imprime el resultado del envío

while True:  # Bucle infinito para enviar logs continuamente
    for service in SERVICES:  # Itera sobre cada servicio en la lista
        send_log(service)  # Envía un log desde el servicio actual
        time.sleep(10)  # Espera 10 segundos antes de enviar el próximo log desde el siguiente servicio
    time.sleep(10)  # Espera 10 segundos adicionales antes de comenzar el siguiente ciclo de envío de logs
