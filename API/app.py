from flask import Flask, request, jsonify
import pickle
import numpy as np
import os

# Load the trained model
filename = 'rdf_model.sav'
model =  pickle.load(open(filename, 'rb'))



# Create a Flask app
app = Flask(__name__)


# Define a route for the API
@app.route('/predict', methods=['POST'])
def predict():
    # Get the data from the request
    data = request.get_json()

    k = np.array([[i for i in data.values()]]).tolist()
    
    # Use the model to make a prediction
    prediction = model.predict(k)

    print(prediction.tolist())
    # Return the prediction as a JSON response
    return jsonify({'pred': prediction.tolist()[0]})

if __name__ == '__main__':
    app.run(host='192.168.43.147', debug=True) # here i have added my local ip to get access from outside of container docker 