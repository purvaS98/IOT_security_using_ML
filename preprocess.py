from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def preprocess_data(data):
    # converting text data tp pd dataframe to start with preprocessing
    data = pd.DataFrame(data)
    print(data)
    # Remove duplicates
    data.drop_duplicates(inplace=True)

    #drop null values
    data.dropna(inplace=True)

    # Encoding categorical or object fetaures  using Label Encoding
    label_encoder = LabelEncoder()
    data['Device_Name'] = label_encoder.fit_transform(data['Device_Name'])
    data['Attack'] = label_encoder.fit_transform(data['Attack'])
    data['Attack_subType'] = label_encoder.fit_transform(data['Attack_subType'])

    # Scaling dataset
    # scaler = MinMaxScaler()
    # res_data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
    #res_data.drop(['label'], axis=1, inplace=True)

    # dropping label column as they are not required
    # res_data= data.drop(['label','Device_Name','Attack','Attack_subType'])
    data.drop(['label'], axis=1, inplace=True)
    data.drop(['Device_Name'], axis=1, inplace=True)
    data.drop(['Attack'], axis=1, inplace=True)
    data.drop(['Attack_subType'], axis=1, inplace=True)

    print(data)
    #processed_data = data
    return data