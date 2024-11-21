import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

ds =  pd.read_json("./data.json")


angles = list(set(ds["angle"]))
angles.sort()

#Variar essa variável para conseguir angulos diferentes entre range(0,180+15,15)
angle=180

distances= list(set(ds[ds["angle"] ==  angle]["distance"]))
distances.sort()

fig, ax =plt.subplots(3,1,figsize=(25,10))

ax[0].set_title("a2-a1")
ax[1].set_title("a3-a2")
ax[2].set_title("a3-a1")

index=0
for row, distance in enumerate(distances):
    for sample in ds[ds["angle"] ==  angle][ds["distance"] == distance].iterrows():
        index+=1

        #plota todas as diferenças de faze dentro de um pacote
        ax[0].plot([index]*len(sample[1]["a2a1"]),sample[1]["a2a1"],"|") 
        
        ax[1].plot([index]*len(sample[1]["a3a2"]),sample[1]["a3a2"],"|") 
        
        ax[2].plot([index]*len(sample[1]["a3a1"]),sample[1]["a3a1"],"|")

    # Faz a distinção de distâncias
    ax[0].vlines(index,-np.pi,np.pi,label=distance)
    ax[1].vlines(index,-np.pi,np.pi,label=distance)
    ax[2].vlines(index,-np.pi,np.pi,label=distance)

plt.show()


