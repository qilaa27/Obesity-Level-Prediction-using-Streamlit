import uvicorn
from fastapi import FastAPI
from obesity import ObesityInput
import pandas as pd
import pickle

# Load model pipeline
with open('final_pipeline_model.pkl', 'rb') as file:
    model = pickle.load(file)

app = FastAPI()

# Fungsi untuk mapping data string ke angka
def preprocess_input(input_dict):
    binary_mapping = {
        "Gender": {"Female": 0, "Male": 1},
        "family_history_with_overweight": {"no": 0, "yes": 1},
        "FAVC": {"no": 0, "yes": 1},
        "SMOKE": {"no": 0, "yes": 1},
        "SCC": {"no": 0, "yes": 1}
    }

    caec_mapping = {'no': 0, 'Sometimes': 1, 'Frequently': 2, 'Always': 3}
    calc_mapping = {'no': 0, 'Sometimes': 1, 'Frequently': 2, 'Always': 3}
    mtrans_mapping = {'Automobile': 0, 'Bike': 1, 'Motorbike': 2, 'Public_Transportation': 3, 'Walking': 4}

    processed = input_dict.copy()
    for col in binary_mapping:
        processed[col] = binary_mapping[col][input_dict[col]]

    processed['CAEC'] = caec_mapping[input_dict['CAEC']]
    processed['CALC'] = calc_mapping[input_dict['CALC']]
    processed['MTRANS'] = mtrans_mapping[input_dict['MTRANS']]

    return processed

# Endpoint predict
@app.post('/predict')
def predict(data: ObesityInput):
    input_dict = data.dict()

    # Preprocess data (mapping string ke angka)
    processed_input = preprocess_input(input_dict)

    # Convert to DataFrame
    input_df = pd.DataFrame([processed_input])

    # Predict
    prediction = model.predict(input_df)

    target_labels = {
        0: 'Insufficient_Weight',
        1: 'Normal_Weight',
        2: 'Overweight_Level_I',
        3: 'Overweight_Level_II',
        4: 'Obesity_Type_I',
        5: 'Obesity_Type_II',
        6: 'Obesity_Type_III'
    }

    predicted_label = target_labels[int(prediction[0])]

    return {
        'prediction_code': int(prediction[0]),
        'prediction_label': predicted_label
    }

# Run server
if __name__ == "__main__":
    uvicorn.run("fast_api:app", host="127.0.0.1", port=8501, reload=True)