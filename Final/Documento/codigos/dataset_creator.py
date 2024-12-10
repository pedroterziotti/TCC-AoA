import pandas as pd
import numpy as np
import os

def pm(angle):
    """ Keeps angle measures between +pi and -pi"""
    if angle > np.pi:
        while angle > np.pi:
            angle -= 2*np.pi
    if angle < -np.pi:
        while angle < -np.pi:
            angle += 2*np.pi
    return angle

pm = np.vectorize(pm)


def single_antenna_to_dataframe(read_fp: str, write_fp=None) -> pd.DataFrame:
    '''Transforma uma captura com uma única antena em um df '''
    raw =pd.read_json(read_fp)
    df= list()
    for group in raw[1]:
        df.append(group)
    df = pd.DataFrame(df)
    df = df.join(pd.DataFrame(df["aoa"].to_list()))
    df.pop("aoa")

    if write_fp is not None:
        df.to_json(write_fp)

    return df

# Generate the datasets
tw= pd.DataFrame()
for file in os.listdir("tw"):
    df = single_antenna_to_dataframe("./tw/"+file)
    df["angle"] = float(file.split("-")[0].split("_")[-1]) -90
    df["distance"] = float(file.split("-")[1].split("_")[-1].split(".")[0])
    tw = pd.concat((tw,df))
tw["capture"] = "tw"
tw.pop("raw")
tw.pop("no")
tw["switch_order"] = "2-2-0-5-6"

poli= pd.DataFrame()
for file in os.listdir("poli"):
    df = single_antenna_to_dataframe("./poli/"+file)
    angle = int(file.split("_")[1]) -90
    distance = int(file.split("_")[3])

    df["angle"] = angle
    df["distance"] = distance if angle == 0 else abs(distance/np.sin(np.deg2rad(angle)))
    poli = pd.concat((poli,df))

poli["capture"] = "poli"
poli.pop("raw")
poli.pop("no")
poli["switch_order"] = "2-2-0-5-6"

camila= pd.DataFrame()
for file in os.listdir("camila"):
    df = single_antenna_to_dataframe("./camila/"+file)
    angle = int(file.split("_")[1]) -90
    distance = int(file.split("_")[3].split(".")[0])

    df["angle"] = angle
    df["distance"] = distance if angle == 0 else abs(distance/np.sin(np.deg2rad(angle)))
    camila = pd.concat((camila,df))

camila["capture"] = "camila"
camila.pop("raw")
camila.pop("no")
camila["switch_order"] = "2-2-0-5-6"

tw2= pd.DataFrame()

for file in os.listdir("tw2"):
    df = single_antenna_to_dataframe("./tw2/"+file)
    df["angle"] = float(file.split("_")[1].split("_")[-1])
    df["distance"] = file.split("_")[3]
    tw2 = pd.concat((tw2,df))
    
tw2["switch_order"] = "2-2-2-0-5-6-14-13-8-10"
tw2["capture"] ="tw2"
tw2.pop("raw")
tw2.pop("no")

dataset = pd.concat((tw,poli,camila,tw2))

# Create preprocessing columns

def get_ref(iq_sample):
    #compile the IQ data
    iq = np.array([np.angle(
        complex(iq_sample[i],iq_sample[i+1])) 
            for i in range(0,len(iq_sample),2)])

    return iq[:8]

def get_phases(iq_sample):
    #compile the IQ data
    iq = np.array([np.angle(complex(iq_sample[i],iq_sample[i+1])) for i in range(0,len(iq_sample),2)])
    
    return iq[8:]

dataset["ref"]=dataset["iq"].map(get_ref)
dataset["phases"]=dataset["iq"].map(get_phases)

wave_dist= (299_792_458/(2.4e6+270e3))/50
aoa = lambda pds: np.rad2deg( np.arcsin(np.clip(pm(pds[1:] - pds[:-1] -np.deg2rad(2*99)) *wave_dist/(2*np.pi),-1,1))) 

dataset["aoa"] = dataset["phases"].map(aoa)

# Deletes invalid phase diffs
new_aoa=[]
for index,row in dataset.iterrows():
    step= 3 if  row["switch_order"] == "2-2-0-5-6" else 4
    new_aoa.append(np.delete(row["aoa"],np.arange(step-1,len(row["aoa"]),step)))

dataset["aoa"]= new_aoa

dataset = dataset.reset_index()
dataset.to_json("../data.json")