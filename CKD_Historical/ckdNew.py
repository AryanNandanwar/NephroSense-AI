# Import necessary libraries
# Import necessary libraries
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Load the dataset
file_path = 'updated_ckd_dataset_with_stages.csv'  # Replace with your actual dataset path
dataset = pd.read_csv(file_path)

# Encode categorical variables
categorical_cols = ['physical_activity', 'diet', 'smoking', 'alcohol', 
                    'painkiller_usage', 'family_history', 'weight_changes', 'stress_level']

label_encoders = {}  # Dictionary to store label encoders
for col in categorical_cols:
    label_encoders[col] = LabelEncoder()
    dataset[col] = label_encoders[col].fit_transform(dataset[col])

# Separate features and target
X = dataset.drop(columns=['ckd_pred', 'ckd_stage', 'months', 'cluster'])
y = dataset['ckd_stage']  # Target: CKD stage (multi-class classification)

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the numerical features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train a multi-class classification model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict CKD stages for test set
y_pred = model.predict(X_test)

# Evaluate the model
print("CKD Stage Prediction Report")
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")

# Save model and scaler as pickle files
with open('ckd_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

with open('scaler.pkl', 'wb') as scaler_file:
    pickle.dump(scaler, scaler_file)

# Save label encoders
with open('label_encoders.pkl', 'wb') as le_file:
    pickle.dump(label_encoders, le_file)


# ---------------- TEST CASES ---------------- #

# Define test cases as dictionaries
test_cases = [
    {
        'serum_creatinine': 1.2,
        'gfr': 85,
        'bun': 15,
        'serum_calcium': 9.5,
        'ana': 0,
        'c3_c4': 1,
        'hematuria': 0,
        'oxalate_levels': 2.0,
        'urine_ph': 6.5,
        'blood_pressure': 120,
        'physical_activity': 'weekly',
        'diet': 'balanced',
        'water_intake': 2.5,
        'smoking': 'yes',
        'alcohol': 'daily',
        'painkiller_usage': 'yes',
        'family_history': 'yes',
        'weight_changes': 'stable',
        'stress_level': 'moderate'
    },
    {
        'serum_creatinine': 3.8,
        'gfr': 40,
        'bun': 35,
        'serum_calcium': 8.2,
        'ana': 1,
        'c3_c4': 2,
        'hematuria': 1,
        'oxalate_levels': 4.0,
        'urine_ph': 5.8,
        'blood_pressure': 145,
        'physical_activity': 'rarely',
        'diet': 'low salt',
        'water_intake': 1.2,
        'smoking': 'yes',
        'alcohol': 'daily',
        'painkiller_usage': 'yes',
        'family_history': 'no',
        'weight_changes': 'gain',
        'stress_level': 'high'
    }
]

# Predict CKD stage for test cases
print("\n---------------- Test Case Predictions ----------------")
for i, test_data in enumerate(test_cases, 1):
    # Convert categorical inputs using label encoders
    for col in categorical_cols:
        test_data[col] = label_encoders[col].transform([test_data[col]])[0]
    
    # Convert input dictionary to NumPy array
    input_array = np.array(list(test_data.values())).reshape(1, -1)
    
    # Scale numerical features
    input_array = scaler.transform(input_array)  # Use same scaler as training
    
    # Predict CKD stage
    predicted_stage = model.predict(input_array)
    print(f"Test Case {i}: Predicted CKD Stage -> {predicted_stage[0]}")
