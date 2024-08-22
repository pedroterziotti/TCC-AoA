import pandas as pd
import numpy as np

# Dict that transformer antena codes in antenna number

ANTENAS = {
    "0":"12",
    "1":"10",
    "2":"11",
    "4":"3",
    "5":"1",
    "6":"2",
    "8":"6",
    "9":"4",
    "10":"5",
    "12":"9",
    "13":"7",
    "14":"8",
}

def to_plus_minus_pi(angle, deg = True):
    ''' Mantém o ângulo entre +- 180/pi '''
    factor = 180 if deg else np.pi
    while angle >= factor:
        angle -= 2 * factor
    while angle < -factor:
        angle += 2 * factor
    return angle

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

def split_samples(iq: np.ndarray, anchor_conf: str="2,2,0,5,1,12"  ):
    anchor_conf = anchor_conf.split(",")
    
    ref_samples = [ complex(iq[i], iq[i+1]) for i in range(0,15,2) ]



