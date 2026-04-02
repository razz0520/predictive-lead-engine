import streamlit as st
import pandas as pd
import joblib
import numpy as np
import logging
from config import MODEL_PATH, SCALER_PATH, FEATURES_PATH, LOG_FILE

# --- 1. SETUP LOGGING ---
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("LeadScoringApp")

# --- 2. LOAD RESOURCES ---
@st.cache_resource
def load_resources():
    try:
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        features = joblib.load(FEATURES_PATH)
        logger.info("Successfully loaded model and scaler.")
        return model, scaler, features
    except Exception as e:
        logger.error(f"Failed to load resources: {e}")
        st.error(f"Critical Error: {e}")
        st.stop()

model, scaler, model_features = load_resources()

# --- 3. UI LAYOUT ---
st.set_page_config(page_title="Predictive Lead Scoring Pro", layout="wide")

st.title("🚀 Predictive Lead Scoring System (Production V2)")
st.markdown("""
### Rank your leads and optimize your sales conversion!
Enter customer details below. The system uses a machine-learning model trained on the Bank Marketing dataset, 
integrated with SMOTE to handle unbalanced lead distributions.
""")

# Define categorical values from dataset
CATEGORICAL_OPTIONS = {
    'job': ['admin.', 'blue-collar', 'technician', 'services', 'management', 'retired', 'entrepreneur', 'self-employed', 'housemaid', 'unemployed', 'student', 'unknown'],
    'marital': ['married', 'single', 'divorced', 'unknown'],
    'education': ['university.degree', 'high.school', 'basic.9y', 'professional.course', 'basic.4y', 'basic.6y', 'unknown', 'illiterate'],
    'housing': ['no', 'yes', 'unknown'],
    'loan': ['no', 'yes', 'unknown'],
    'poutcome': ['nonexistent', 'failure', 'success'],
    'contact': ['cellular', 'telephone'],
    'month': ['may', 'jul', 'aug', 'jun', 'nov', 'apr', 'oct', 'sep', 'mar', 'dec'],
    'day_of_week': ['mon', 'tue', 'wed', 'thu', 'fri']
}

# --- 4. INPUT TABS ---
tab1, tab2, tab3 = st.tabs(["👤 Demographic Info", "💼 Campaign & Finance", "📅 Previous History"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", 18, 100, 30)
        job = st.selectbox("Job Type", CATEGORICAL_OPTIONS['job'])
    with col2:
        marital = st.selectbox("Marital Status", CATEGORICAL_OPTIONS['marital'])
        education = st.selectbox("Education Level", CATEGORICAL_OPTIONS['education'])

with tab2:
    col3, col4 = st.columns(2)
    with col3:
        housing = st.selectbox("Has Housing Loan?", CATEGORICAL_OPTIONS['housing'])
        loan = st.selectbox("Has Personal Loan?", CATEGORICAL_OPTIONS['loan'])
        duration = st.number_input("Call Duration (seconds)", 0, 5000, 180)
    with col4:
        campaign = st.number_input("Contacts during this campaign", 1, 50, 1)
        emp_var_rate = st.number_input("Employment Variation Rate", value=-1.8)
        nr_employed = st.number_input("Number of Employees Index", value=5099.1)

with tab3:
    col5, col6 = st.columns(2)
    with col5:
        pdays = st.number_input("Days since last contact (999 if never)", value=999)
        previous = st.number_input("Previous contacts count", 0, 10, 0)
        poutcome = st.selectbox("Previous campaign outcome", CATEGORICAL_OPTIONS['poutcome'])
    with col6:
        cons_conf_idx = st.number_input("Consumer Confidence Index", value=-46.2)
        euribor3m = st.number_input("Euribor 3 Month Rate", value=1.3)
        cons_price_idx = st.number_input("Consumer Price Index", value=92.8)

# --- 5. PREDICTION LOGIC ---
if st.button("Calculate Lead Score", type="primary"):
    # Initialize empty row with 0s for model alignment
    input_df = pd.DataFrame(0, index=[0], columns=model_features)
    
    # Fill in numerical features
    input_df['age'] = age
    input_df['duration'] = duration
    input_df['campaign'] = campaign
    input_df['pdays'] = pdays
    input_df['previous'] = previous
    input_df['emp.var.rate'] = emp_var_rate
    input_df['cons.conf.idx'] = cons_conf_idx
    input_df['euribor3m'] = euribor3m
    input_df['nr.employed'] = nr_employed
    input_df['cons.price.idx'] = cons_price_idx
    
    # Map categorical features to one-hot structure
    # NOTE: pd.get_dummies(df, drop_first=True) results in feature names like 'job_blue-collar'
    # If the selected category is NOT the baseline (first one), set its corresponding column to 1
    
    cat_mapping = {
        'job': job, 'marital': marital, 'education': education, 
        'housing': housing, 'loan': loan, 'poutcome': poutcome,
        'contact': 'cellular', # Simplified for UI, assuming common
        'month': 'may', # Simplified, can expand if needed
        'day_of_week': 'mon' # Simplified
    }
    
    for prefix, selection in cat_mapping.items():
        col_name = f"{prefix}_{selection}"
        if col_name in model_features:
            input_df[col_name] = 1
            
    # Apply Scaling
    try:
        input_scaled = scaler.transform(input_df)
        prediction_proba = model.predict_proba(input_scaled)[0][1]
        
        # Log Prediction
        logger.info(f"User Input Prediction: Score {prediction_proba:.4f}")
        
        # Display Result
        st.divider()
        score_percentage = prediction_proba * 100
        
        col_res1, col_res2 = st.columns([1, 2])
        col_res1.metric("Lead Conversion Score", f"{score_percentage:.1f}%")
        
        if score_percentage > 70:
            st.success("🔥 **High Priority Lead**: This customer is very likely to convert.")
            st.balloons()
        elif score_percentage > 40:
            st.warning("⚡ **Medium Priority Lead**: Recommended for follow-up.")
        else:
            st.error("❄️ **Low Priority Lead**: Minimal likelihood of conversion at this time.")
            
        st.info("💡 *Confidence: The model calculates this score based on historical patterns of 40,000+ interactions.*")
        
    except Exception as e:
        logger.error(f"Prediction Error: {e}")
        st.error(f"Model failed to calculate the score: {e}")