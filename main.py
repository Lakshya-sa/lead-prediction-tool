'''import pandas as pd
from flask import Flask, request, jsonify
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.tree import DecisionTreeClassifier
import joblib

# Load the trained model and scaler
dt_classifier = joblib.load('decision_tree.pkl')  # Load your trained model
scaler = joblib.load('scaler.pkl')  # Load the scaler

# Initialize Flask app
app = Flask(__name__)
@app.route('/', methods=['GET'])
def home():
    return "hello"


# Define a route for predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Get JSON data from request
    data = request.get_json(force=True)
    
    # Convert JSON data to DataFrame
    input_data = pd.DataFrame([data])
    
    # Handle categorical data (encode if necessary)
    label_encoders = {}  # Load or define your label encoders used during training
    for column in input_data.select_dtypes(include='object').columns:
        if column in label_encoders:
            input_data[column] = label_encoders[column].transform(input_data[column])
        else:
            le = LabelEncoder()
            input_data[column] = le.fit_transform(input_data[column])
            label_encoders[column] = le
    
    # Scale the features
    scaled_data = scaler.transform(input_data)

    # Make predictions
    prediction = dt_classifier.predict(scaled_data)

    # Return the prediction as JSON response
    return jsonify({"prediction": "Hot Lead" if prediction[0] == 1 else "Cold Lead"})

if __name__ == '__main__':
    app.run(debug=True,port=8080)'''


import pandas as pd
from flask import Flask, request, jsonify, render_template
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.tree import DecisionTreeClassifier
import joblib

# Load the trained model and scaler
dt_classifier = joblib.load('decision_tree.pkl')  # Load your trained model
scaler = joblib.load('scaler.pkl')  # Load the scaler

# Initialize Flask app
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('mlops.html')  # Serve the HTML page

# Define a route for predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from request
        data = request.get_json(force=True)
        
        # Convert JSON data to DataFrame
        input_data = pd.DataFrame([data])
        
        # Handle categorical data (encode if necessary)
        label_encoders = {}  # Load or define your label encoders used during training
        for column in input_data.select_dtypes(include='object').columns:
            if column in label_encoders:
                input_data[column] = label_encoders[column].transform(input_data[column])
            else:
                le = LabelEncoder()
                input_data[column] = le.fit_transform(input_data[column])
                label_encoders[column] = le
        
        # Scale the features
        scaled_data = scaler.transform(input_data)

        # Make predictions
        prediction = dt_classifier.predict(scaled_data)

        # Return the prediction as JSON response
        return jsonify({"prediction": "Hot Lead" if prediction[0] == 1 else "Cold Lead"})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=8080)
