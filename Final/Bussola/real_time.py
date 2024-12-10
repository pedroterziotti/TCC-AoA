import paho.mqtt.client as mqtt
import json
import numpy as np
import xgboost as xgb
import json
import os

with open(r"C:\Users\pedro\OneDrive\Documentos\Eletrica\Eletrica\TCC - Macapá\TCC-AoA\Final\ML\xgboost\tw2\pd_row\dicts.json") as file:
    dicts= json.load(file)

def pm(angle):
    if angle > 2*np.pi:
        while angle > np.pi:
            angle -= 2*np.pi
    if angle < -2*np.pi:
        while angle < -np.pi:
            angle += 2*np.pi
    return angle

pm = np.vectorize(pm)


wave_dist= (299_792_458/(2.4e6+270e3))/50
#phase_diff - 29= np.sin(np.deg2rad(angles))*2*np.pi/wave_dist
aoa = lambda pds: np.rad2deg( np.arcsin(np.clip(pm(pds[1:] - pds[:-1] -np.deg2rad(2*99)) *wave_dist/(2*np.pi),-1,1))) 


regressor = xgb.XGBRegressor()
regressor.load_model("./ML/xgboost/tw2/pd_row/regressor_pd_row.json")

classifier = xgb.XGBClassifier()
classifier.load_model("./ML/xgboost/tw2/pd_row/pd_row_classifier.json")

model = regressor

azi_ma = [0]*6
el_ma = [0]*6

# Callback chamado quando o cliente recebe a resposta CONNACK do servidor.
def on_connect(client, userdata, flags, rc):
    print("Conectado com o código de resultado "+str(rc))
    client.subscribe("/gw/ac233fc09283/status")
    
    
def on_message(client, userdata, msg):
    
    data = json.loads(msg.payload)
    
    phases = np.array([np.angle(complex(data[1]["aoa"]["iq"][i],data[1]["aoa"]["iq"][i+1])) for i in range(0,len(data[1]["aoa"]["iq"]),2)])
        
    pds = np.array([phases[i:i+8][1:]-phases[i:i+8][:-1] for i in range(8,len(phases),8)][:-1])

    model_predictions = model.predict(pds)
    
    #model_predictions = [int(dicts["backwards_dict"][str(prediction)]) for prediction in model_predictions]

    azi = model_predictions[0::2]
    el = model_predictions[1::2]


    azi_ma.append(np.mean(azi))
    azi_ma.pop(0) 

    el_ma.append(float(np.mean(el)))
    el_ma.pop(0) 

    aoa_xz = np.arctan2(np.deg2rad(np.mean(azi_ma)),np.deg2rad(np.mean(el_ma))) 
    angle= np.rad2deg(aoa_xz) +180

    with open(r"C:\Users\pedro\OneDrive\Documentos\Eletrica\Eletrica\TCC - Macapá\TCC-AoA\Final\Bussola\angle.txt","w") as file:
        file.write(str(angle))

    print(f"Elevation I: {el_ma[-1]} \t Azimutal I: {azi_ma[-1]}")
    print(f"Elevation: {np.mean(el_ma)} \t Azimutal: {np.mean(azi_ma)}")
    print(f"AoA={angle} \n")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)
#client.connect("test.mosquitto.org", 1883, 60)

client.loop_forever()