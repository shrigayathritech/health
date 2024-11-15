from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle
with open('kmeans_model.pkl', 'rb') as f:
    kmeans_model = pickle.load(f)

with open('gmm_model.pkl', 'rb') as f:
    gmm_model = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
app = Flask(__name__)
def assign_treatment(blood_pressure, cholesterol, heart_rate):
    if blood_pressure > 140 and cholesterol > 200:
        return "ACE Inhibitors and Statins"
    elif heart_rate < 70:
        return "Beta Blockers"
    elif cholesterol > 200:
        return "Statins and Dietary Changes"
    else:
        return "General Checkup"

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/get_treatment', methods=['POST'])
def predict():
    try:
        age = float(request.form['age'])
        blood_pressure = float(request.form['blood_pressure'])
        cholesterol = float(request.form['cholesterol'])
        heart_rate = float(request.form['heart_rate'])
        treatment_duration = float(request.form['treatment_duration'])
        user_data = np.array([[age, blood_pressure, cholesterol, heart_rate, treatment_duration]])
        user_data_scaled = scaler.transform(user_data)

        kmeans_cluster = int(kmeans_model.predict(user_data_scaled)[0])  
        gmm_cluster = int(gmm_model.predict(user_data_scaled)[0])         
        treatment = assign_treatment(blood_pressure, cholesterol, heart_rate)

        result = {
            'age': age,
            'blood_pressure': blood_pressure,
            'cholesterol': cholesterol,
            'heart_rate': heart_rate,
            'treatment_duration': treatment_duration,
            'kmeans_cluster': kmeans_cluster,
            'gmm_cluster': gmm_cluster,
            'personalized_treatment': treatment
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
