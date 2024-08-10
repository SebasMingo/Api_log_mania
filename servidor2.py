from flask import Flask, request, jsonify  # Importa Flask, request, y jsonify de Flask
import sqlite3  # Importa sqlite3 para manejar la base de datos SQLite
from datetime import datetime, timezone  # Importa datetime y timezone para manejar fechas y horas

app = Flask(__name__)  # Crea una instancia de la aplicación Flask
# Configura la base de datos
def init_db():
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        service_name TEXT,
        severity TEXT,
        message TEXT,
        received_at TEXT
    )
    ''')
    conn.commit()
    conn.close()

init_db()  # Llama a la función para inicializar la base de datos

# Tokens de autenticación para múltiples servicios
VALID_TOKENS = {
    "service1": "token1",
    "service2": "token2",
    "service3": "token3"
}  # Diccionario que almacena los tokens válidos para cada servicio

def authenticate(token):
    return token in VALID_TOKENS.values()  # Verifica si el token proporcionado es válido

@app.route('/logs', methods=['POST'])
def receive_log():
    token = request.headers.get('Authorization')  # Obtiene el token de autorización del encabezado de la solicitud
    if not authenticate(token):  # Si el token no es válido, retorna un error de autorización
        return jsonify({"error": "Unauthorized"}), 401

    log_data = request.json  # Obtiene los datos del log en formato JSON
    timestamp = log_data.get('timestamp')  # Obtiene la marca de tiempo del log
    service_name = log_data.get('service_name')  # Obtiene el nombre del servicio que envió el log
    severity = log_data.get('severity')  # Obtiene la severidad del log
    message = log_data.get('message')  # Obtiene el mensaje del log
    
    # Usa datetime.now(timezone.utc) para obtener la hora actual en UTC
    received_at = datetime.now(timezone.utc).isoformat()  # Obtiene la fecha y hora actuales en formato ISO en UTC

    try:
        conn = sqlite3.connect('logs.db')  # Conecta a la base de datos 'logs.db'
        cursor = conn.cursor()  # Crea un cursor para ejecutar comandos SQL
        cursor.execute('''
        INSERT INTO logs (timestamp, service_name, severity, message, received_at)
        VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, service_name, severity, message, received_at))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        conn.close()

    return jsonify({"status": "Log received"}), 200

@app.route('/logs', methods=['GET'])
def get_logs():
    start_date = request.args.get('start_date')  # Obtiene la fecha de inicio desde los parámetros de la URL
    end_date = request.args.get('end_date')  # Obtiene la fecha de fin desde los parámetros de la URL
    conn = sqlite3.connect('logs.db')  # Conecta a la base de datos 'logs.db'
    cursor = conn.cursor()  # Crea un cursor para ejecutar comandos SQL
    query = 'SELECT * FROM logs WHERE timestamp BETWEEN ? AND ?'  # Define la consulta para seleccionar logs entre dos fechas
    cursor.execute(query, (start_date, end_date))  # Ejecuta la consulta con las fechas proporcionadas
    logs = cursor.fetchall()  # Recupera todos los logs que cumplen con la consulta
    conn.close()  # Cierra la conexión con la base de datos
    return jsonify(logs)  # Retorna los logs en formato JSON

if __name__ == '__main__':
    app.run(port=5000)  # Inicia la aplicación Flask en el puerto 5000
