import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load model components
model = joblib.load('./model/model.pkl')
scaler = joblib.load('scaler.pkl')
le = joblib.load('label_encoder.pkl')
features = joblib.load('features.pkl')

# Updated selected features
selected_features = features

# Mappings for categorical features
application_mode_mapping = {
    "1st phase - general contingent": 1,
    "Ordinance No. 612/93": 2,
    "1st phase - special contingent (Azores Island)": 5,
    "Holders of other higher courses": 7,
    "Ordinance No. 854-B/99": 10,
    "International student (bachelor)": 15,
    "1st phase - special contingent (Madeira Island)": 16,
    "2nd phase - general contingent": 17,
    "3rd phase - general contingent": 18,
    "Ordinance No. 533-A/99, item b2) (Different Plan)": 26,
    "Ordinance No. 533-A/99, item b3 (Other Institution)": 27,
    "Over 23 years old": 39,
    "Transfer": 42,
    "Change of course": 43,
    "Technological specialization diploma holders": 44,
    "Change of institution/course": 51,
    "Short cycle diploma holders": 53,
    "Change of institution/course (International)": 57
}
debt_status_mapping = {'Yes': 1, 'No': 0}
tuition_fees_mapping = {'Yes': 1, 'No': 0}
gender_mapping = {'Male': 0, 'Female': 1}
scholarship_holder_mapping = {'Yes': 1, 'No': 0}

# App layout
st.title("🧑🏻‍🎓 Student Dropout Prediction")

# Input fields
col1, col2 = st.columns(2)
inputs = {}

for idx, feature in enumerate(selected_features):
    if feature == 'Application_mode':
        inputs[feature] = col1.selectbox("Aplication Mode", application_mode_mapping.keys(), key=f"{feature}_{idx}")
    elif feature == 'Debtor':
        inputs[feature] = col1.selectbox("Is the student a debtor?", debt_status_mapping.keys(), key=f"{feature}_{idx}")
    elif feature == 'Tuition_fees_up_to_date':
        inputs[feature] = col1.selectbox("Is the student have tuition fees?", tuition_fees_mapping.keys(), key=f"{feature}_{idx}")
    elif feature == 'Gender':
        inputs[feature] = col1.selectbox("Gender", gender_mapping.keys(), key=f"{feature}_{idx}")
    elif feature == 'Scholarship_holder':
        inputs[feature] = col1.selectbox("Is the student a scholarship holder?", scholarship_holder_mapping.keys(), key=f"{feature}_{idx}")
    elif feature == 'Age_at_enrollment':
        inputs[feature] = col2.number_input("Age at Enrollment", min_value=10, max_value=100, key=f"{feature}_{idx}")
    elif feature == 'Curricular_units_1st_sem_approved':
        inputs[feature] = col2.number_input("Curricular 1st Sem Approved (0 - 30)", min_value=0, max_value=30, key=f"{feature}_{idx}")
    elif feature == 'Curricular_units_1st_sem_grade':
        inputs[feature] = col2.number_input("Curricular 1st Sem Grade (0 - 30)", min_value=0, max_value=30, key=f"{feature}_{idx}")
    elif feature == 'Curricular_units_2nd_sem_approved':
        inputs[feature] = col2.number_input("Curricular 2nd Sem Approved (0 - 30)", min_value=0, max_value=30, key=f"{feature}_{idx}")
    elif feature == 'Curricular_units_2nd_sem_grade':
        inputs[feature] = col2.number_input("Curricular 2nd Sem Grade (0 - 30)", min_value=0, max_value=30, key=f"{feature}_{idx}")

# Validation
valid_inputs = True
error_messages = []

for feature in selected_features:
    if inputs[feature] in ["", None]:
        valid_inputs = False
        error_messages.append(f"{feature} is required.")

# Show errors if any
if not valid_inputs:
    st.error("Please correct the following errors:")
    for msg in error_messages:
        st.write(f"- {msg}")
else:
    # Convert to numerical values
    input_values = []
    for feature in selected_features:
        if feature == 'Application_mode':
            input_values.append(application_mode_mapping[inputs[feature]])
        elif feature == 'Debtor':
            input_values.append(debt_status_mapping[inputs[feature]])
        elif feature == 'Tuition_fees_up_to_date':
            input_values.append(tuition_fees_mapping[inputs[feature]])
        elif feature == 'Gender':
            input_values.append(gender_mapping[inputs[feature]])
        elif feature == 'Scholarship_holder':
            input_values.append(scholarship_holder_mapping[inputs[feature]])
        else:
            input_values.append(float(inputs[feature]))

    # Prepare for prediction
    input_df = pd.DataFrame([input_values], columns=selected_features)
    input_scaled = scaler.transform(input_df)

    if st.button("Make Prediction"):
        prediction = model.predict(input_scaled)
        prediction_label = le.inverse_transform(prediction)
        proba = model.predict_proba(input_scaled)[0]

        st.subheader(f"🎯 Predicted Status: {prediction_label[0]}")
        st.write(f"Confidence: {np.max(proba) * 100:.2f}%")