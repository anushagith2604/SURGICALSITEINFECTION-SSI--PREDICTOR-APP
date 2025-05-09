
# utils.py
import pickle
import numpy as np
import pandas as pd

#Load components
with open("ssi_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("scaler.pkl", "rb") as f:
   scaler = pickle.load(f)
with open("label_encoders.pkl", "rb") as f:
    label_encoders = pickle.load(f)

def preprocess_input(data, df_template):
    new_df = pd.DataFrame([data])
    
    for column, le in label_encoders.items():
        if column in new_df.columns:
            if 'Unknown' not in le.classes_:
                most_common = pd.Series(le.classes_).mode()[0]
                new_df[column] = new_df[column].apply(lambda x: x if x in le.classes_ else most_common)
            new_df[column] = le.transform(new_df[column])

    new_df = new_df.fillna(df_template.median(numeric_only=True))
    return scaler.transform(new_df)

def predict_ssi(new_data, df_template):
    processed = preprocess_input(new_data, df_template)
    probability = model.predict_proba(processed)[0][1]
    prediction = model.predict(processed)[0]
    return prediction, probability

import matplotlib.pyplot as plt

def plot_numeric_comparison(new_data, df_template):
    numeric_features = ['BMI_Final', 'Surgery_Duration_Final', 'mic1', 'mic2', 'mic3', 'mic4']

    patient_values = [new_data.get(f, np.nan) for f in numeric_features]
    ssi_avg_values = [df_template[df_template['Outcome'] == 1][f].mean() for f in numeric_features]

    x = np.arange(len(numeric_features))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x - width/2, patient_values, width, label='Patient', color='skyblue')
    ax.bar(x + width/2, ssi_avg_values, width, label='SSI Avg', color='salmon')

    ax.set_ylabel('Risk Percentage')
    ax.set_title('Numeric Feature Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(numeric_features, rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()
    return fig

def plot_categorical_comparison(new_data, df_template, label_encoders):
    categorical_features = ['Sex', 'Patient on Steroid (Last 3 Months)', 'Regular Smoker',
                            'Regular Alcohol Consumer', 'Diabetic (HB1C)']
    plots = []
    for feature in categorical_features:
        le = label_encoders[feature]

        patient_value = new_data.get(feature, 'Unknown')
        if patient_value not in le.classes_:
            patient_value = 'Unknown'

        ssi_group = df_template[df_template['Outcome'] == 1]
        ssi_most_common_encoded = ssi_group[feature].mode()[0]
        ssi_most_common_decoded = le.inverse_transform([ssi_most_common_encoded])[0]

        fig, ax = plt.subplots(figsize=(4, 3))
        ax.bar(['Patient', 'SSI Common'], [1, 1], color=['skyblue', 'salmon'])
        ax.set_title(f"{feature}\n(Patient: {patient_value}, SSI: {ssi_most_common_decoded})")
        ax.set_ylim(0, 1.5)
        ax.get_yaxis().set_visible(False)
        plt.tight_layout()
        plots.append(fig)
    return plots