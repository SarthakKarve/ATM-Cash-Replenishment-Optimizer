# ATM Cash Replenishment Optimizer

## 📌 Overview

ATM Cash Replenishment Optimizer is an AI-powered system designed to improve ATM cash management by predicting future cash demand, prioritizing ATMs for replenishment, and optimizing cash delivery routes. The system helps banks minimize cash shortages, reduce operational costs, and ensure uninterrupted ATM services.

This project combines Machine Learning, Explainable AI (XAI), Route Optimization, and an AI-powered chatbot to support intelligent decision-making in ATM cash replenishment operations.

---

## 🚀 Key Features

- Predicts future ATM cash demand using Machine Learning.
- Identifies ATMs requiring immediate replenishment.
- Assigns priority ranks based on cash urgency.
- Calculates recommended refill amounts with a safety buffer.
- Generates optimized ATM replenishment routes.
- Displays ATM locations and routes on interactive maps.
- Provides Explainable AI insights using SHAP.
- Includes an AI-powered chatbot using Google Gemini API.
- Offers an interactive dashboard built with Streamlit.

---

## 🛠️ Technologies Used

### Programming Language
- Python

### Libraries & Frameworks
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- Streamlit
- Folium
- SHAP
- Matplotlib
- Seaborn

### Explainable AI
- SHAP (SHapley Additive exPlanations)

### AI Integration
- Google Gemini API

---

## 📊 Project Workflow

1. Data Collection and Preprocessing
2. Exploratory Data Analysis (EDA)
3. Feature Engineering
4. Machine Learning Model Training
5. ATM Cash Demand Prediction
6. ATM Priority Ranking
7. Cash Refill Recommendation
8. Route Optimization
9. Explainable AI Analysis using SHAP
10. Dashboard Visualization and Decision Support

---

## 🧠 Machine Learning Models Used

- Linear Regression
- Random Forest Regressor
- XGBoost Regressor

The best-performing model is used for predicting ATM cash demand and generating replenishment recommendations.

---

## 🗺️ Route Optimization

The route optimization module:

- Selects ATMs requiring replenishment.
- Prioritizes ATMs based on predicted cash requirements.
- Generates an optimized replenishment sequence.
- Visualizes ATM routes on an interactive map for efficient cash delivery.

---

## 📈 Explainable AI (XAI)

To improve transparency and trust, SHAP has been integrated into the system.

SHAP helps:

- Identify the most important features influencing predictions.
- Explain individual ATM cash demand predictions.
- Visualize feature contributions through summary plots.
- Support data-driven decision-making.

---

## 🤖 AI-Powered Chatbot

The dashboard integrates Google's Gemini API to provide intelligent assistance.

The chatbot can:

- Answer questions related to ATM replenishment recommendations.
- Explain prediction results.
- Provide insights about ATM priorities and route planning.

---

## 💻 Installation

### Clone the Repository

```bash
git clone https://github.com/SarthakKarve/ATM-Cash-Replenishment-Optimizer.git
```

### Navigate to the Project Directory

```bash
cd ATM-Cash-Replenishment-Optimizer
```

### Install Required Dependencies

```bash
pip install -r requirements.txt
```

### Run the Streamlit Application

```bash
streamlit run app.py
```

---

## 📷 Dashboard Preview

Add screenshots of your dashboard here to showcase the application's interface and functionalities.

---

## 🎯 Future Enhancements

- Real-time ATM transaction integration.
- IoT-based ATM monitoring.
- Advanced Vehicle Routing Problem (VRP) optimization.
- Cloud deployment using AWS or Azure.
- Real-time alert and notification system.
- Integration with live banking transaction systems.

---

## 👨‍💻 Author

**Sarthak Karve**

GitHub: https://github.com/SarthakKarve

LinkedIn: https://linkedin.com/in/sarthakkarve

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.
