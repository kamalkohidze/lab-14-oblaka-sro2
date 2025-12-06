from flask import Flask, render_template, jsonify
import paho.mqtt.client as mqtt
import threading
import time

app = Flask(__name__)

# Параметры подключения к HiveMQ
BROKER_HOST = "9d3180b798be4c58bc31b6e5b073bfda.s1.eu.hivemq.cloud"
BROKER_PORT = 8883
USERNAME = "student"
PASSWORD = "MyPass123"
TOPIC = "iot/device/temp"

# Глобальная переменная для хранения последней температуры
latest_temperature = {"value": None, "timestamp": None}


# Callback для получения сообщений
def on_message(client, userdata, message):
    global latest_temperature
    try:
        temp = float(message.payload.decode())
        latest_temperature = {
            "value": temp,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        print(f"📥 Получена температура: {temp}°C")
    except Exception as e:
        print(f"❌ Ошибка обработки сообщения: {e}")


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("✅ Подключено к MQTT брокеру!")
        client.subscribe(TOPIC)
        print(f"📡 Подписка на топик: {TOPIC}")
    else:
        print(f"❌ Ошибка подключения: {reason_code}")


# Запуск MQTT клиента в отдельном потоке
def start_mqtt_client():
    client = mqtt.Client(
        client_id="web_service_client",
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )
    client.username_pw_set(USERNAME, PASSWORD)
    client.tls_set()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
        client.loop_forever()
    except Exception as e:
        print(f"❌ Ошибка MQTT: {e}")


# Главная страница
@app.route('/')
def index():
    return render_template('index.html')


# API для получения данных температуры
@app.route('/api/temperature')
def get_temperature():
    return jsonify(latest_temperature)


if __name__ == '__main__':
    # Запускаем MQTT клиент в отдельном потоке
    mqtt_thread = threading.Thread(target=start_mqtt_client, daemon=True)
    mqtt_thread.start()

    print("🌐 Веб-сервер запускается...")
    print("🔗 Откройте браузер: http://127.0.0.1:5000")

    # Запускаем Flask
    app.run(host='0.0.0.0', port=5000, debug=True)