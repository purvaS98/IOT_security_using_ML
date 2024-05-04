from flask import Flask, render_template, request
from preprocess import preprocess_data
from predict_res import predict
#from labelEncode import label_data
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import pickle


app = Flask(__name__)

# Load the trained models
model_attack = pickle.load(open("c:/Users/Dell/Downloads/IOT security using ML models project/attack_DT_model.sav", 'rb'))
model_subattack = pickle.load(open("c:/Users/Dell/Downloads/IOT security using ML models project/subattack_DT_model.sav", 'rb'))

def label_data():
    # Encoding categorical or object features using Label Encoding
    data = pd.read_csv(r'C:\Users\Dell\Downloads\BoTNeTIoT-L01-v2 (1).csv')
    label_encoder_attack = LabelEncoder()
    data['Attack'] = label_encoder_attack.fit_transform(data['Attack'])
    label_encoder_subattack = LabelEncoder()
    data['Attack_subType'] = label_encoder_subattack.fit_transform(data['Attack_subType'])
    return label_encoder_attack, label_encoder_subattack

# Route to render the index.html page with the file upload form
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('aboutus.html')


# Route to handle file upload and preprocess the data
@app.route('/upload', methods=['POST'])
def upload():
    if 'testDataFile' in request.files:
        file = request.files['testDataFile']
        if file.filename != '':
            # Save the uploaded file
            file.save('test_data.csv')

            # Preprocess the data (replace this with your preprocessing logic)
            processed_data = preprocess_data(pd.read_csv('test_data.csv'))  # Example function to preprocess data
            
            if len(processed_data) == 0:
                return render_template('index.html', processed_data= processed_data, msg = 'Preprocessing Unsucessfull !!!')

            file.save('preprocessedData.csv')
            
            return render_template('index.html', processed_data = processed_data, msg = 'Preprocessing successfully  !!!')
            #return render_template('index.html')
    return 'File upload failed.'

# Route to handle prediction
@app.route('/predict', methods=['POST'])
def predict():
    expected_res = pd.read_csv('test_data.csv')
    processed_data = preprocess_data(pd.read_csv('test_data.csv'))
    #processed_data = request.files['processed_data']
    selected_features = ['MI_dir_L0.1_weight','MI_dir_L0.1_mean','MI_dir_L0.1_variance','H_L0.1_weight','H_L0.1_mean','H_L0.1_variance','HH_L0.1_mean',
                         'HH_L0.1_magnitude','HpHp_L0.1_mean','HpHp_L0.1_magnitude','MI_dir_L0.1_weight','MI_dir_L0.1_mean','MI_dir_L0.1_variance',
                         'H_L0.1_weight','H_L0.1_mean','H_L0.1_variance','HH_L0.1_weight','HH_jit_L0.1_weight','HH_jit_L0.1_mean','HpHp_L0.1_weight']
    
    selected_features1 = ['MI_dir_L0.1_variance', 'H_L0.1_mean', 'HpHp_L0.1_magnitude', 'H_L0.1_weight', 'HH_L0.1_magnitude', 'HH_jit_L0.1_weight', 'MI_dir_L0.1_mean', 'HH_L0.1_weight', 'HpHp_L0.1_mean', 'MI_dir_L0.1_weight', 'HH_L0.1_mean', 'HpHp_L0.1_weight', 'HH_jit_L0.1_mean', 'H_L0.1_variance']
    df = pd.DataFrame(processed_data, columns=selected_features)
    print(df)

    if not processed_data.empty:
        #processed_data = preprocess_data(pd.read_csv('test_data.csv'))

        # Initialize label encoders
        label_encoder_attack, label_encoder_subattack = label_data()

        # Perform prediction using the preprocessed data
        prediction_attack_labels = model_attack.predict(processed_data[selected_features])
        prediction_subattack_labels = model_subattack.predict(processed_data[selected_features])
        print(prediction_attack_labels)
        print(prediction_subattack_labels)
        # Reverse label encoding to get the original labels
        prediction_attack = label_encoder_attack.inverse_transform(prediction_attack_labels)
        prediction_subattack = label_encoder_subattack.inverse_transform(prediction_subattack_labels)






        # Perform prediction using the preprocessed data
        #prediction_attack = model_attack.predict(processed_data[selected_features])
        #prediction_subattack = model_subattack.predict(processed_data[selected_features])

        # Create a DataFrame to display the results
        results_df = pd.DataFrame({
            'Expected Attack': expected_res['Attack'],
            'Predicted Attack': prediction_attack,
            'Expected Subattack': expected_res['Attack_subType'],
            'Predicted Subattack': prediction_subattack
        })
        print(results_df)
        # Convert the DataFrame to HTML table
        results_html = results_df.to_html(index=False)
        check = expected_res['Attack'].item()
        pred_check = prediction_attack
        if pred_check != 'Normal' and check != 'Normal':
            result_msg ="Your request is not safe"
            print(result_msg)
            result_flag= 1

        elif check == 'Normal':
            result_msg ="Your request is safe"
            print(result_msg)
            result_flag= 0

        return render_template('results.html', results_df=results_df, result_msg=result_msg,result_flag=result_flag)
    else:
        return render_template('index.html', error='No file selected')

if __name__ == '__main__':
    app.run(debug=True)