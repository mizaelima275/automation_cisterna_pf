import machine # type: ignore
import time
import network # type: ignore
import urequests # type: ignore

# Configurações do Wi-Fi
ssid = '****'
password = '****'

# Configurações do Home Assistant
url = 'http://(ip_broker)/api/states/sensor.cisterna_aedi'
token = '****'

# Configurações do Sensor SR04
trig_pin = machine.Pin(26, machine.Pin.OUT)
echo_pin = machine.Pin(27, machine.Pin.IN)
pulse_time = machine.time_pulse_us

# Alturas da cisterna em cm
altura_maxima = 250
altura_minima = 19.8

# Buffer para armazenar as últimas leituras válidas
buffer_leituras = []
numero_leituras_validas = 3  # Número de leituras consistentes necessárias
margem_cm = 5  # Margem de variação aceitável entre leituras

def connect_wifi(ssid, password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    start_time = time.time()
    while not station.isconnected():
        if time.time() - start_time > 30:  # Tempo limite de 30 segundos
            print("Falha ao conectar ao Wi-Fi. Tentando novamente...")
            start_time = time.time()
            station.connect(ssid, password)
        time.sleep(1)
    print('Conexão Wi-Fi estabelecida')

def read_distance():
    trig_pin.value(0)
    time.sleep_us(2)
    trig_pin.value(1)
    time.sleep_us(10)
    trig_pin.value(0)
    duration = pulse_time(echo_pin, 1, 1000000)
    distance = (duration / 2) / 29.1
    return distance

def calculate_percentage(distance):
    if distance > altura_maxima:
        return 0
    elif distance < altura_minima:
        return 100
    else:
        percentage = (1 - (distance - altura_minima) / (altura_maxima - altura_minima)) * 100
        return round(percentage, 1)  # Arredonda para uma casa decimal

def is_consistent_reading(new_reading):
    if len(buffer_leituras) >= numero_leituras_validas:
        if all(abs(new_reading - reading) <= margem_cm for reading in buffer_leituras[-numero_leituras_validas:]):
            return True
    buffer_leituras.append(new_reading)
    if len(buffer_leituras) > numero_leituras_validas:
        buffer_leituras.pop(0)
    return False

def send_to_home_assistant(url, token, percentage):
    headers = {'Authorization': 'Bearer ' + token,
               'Content-Type': 'application/json'}
    data = {'state': percentage, 'attributes': {'unit_of_measurement': '%'}}
    try:
        response = urequests.post(url, json=data, headers=headers)
        response.close()
        print("Dados enviados com sucesso para o Home Assistant.")
    except OSError as e:
        print("Erro de conexão:", e)

connect_wifi(ssid, password)

reset_timer = time.time() + 150  # Define um temporizador para 2.30 minutos (150 segundos)

while True:
    if time.time() >= reset_timer:
        machine.reset()  # Reseta o dispositivo a cada 2.30 minutos

    distance = read_distance()
    if is_consistent_reading(distance):
        percentage = calculate_percentage(distance)
        print('Porcentagem de água:', percentage, '%')
        send_to_home_assistant(url, token, percentage)
    time.sleep(2)