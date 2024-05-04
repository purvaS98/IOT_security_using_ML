from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def label_data():
    # Encoding categorical or object fetaures  using Label Encoding

    data = pd.read_csv(r'C:\Users\Dell\Downloads\BoTNeTIoT-L01-v2 (1).csvs')
    label_encoder_attack = LabelEncoder()
    data['Attack'] = label_encoder_attack.fit_transform(data['Attack'])
    label_encoder_subattack = LabelEncoder()
    data['Attack_subType'] = label_encoder_subattack.fit_transform(data['Attack_subType'])

    return label_encoder_attack, label_encoder_subattack