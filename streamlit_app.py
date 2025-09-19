import streamlit as st
import requests
import json

# Gambar header
st.image('https://cdn-icons-png.flaticon.com/128/561/561611.png', width=150)
st.title('🍔 Obesity Level Prediction App')
st.markdown('Masukkan data Anda untuk memprediksi tingkat obesitas dengan lebih presisi.')

st.markdown('---')

col1, col2 = st.columns(2)

with st.expander("📝 Basic Information"):
    with col1:
        Gender = st.selectbox('Gender', ['Female', 'Male'])
        Age = st.number_input('Age', min_value=1, max_value=120, value=25)
        Height = st.number_input('Height (m)', min_value=1.0, max_value=2.5, value=1.70, step=0.01, format="%.2f")

    with col2:
        Weight = st.number_input('Weight (kg)', min_value=30.0, max_value=200.0, value=65.0, step=0.01, format="%.2f")
        family_history_with_overweight = st.selectbox('Family History of Overweight', ['no', 'yes'])
        FAVC = st.selectbox('Frequent Consumption of High-Calorie Food', ['no', 'yes'])

with st.expander("🥗 Eating & Lifestyle Habits"):
    FCVC = st.number_input('Frequency of Vegetable Consumption (1-3)', min_value=0.0, max_value=10.0, value=2.0, step=0.01, format="%.2f")
    NCP = st.number_input('Number of Meals per Day', min_value=0.0, max_value=10.0, value=3.0, step=0.01, format="%.2f")
    CAEC = st.selectbox('Consumption of Food Between Meals', ['no', 'Sometimes', 'Frequently', 'Always'])
    SMOKE = st.selectbox('Do You Smoke?', ['no', 'yes'])
    CH2O = st.number_input('Water Consumption (Liters per Day)', min_value=0.0, max_value=10.0, value=2.0, step=0.01, format="%.2f")
    SCC = st.selectbox('Monitor Calories Consumption', ['no', 'yes'])
    FAF = st.number_input('Physical Activity Frequency (Hours per Week)', min_value=0.0, max_value=20.0, value=1.0, step=0.01, format="%.2f")
    TUE = st.number_input('Time Using Technology Devices (Hours per Day)', min_value=0.0, max_value=24.0, value=1.0, step=0.001, format="%.3f")
    CALC = st.selectbox('Alcohol Consumption', ['no', 'Sometimes', 'Frequently', 'Always'])
    MTRANS = st.selectbox('Transportation Used', ['Automobile', 'Bike', 'Motorbike', 'Public_Transportation', 'Walking'])

st.markdown('---')

inputs = {
    'Gender': Gender,
    'Age': Age,
    'Height': Height,
    'Weight': Weight,
    'family_history_with_overweight': family_history_with_overweight,
    'FAVC': FAVC,
    'FCVC': FCVC,
    'NCP': NCP,
    'CAEC': CAEC,
    'SMOKE': SMOKE,
    'CH2O': CH2O,
    'SCC': SCC,
    'FAF': FAF,
    'TUE': TUE,
    'CALC': CALC,
    'MTRANS': MTRANS
}

if st.button('🚀 Predict'):
    res = requests.post(url='http://127.0.0.1:8501/predict', data=json.dumps(inputs))

    if res.status_code == 200:
        result = res.json()
        st.success(f"🎯 Hasil Prediksi: {result['prediction_label']} (Code: {result['prediction_code']})")
    else:
        st.error('❌ Error: Gagal memproses permintaan.')

st.markdown('---')
st.markdown('Created with ❤️ using Streamlit and FastAPI')
