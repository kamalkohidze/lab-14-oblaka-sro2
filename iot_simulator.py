import time
import random
import paho.mqtt.client as mqtt

# Параметры подключения
BROKER_HOST = "9d3180b798be4c58bc31b6e5b073bfda.s1.eu.hivemq.cloud"
BROKER_PORT = 8883  # Для TLS используем 8883
USERNAME = "student"
PASSWORD = "MyPass123"

# Топик для отправки данных
TOPIC = "iot/device/temp"

# Callback функции (для отладки)
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("✅ Успешно подключено к HiveMQ!")
    else:
        print(f"❌ Ошибка подключения. Код: {reason_code}")

def on_publish(client, userdata, mid, reason_code, properties):
    print(f"📤 Сообщение отправлено (ID: {mid})")

# Создаём MQTT клиента (с указанием версии API)
client = mqtt.Client(
    client_id="python_simulator",
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

client.username_pw_set(USERNAME, PASSWORD)
client.tls_set()  # Включаем TLS шифрование
client.on_connect = on_connect
client.on_publish = on_publish

# Подключаемся к брокеру
print(f"🔗 Подключение к {BROKER_HOST}:{BROKER_PORT}...")
client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

# Запускаем сетевой цикл в отдельном потоке
client.loop_start()

# Ждём подключения
time.sleep(2)

# Отправляем данные каждые 2 секунды
print("🌡️ Начинаю отправку температуры...\n")
try:
    while True:
        temperature = round(random.uniform(20.0, 30.0), 2)
        result = client.publish(TOPIC, temperature)
        print(f"🌡️ Температура: {temperature}°C")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n⛔ Остановлено пользователем")
finally:
    client.loop_stop()
    client.disconnect()
    print("👋 Отключено от HiveMQ")