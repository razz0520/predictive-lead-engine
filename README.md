# 🚀 Predictive Lead Scoring System

An AI-powered system designed to predict the probability of a client subscribing to a term deposit based on demographic and campaign data.

## 🌟 Features
- **Real-time Predictions**: Enter customer details and get a score instantly.
- **Full Feature Support**: Captures job roles, education, financial indices, and previous campaign history.
- **Enterprise-ready Architecture**: 
  - **Logging**: All predictions and errors are tracked in `app.log`.
  - **Configuration**: Environment-aware path management in `config.py`.
  - **Robustness**: Automated scaling and error-handling in predictions.
- **Machine Learning**: Uses a Random Forest Classifier trained on the Bank Marketing dataset.
- **Balanced Results**: Implements SMOTE to handle class imbalance in the training data.

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd predictive-lead-scoring
   ```

2. **Setup virtual environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

## 📦 Deployment
For detailed deployment recommendations and critical checklists, see the [Deployment Report](deployment_report.md).

You can also run this using Docker:
```bash
docker build -t lead-scoring-app .
docker run -p 8501:8501 lead-scoring-app
```

## 📊 Model Performance
The current model achieved the following performance on the test set:
- **Precision**: 60%+ for the "yes" class
- **Recall**: 60%+ for the "yes" class
- **SMOTE Balanced**: Yes
