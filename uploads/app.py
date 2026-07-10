import streamlit as st
import joblib
import pandas as pd

# Load trained model
model = joblib.load("app/predictive_maintenance_model.pkl")

st.title("Predictive Maintenance System")

st.write("Enter Machine Sensor Values")

# Inputs
type_val = st.selectbox("Machine Type (0=L,1=M,2=H)", [0,1,2])

air_temp = st.number_input("Air Temperature")
process_temp = st.number_input("Process Temperature")

rpm = st.number_input("Rotational Speed")

torque = st.number_input("Torque")

tool_wear = st.number_input("Tool Wear")

# Prediction
if st.button("Predict Failure"):

    data = pd.DataFrame([[

        type_val,
        air_temp,
        process_temp,
        rpm,
        torque,
        tool_wear,
        0,0,0,0,0

    ]], columns=[
        "Type",
        "Air temperature [K]",
        "Process temperature [K]",
        "Rotational speed [rpm]",
        "Torque [Nm]",
        "Tool wear [min]",
        "TWF","HDF","PWF","OSF","RNF"
    ])

    prediction = model.predict(data)

    if prediction[0] == 1:
        st.error("⚠ Machine Failure Predicted")
    else:
        st.success("✅ Machine is Healthy")