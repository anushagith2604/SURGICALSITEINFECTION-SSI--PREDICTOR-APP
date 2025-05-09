import streamlit as st
import pandas as pd
import pickle
from utils import predict_ssi, plot_numeric_comparison, plot_categorical_comparison, label_encoders


# Load dataset template
df_template = pd.read_csv("data/Shuffled_Cumulative_Dataset.csv")

# Load trained model and scaler
with open("ssi_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# Streamlit App
st.set_page_config(page_title="SSI Risk Predictor", layout="centered")
st.title("🧪 Surgical Site Infection (SSI) Risk Predictor")

st.markdown("Enter patient details to predict the risk of Surgical Site Infection (SSI).")
#st.markdown("""

    #<style>
    #.stApp {
      #  background-color: #f0f4f8;
    #}

    #.main {
     #   background-color: #ffffff;
      #  padding: 2rem;
       # border-radius: 10px;
        #box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    #}

    #.stButton > button {
     #   background-color: #2a5d84;
      #  color: white;
       # font-weight: bold;
        #border-radius: 5px;
        #padding: 0.5rem 1rem;
    #}

  #  .stDataFrame thead {
   #     background-color: #2a5d84;
  #      color: white;
   # }

    #h1, h2, h3 {
     #   color: #2a5d84;
    #}

    #input[type="text"], input[type="number"], textarea {
     #   background-color: #ffffff !important;
      #  color: #000000;
       # border: 1px solid #2a5d84;
       # border-radius: 4px;
       # padding: 0.4rem;
    #}

    #div[data-baseweb="select"] {
     #   background-color: #ffffff !important;
      #  border: 1px solid #2a5d84 !important;
       # border-radius: 4px !important;
       # padding: 0.2rem !important;
    #}

    #div[data-baseweb="select"] > div {
     #   background-color: #ffffff !important;
    #}

    #label {
     #   color: #2a5d84;
      #  font-weight: 500;
    #}
    #</style>


#""", unsafe_allow_html=True)


# Input form
with st.form("patient_form"):
    age = st.number_input("Age (years)", 0, 120, 45)
    sex = st.selectbox("Sex", ['Male', 'Female'])
    steroid = st.selectbox("On Steroid (Last 3 Months)?", ['Yes', 'No'])
    smoker = st.selectbox("Regular Smoker?", ['Yes', 'No'])
    alcohol = st.selectbox("Regular Alcohol Consumer?", ['Yes', 'No'])
    diabetic = st.selectbox("Diabetic (HB1C)", ['High', 'Normal', 'Low'])

    bmi = st.number_input("BMI", 10.0, 50.0, 25.0)
    duration = st.number_input("Surgery Duration (hours)", 0.5, 12.0, 2.0)
    mic1 = st.number_input("MIC1(Cefuroxime)", 0.0, 512.0, 64.0)
    mic2 = st.number_input("MIC2(Cefepime)", 0.0, 512.0, 8.0)
    mic3 = st.number_input("MIC3(Cefoperazone Sulbactum)", 0.0, 512.0, 32.0)
    mic4 = st.number_input("MIC4(Gentamicin)", 0.0, 512.0, 0.248)

    # Hidden or defaulted values
    ecoli = 'Ecoli'
    interp1 = 'Resistant'
    interp2 = 'Susceptible'
    interp3 = 'Intermediate'
    interp4 = 'Sensitive'

    submitted = st.form_submit_button("Predict SSI Risk")

# Construct user input dict
user_input = {
    'Age (years)': age,
    'Sex': sex,
    'Patient on Steroid (Last 3 Months)': steroid,
    'Regular Smoker': smoker,
    'Regular Alcohol Consumer': alcohol,
    'Diabetic (HB1C)': diabetic,
    'BMI_Final': bmi,
    'Surgery_Duration_Final': duration,
    'E.coli': ecoli,
    'mic1': mic1,
    'interpretation1': interp1,
    'mic2': mic2,
    'interpretation2': interp2,
    'mic3': mic3,
    'interpretation3': interp3,
    'mic4': mic4,
    'interpretation4': interp4
}

# Run prediction
if submitted:
    prediction, probability = predict_ssi(user_input, df_template)

     # Construct dynamic data table
    table_data = [
        ["Age (years)", 3, "Administration form,SSI Surveillance Form, SSI Evaluation Tool", "Age entered by patient", "18–65 yrs", "2 (45.94)", "89 (45.94)", "0-20 years: 11,21-40 years: 13, 41-60 years: 17 ,61-80 years: 13", user_input['Age (years)']],
        ["Sex", 3, "Administration Form, SSI Evaluation Tool", "Male / Female", "Male / Female", "Categorical", "Categorical", "Female: 31, Male: 29  ", user_input['Sex']],
        ["Patient on Steroid (Last 3 Months)", 2, "Surgery Procedure Form, SSI Evaluation Tool", "Yes / No,Cortisol Level", "No", "Categorical", "Categorical", 37, user_input['Patient on Steroid (Last 3 Months)']],
        ["Regular Smoker", 2, "Administration Form, SSI Evaluation Tool", "Yes / No,Cotinine", "No", "Categorical", "Categorical", 36, user_input['Regular Smoker']],
        ["Regular Alcohol Consumer", 2, "Surgery Procedure Form, SSI Evaluation Tool", "Yes / No, 2 weeks (CDT)", "No", "Categorical", "Categorical", 39, user_input['Regular Alcohol Consumer']],
        ["Diabetic (HB1C)", 3, "Surgery Procedure Form, SSI surveillance,SSI Evaluation Tool", "Diabetes status/Blood Glucose", "HbA1c < 6.5%", "Normal", "High", 45, user_input['Diabetic (HB1C)']],
        ["BMI_Final", 1, "Administration form", "Height & Weight", "18.5–24.9 normal", "25.58 (32.78)", "40.07 (32.78)", 60, user_input['BMI_Final']],
        ["Surgery_Duration_Final", 2, "Surgery/Event Details , SSI Survellaince Form", "Surgery time in hours", "< 3 hrs", "2.7 (5.22)", "7.3 (5.22)", 58, user_input['Surgery_Duration_Final']],
        ["Cefuroxime", 2, "Microbiology Report, Antibiotic Surveillance", "Bacteria culture", "Protocol dependent", "30 (65.58)", "98 (65.58)", 14, user_input['mic1']],
        ["Cefepime", 3, "Microbiology Report, Antibiotic Surveillance,SSI Surveillance", "Infection index", "Internal scale", "1 (6.96)", "10 (6.96)", 1, user_input['mic2']],
        ["Cefoperazone Sulbactum", 2, "Microbiology Report,Antibiotic Surveillance", "Bacterial colony count", "Range dependent", "0.0 (23.53)", "40.0 (23.53)", 1, user_input['mic3']],
        ["Gentamicin", 2, "Microbiology Report,Antibiotic Surveillance", "MIC concentration", "Drug dependent", "0.158 (1.39)", "3.388 (1.39)", 14, user_input['mic4']],
    ]

    columns = ["Risk Factor", "No. of Forms", "Form Name", "Parameters Used", "Ref. Value", "Min (Avg)", "Max (Avg)", "Count of public", "Prediction Input"]
    display_df = pd.DataFrame(table_data, columns=columns)

    st.markdown("### 📋 Patient Risk Factor Summary")
    st.dataframe(display_df, use_container_width=True)



    if prediction == 1:
        st.error(f"⚠️ RISK of SSI! Probability: {probability:.2%}")
        st.subheader("📊 Feature Comparison with SSI Patients")

        # Plot numeric
        fig = plot_numeric_comparison(user_input, df_template)
        st.pyplot(fig)



    else:
        st.success(f"✅ LOW RISK of SSI! Probability: {probability:.2%}")
        st.markdown("Patient is safe and approved for further medical procedures.") 