import paho.mqtt.client as mqtt
import json
import numpy as np

data_list = []
FILE = "14_tile_front_ground"

# Callback chamado quando o cliente recebe a resposta CONNACK do servidor.
def on_connect(client, userdata, flags, rc):
    print("Conectado com o código de resultado "+str(rc))
    client.subscribe("/gw/ac233fc09283/status")
    
# Callback chamado quando uma mensagem PUBLISH é recebida do servidor.
def on_message(client, userdata, msg):
    global data_list
    data = json.loads(msg.payload)
    data_list.append(data)
    print(data_list[-1])

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    with open(f"{FILE}.json","w") as file:
        json.dump(data_list,file)