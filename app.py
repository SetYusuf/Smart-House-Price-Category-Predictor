"""
Smart House Price & Category Predictor - Flask Backend
This app loads pre-trained ML models and predicts house prices and categories
"""

from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np
import os
from werkzeug.utils import secure_filename
import traceback

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# ==================== Load ML Models ====================
def load_models():
    """Load all pre-trained ML models"""
    try:
        model_dir = os.path.dirname(os.path.abspath(__file__))
        
        with open(os.path.join(model_dir, 'linear_model.pkl'), 'rb') as f:
            linear_model = pickle.load(f)
        print("✓ Linear Regression Model loaded successfully")
        
        with open(os.path.join(model_dir, 'logistic_model.pkl'), 'rb') as f:
            logistic_model = pickle.load(f)
        print("✓ Logistic Regression Model loaded successfully")
        
        with open(os.path.join(model_dir, 'tree_model.pkl'), 'rb') as f:
            tree_model = pickle.load(f)
        print("✓ Decision Tree Model loaded successfully")
        
        with open(os.path.join(model_dir, 'scaler.pkl'), 'rb') as f:
            scaler = pickle.load(f)
        print("✓ Scaler loaded successfully")
        
        return linear_model, logistic_model, tree_model, scaler
    
    except FileNotFoundError as e:
        print(f"⚠ Error: {e}")
        print("Please ensure all .pkl files (linear_model.pkl, logistic_model.pkl, tree_model.pkl, scaler.pkl) are in the project root folder")
        return None, None, None, None

# Load models on startup
linear_model, logistic_model, tree_model, scaler = load_models()

# ==================== Helper Functions ====================
def validate_input(data):
    """Validate user input"""
    try:
        size = float(data.get('size', 0))
        rooms = float(data.get('rooms', 0))
        location = float(data.get('location', 0))
        age = float(data.get('age', 0))
        
        if size <= 0 or rooms <= 0 or location < 1 or location > 10 or age < 0:
            return False, "Please enter valid values (Size > 0, Rooms > 0, Location 1-10, Age >= 0)"
        
        return True, [size, rooms, location, age]
    except ValueError:
        return False, "All fields must be numbers"

def prepare_features(values_list):
    """Prepare features for prediction"""
    features = np.array(values_list).reshape(1, -1)
    features_scaled = scaler.transform(features)
    return features_scaled

def get_category_name(prediction):
    """Convert numeric prediction to category name"""
    categories = {0: "Cheap", 1: "Medium", 2: "Expensive"}
    return categories.get(int(prediction), "Unknown")

def predict_single_house(features_scaled):
    """Make predictions for a single house"""
    results = {}
    
    # Linear Regression for price
    predicted_price = linear_model.predict(features_scaled)[0]
    results['price'] = round(predicted_price, 2)
    
    # Logistic Regression for category
    lg_prediction = logistic_model.predict(features_scaled)[0]
    lg_probabilities = logistic_model.predict_proba(features_scaled)[0]
    results['category_logistic'] = get_category_name(lg_prediction)
    
    # Decision Tree for category
    tree_prediction = tree_model.predict(features_scaled)[0]
    tree_probabilities = tree_model.predict_proba(features_scaled)[0]
    results['category_tree'] = get_category_name(tree_prediction)
    
    # Store probabilities
    results['probabilities'] = {
        'logistic': {
            'Cheap': round(lg_probabilities[0] * 100, 2),
            'Medium': round(lg_probabilities[1] * 100, 2) if len(lg_probabilities) > 1 else 0,
            'Expensive': round(lg_probabilities[2] * 100, 2) if len(lg_probabilities) > 2 else 0
        },
        'tree': {
            'Cheap': round(tree_probabilities[0] * 100, 2),
            'Medium': round(tree_probabilities[1] * 100, 2) if len(tree_probabilities) > 1 else 0,
            'Expensive': round(tree_probabilities[2] * 100, 2) if len(tree_probabilities) > 2 else 0
        }
    }
    
    return results

# ==================== Routes ====================
@app.route('/')
def home():
    """Render the homepage"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Single house prediction endpoint"""
    try:
        if not all([linear_model, logistic_model, tree_model, scaler]):
            return jsonify({'error': 'ML models not loaded. Please place .pkl files in the project root.'}), 500
        
        # Get form data
        data = request.get_json()
        
        # Validate input
        valid, result = validate_input(data)
        if not valid:
            return jsonify({'error': result}), 400
        
        # Prepare features
        features_scaled = prepare_features(result)
        
        # Make predictions
        predictions = predict_single_house(features_scaled)
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'input': {
                'size': float(data.get('size')),
                'rooms': float(data.get('rooms')),
                'location': float(data.get('location')),
                'age': float(data.get('age'))
            }
        }), 200
    
    except Exception as e:
        print(f"Error during prediction: {traceback.format_exc()}")
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500

@app.route('/predict-csv', methods=['POST'])
def predict_csv():
    """CSV file prediction endpoint"""
    try:
        if not all([linear_model, logistic_model, tree_model, scaler]):
            return jsonify({'error': 'ML models not loaded. Please place .pkl files in the project root.'}), 500
        
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Only CSV files are allowed'}), 400
        
        # Read CSV file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Load CSV
        df = pd.read_csv(filepath)
        
        # Validate CSV columns
        required_columns = ['size', 'rooms', 'location', 'age']
        if not all(col in df.columns for col in required_columns):
            return jsonify({
                'error': f'CSV must contain columns: {", ".join(required_columns)}'
            }), 400
        
        # Make predictions for each row
        results = []
        for idx, row in df.iterrows():
            try:
                # Prepare input
                input_data = [
                    float(row['size']),
                    float(row['rooms']),
                    float(row['location']),
                    float(row['age'])
                ]
                
                # Validate
                if input_data[0] <= 0 or input_data[1] <= 0 or not (1 <= input_data[2] <= 10) or input_data[3] < 0:
                    results.append({
                        'row': idx + 1,
                        'input': input_data,
                        'error': 'Invalid values in this row'
                    })
                    continue
                
                # Scale and predict
                features_scaled = prepare_features(input_data)
                predictions = predict_single_house(features_scaled)
                
                results.append({
                    'row': idx + 1,
                    'input': {
                        'size': input_data[0],
                        'rooms': input_data[1],
                        'location': input_data[2],
                        'age': input_data[3]
                    },
                    'predictions': predictions
                })
            
            except Exception as e:
                results.append({
                    'row': idx + 1,
                    'error': f'Error processing row: {str(e)}'
                })
        
        # Clean up
        if os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify({
            'success': True,
            'results': results,
            'total_rows': len(df)
        }), 200
    
    except Exception as e:
        print(f"Error during CSV prediction: {traceback.format_exc()}")
        return jsonify({'error': f'CSV processing error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    models_loaded = all([linear_model, logistic_model, tree_model, scaler])
    return jsonify({
        'status': 'ok',
        'models_loaded': models_loaded
    }), 200

# ==================== Error Handlers ====================
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

# ==================== Main ====================
if __name__ == '__main__':
    print("\n" + "="*60)
    print("🏠 Smart House Price & Category Predictor")
    print("="*60)
    print("\nStarting Flask application...")
    print("Visit: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True, host='localhost', port=5000)
