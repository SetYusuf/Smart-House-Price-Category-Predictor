# 🏠 Smart House Price & Category Predictor

A full-stack web application that predicts house prices and categories using machine learning models. Built with Flask, Bootstrap, and trained ML models.

## 🌟 Features

- ✅ **Single House Prediction**: Enter house details to get instant predictions
- ✅ **Batch Processing**: Upload CSV files for multiple house predictions
- ✅ **Multiple ML Models**:
  - Linear Regression for price prediction
  - Logistic Regression for category classification
  - Decision Tree for category classification
- ✅ **Beautiful UI**: Animated header, responsive design with Bootstrap
- ✅ **Real-time Results**: Display predictions with probabilities
- ✅ **CSV Support**: Easy bulk predictions from CSV files
- ✅ **Type Animation**: Animated typing effect on page header

## 📁 Project Structure

```
smart_house_app/
│
├─ app.py                    # Flask backend server
├─ requirements.txt          # Python dependencies
├─ README.md                 # This file
│
├─ templates/
│  └─ index.html            # Frontend HTML with animations
│
├─ static/
│  ├─ css/
│  │  └─ style.css          # Custom CSS with animations
│  └─ images/
│     └─ house.png          # House icon (optional)
│
├─ uploads/                 # Auto-created folder for CSV uploads
│
├─ linear_model.pkl         # Trained Linear Regression model
├─ logistic_model.pkl       # Trained Logistic Regression model
├─ tree_model.pkl           # Trained Decision Tree model
└─ scaler.pkl               # Feature scaler (StandardScaler)
```

## 🔧 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SetYusuf/Smart-House-Price-Category-Predictor.git
   cd Smart-House-Price-Category-Predictor
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Add ML Models**:
   - Place your trained ML models in the project root folder:
     - `linear_model.pkl` (Linear Regression)
     - `logistic_model.pkl` (Logistic Regression)
     - `tree_model.pkl` (Decision Tree)
     - `scaler.pkl` (Feature Scaler - StandardScaler from sklearn)

## 🚀 Running the Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open in browser**:
   ```
   http://localhost:5000
   ```

3. The application will display a message showing the server is running.

## 💡 How to Use

### Single House Prediction
1. Fill in the form fields:
   - **House Size** (sqft): Total area of the house
   - **Number of Rooms**: Total count of rooms
   - **Location Score** (1-10): Quality of location (1=Poor, 10=Excellent)
   - **Age of House** (years): How old the house is

2. Click "Predict Price & Category" button
3. View results showing:
   - Predicted price
   - Category (Cheap/Medium/Expensive) from Logistic Regression
   - Category from Decision Tree
   - Probability distribution for each model

### Batch Prediction (CSV Upload)
1. Prepare a CSV file with columns: `size`, `rooms`, `location`, `age`
2. Example CSV format:
   ```
   size,rooms,location,age
   2500,4,8,15
   1500,3,6,25
   3000,5,9,5
   ```

3. Click "Upload & Predict" button
4. View results in table format

## 📊 Input Requirements

- **Size**: Positive number (sqft)
- **Rooms**: Positive number
- **Location**: Number between 1-10
- **Age**: Non-negative number (years)

## 🎨 Features

- **Animated Header**: Typing effect animation on the main title
- **Floating House Icon**: Animated house icon at the top
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Progress Bars**: Visual representation of prediction probabilities
- **Color-coded Results**: Different colors for different models
- **Loading Animation**: Smooth loading spinner during prediction

## 📋 API Endpoints

### Predict (Single House)
- **URL**: `/predict`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "size": 2500,
    "rooms": 4,
    "location": 8,
    "age": 15
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "predictions": {
      "price": 450000.50,
      "category_logistic": "Medium",
      "category_tree": "Medium",
      "probabilities": {
        "logistic": {"Cheap": 10.5, "Medium": 75.3, "Expensive": 14.2},
        "tree": {"Cheap": 5.0, "Medium": 85.0, "Expensive": 10.0}
      }
    }
  }
  ```

### Predict CSV (Batch)
- **URL**: `/predict-csv`
- **Method**: `POST`
- **Body**: Form data with file upload (`file` parameter)
- **Response**: Array of predictions for each row

### Health Check
- **URL**: `/health`
- **Method**: `GET`
- **Response**: Server status and model loading status

## 🐛 Troubleshooting

### Models Not Loading?
```
Error: ML models not loaded. Please place .pkl files in the project root.
```
**Solution**: Ensure all four `.pkl` files are in the project root directory:
- `linear_model.pkl`
- `logistic_model.pkl`
- `tree_model.pkl`
- `scaler.pkl`

### Port Already in Use?
If port 5000 is already in use, edit `app.py` and change the port:
```python
app.run(debug=True, host='localhost', port=5001)
```

### CSV Column Error?
Ensure your CSV has these exact columns (case-sensitive):
- `size`
- `rooms`
- `location`
- `age`

## 📚 Technologies Used

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **ML**: scikit-learn (sklearn)
- **Data**: pandas, numpy
- **Styling**: Custom CSS with animations
- **Icons**: Font Awesome 6

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Yusuf Set**
- GitHub: [@SetYusuf](https://github.com/SetYusuf)

## 🎯 Future Enhancements

- [ ] Add user authentication
- [ ] Database integration for storing predictions
- [ ] Export predictions as PDF/Excel
- [ ] Advanced visualizations with charts
- [ ] Model comparison dashboard
- [ ] REST API documentation (Swagger)
- [ ] Deployment to cloud (Heroku, AWS, Google Cloud)

## 📞 Support

For issues or questions, please create an issue on GitHub.

---

**Happy Predicting! 🏠✨**
