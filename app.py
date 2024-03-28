from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Route to render the index.html page with the file upload form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload and preprocess the data
@app.route('/upload', methods=['POST'])
def upload():
    if 'testDataFile' in request.files:
        file = request.files['testDataFile']
        if file.filename != '':
            # Save the uploaded file
            file.save('test_data.csv')

            # Preprocess the data (replace this with your preprocessing logic)
            #processed_data = preprocess_data('test_data.csv')  # Example function to preprocess data

            #return render_template('index.html', processed_data=processed_data)
            return render_template('index.html')
    return 'File upload failed.'

# Route to handle prediction
@app.route('/predict', methods=['POST'])
def predict():
    # Perform prediction using the preprocessed data (replace this with your prediction logic)
    #prediction = make_prediction()  # Example function to make prediction

    prediction = "Normal"
    return render_template('results.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)