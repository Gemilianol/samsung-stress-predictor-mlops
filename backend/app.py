from flask import Flask, request, jsonify
from flask_cors import CORS # Needed for cross-origin requests during development
import pandas as pd
import numpy as np
from src.pipeline.predict_pipeline import predict_input
import traceback

app = Flask(__name__)
CORS(app) # Enable CORS for all routes (important for development)
# At the beginning, Flask and React apps will be running on localhost but in 
# differents ports so CORS allows to communicate each other.

# @app.route('/', methods=['GET'])
# def home():
#     return 'The Flask Application is running ONLY as a Backend on port 2000'

# Matches the fetch URL and method from your App.jsx (React frontend).
@app.route('/predict', methods=['POST'])
def predict():
        try:
            # Parses the JSON data sent from the frontend into a Python dictionary.
            data = request.get_json()
            
            if not data:
                return jsonify({'Error': 'No data was provided'}), 400
            
            # Then you simply convert the dict to DataFrame:
            data = pd.DataFrame([data], index=[0])
            
            # IMPORTANT: all input values which send from the frontend 
            # are string by default:
            data = data.astype(float)
            
            pred = predict_input(data)
            
            # jsonify(): Converts a Python dictionary into a JSON response.
            return jsonify({'Prediction': round(float(pred[0]), 2)})

            # Exception avoids to see the traceback from the predict_input function 
            # if fails so we need to set explicity. 
        except Exception as e:
            print(f"An unexpected error occurred in predict route: {e}")
            traceback.print_exc() # <--- THIS WILL PRINT THE FULL TRACEBACK
            return jsonify({'Error': str(e)}), 500 # Can hide crucial details for the frontend.


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000, debug=True) # Flask is listening on all network interfaces (0.0.0.0)