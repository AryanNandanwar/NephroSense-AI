from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from dotenv import load_dotenv
import os
import pickle
import logging
import random
import numpy as np


# Set up the logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

# Example debug message


load_dotenv()

# Access the SECRET_KEY
SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_URI = os.getenv('DATABASE_URI')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}},supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)

ckd_new_model = pickle.load(open('ckd_model.pkl','rb'))
param_model = pickle.load(open('future_params.pkl', 'rb'))
cluster_model = pickle.load(open('cluster_model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))
label_encoders = pickle.load(open('label_encoders.pkl', 'rb'))


class UserTable(db.Model):
    __tablename__ = 'users_table'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(15), nullable=True)
    final_treatment_id = db.Column(db.Integer, db.ForeignKey('final_treatment_plans.id'), nullable=True)
    cluster_no = db.Column(db.Integer, nullable=True)
    
class TestReports(db.Model):
    
     __tablename__ = 'test_report'
     report_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
     user_id = db.Column(db.Integer, db.ForeignKey('users_table.user_id'), nullable=False)
     serum_creatinine = db.Column(db.Float, nullable=False)
     gfr = db.Column(db.Float, nullable=False)
     bun = db.Column(db.Float, nullable=False)
     serum_calcium = db.Column(db.Float, nullable=False)
     ana = db.Column(db.Boolean, nullable=False)
     c3_c4 = db.Column(db.Float, nullable=False)
     hematuria = db.Column(db.Boolean, nullable=False)
     oxalate_levels = db.Column(db.Float, nullable=False)
     urine_ph = db.Column(db.Float, nullable=False)
     blood_pressure = db.Column(db.Float, nullable=False)
     gender = db.Column(db.String, nullable=False)
     age = db.Column(db.Integer, nullable=False)
     physical_activity = db.Column(db.String, nullable=False)
     diet = db.Column(db.String(20), nullable=False)
     family_history = db.Column(db.String(20), nullable=False)
     water_intake = db.Column(db.String(20), nullable=False)
     smoking = db.Column(db.String(20), nullable=False)
     alcohol_consumption = db.Column(db.String(20), nullable=False)
     painkiller_usage = db.Column(db.String(20), nullable=False)
     stress_level = db.Column(db.String(20), nullable=False)
     weight_changes = db.Column(db.String(20), nullable=False)
     ckd_report = db.Column(db.String(255), nullable=True)
     
class FinalTreatmentPlan(db.Model):
    __tablename__ = 'final_treatment_plans'
    id = db.Column(db.Integer, primary_key=True)
    sodium_limit = db.Column(db.String, nullable=True)
    fluid_intake = db.Column(db.String, nullable=True)
    physical_activity = db.Column(db.String, nullable=True)
    diet = db.Column(db.String, nullable=True)
    alcohol_limit = db.Column(db.String, nullable=True)
    cluster = db.Column(db.Integer, nullable=True)
    serum_creatinine = db.Column(db.Float, nullable=True)
    gfr = db.Column(db.Float, nullable=True)
    bun = db.Column(db.Float, nullable=True)
    serum_calcium = db.Column(db.Float, nullable=True)
    oxalate_levels = db.Column(db.Float, nullable=True)
    urine_ph = db.Column(db.Float, nullable=True)
    blood_pressure = db.Column(db.Float, nullable=True)
    sodium_int = db.Column(db.Float, nullable=True)
    fluid_int = db.Column(db.Float, nullable=True)
    
class FinalSelectedPlan(db.Model):
    __tablename__ = 'final_selected_plan'
    key = db.Column(db.Integer, primary_key=True)
    sodium_int = db.Column(db.Float, nullable=True)
    fluid_int = db.Column(db.Float, nullable=True)
    physical_activity = db.Column(db.String, nullable=True)
    diet = db.Column(db.String, nullable=True)
    alcohol_limit = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users_table.user_id'), nullable=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('final_treatment_plans.id'), nullable=True)



    
    
with app.app_context():
    db.create_all()
    
NORMAL_RANGES = {
    "serum_creatinine": 1.0,
    "gfr": 90,
    "bun": 15,
    "serum_calcium": 9.5,
    "oxalate_levels": 3,
    "urine_ph": 5.8,
    "blood_pressure": 120,
}

# Q-learning parameters and actions
actions = [
    "adjust_sodium_limit",
    "adjust_fluid_intake",
    "modify_physical_activity",
    "update_diet",
    "restrict_alcohol"
]
q_table = {action: 0.0 for action in actions}
learning_rate = 0.1
discount_factor = 0.9
epsilon = 0.2
q_threshold = 0.5

# Helper functions for Q-learning
def calculate_difference(old_state, new_state):
    return {key: new_state[key] - old_state[key] for key in old_state}

def select_actions(difference):
    selected_actions = [
        action for action in actions if random.uniform(0, 1) < epsilon or q_table[action] > q_threshold
    ]
    return selected_actions if selected_actions else [random.choice(actions)]

def update_q_table(selected_actions, reward):
    reward_per_action = reward / len(selected_actions)
    for action in selected_actions:
        q_table[action] += learning_rate * (reward_per_action + discount_factor * max(q_table.values()) - q_table[action])

# --- New recommendation functions with 5 options each ---

def determine_physical_activity(state):
    # Option 1: Very high blood pressure
    if state["blood_pressure"] > 160:
        return "Strength exercises twice a week"
    # Option 2: Moderately high blood pressure
    elif state["blood_pressure"] > 140:
        return "Moderate-intensity aerobic activity for 150 minutes per week"
    # Option 3: Reduced kidney function
    elif state["gfr"] < 60:
        return "Low-impact exercises like swimming or cycling 3 times a week"
    # Option 4: Older age
    elif state["gfr"] > 45:
        return "Gentle yoga and stretching exercises twice a week"
    # Option 5: Default recommendation
    else:
        return "Aerobic exercises thrice a week"

def determine_diet_change(state):
    # Option 1: Very high BUN
    if state["bun"] > 25:
        return "Very low-protein diet enriched with fruits and vegetables"
    # Option 2: Moderately high BUN
    elif state["bun"] > 20:
        return "Low-protein diet with an emphasis on lean proteins and vegetables"
    # Option 3: Low serum calcium
    elif state["serum_calcium"] < 8.5:
        return "Calcium-rich diet with vitamin D supplementation"
    # Option 4: Family history of kidney disease (assuming 'positive' indicates risk)
    elif state["serum_creatinine"] > 1.5:
        return "Renal protective diet with controlled protein and sodium intake"
    # Option 5: Default balanced diet
    else:
        return "Balanced diet with controlled protein intake"

def determine_alcohol_limit(state):
    # Option 1: ANA positive—immunological indicator suggesting risk
    if state["ana"]:
        return "Strictly no alcohol"
    # Option 2: Reported excessive or high alcohol consumption
    
    else:
        return "Moderate alcohol consumption within recommended limits"

def dynamic_adjustment(old_state, difference):
    return {
        "sodium_limit_adjustment": round(max(0.1, min(0.7, 0.1 * abs(difference["gfr"]))), 2),
        "fluid_intake_adjustment": round(max(0.2, min(1.0, 0.2 * abs(difference["serum_creatinine"]))), 2),
        "physical_activity_change": determine_physical_activity(old_state),
        "diet_change": determine_diet_change(old_state),
        "alcohol_limit_change": determine_alcohol_limit(old_state),
    }

def oxalate(plan, patient):
    value = patient - (plan/100 * patient)
    return value

def apply_treatment(patient_data, treatment):
    modified_data = patient_data.copy()
    for param, change in treatment.items():
        if param in modified_data:
            if isinstance(change, (float, int)):
                modified_data[param] += change
    return modified_data

def calculate_efficiency(modified_data, normal_ranges):
    efficiency = 0
    total_deviation = 0
    count = 0  # Track the number of valid normal_values

    for param, normal_value in normal_ranges.items():
        if param in modified_data and normal_value != 0:  # Avoid division by zero
            
            deviation = abs(modified_data[param] - normal_value) / normal_value * 100
            # print(normal_value)
            total_deviation += deviation
            count += 1  # Count only valid values
    
    if count == 0:  # Avoid division by zero in efficiency calculation
        return 0  
    
    efficiency = (total_deviation / count)  # Use count instead of fixed 7
    return efficiency

def individual_efficiency(orignal, changes):
    positive = abs(changes)
    percent = positive/ orignal * 100
    if(percent > 10):
        percent -= 10
        
    return round(percent, 2)
    
    
    
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.now() + datetime.timedelta(hours=12),  # Token expiry
        'iat': datetime.datetime.now()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# Utility function to decode JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        if request.method == 'OPTIONS':
            return jsonify({'message': 'Preflight allowed'}), 200

        token = None

        # Check if the token is present in the Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]  # Format: "Bearer <token>"
        
        if not token:
            return jsonify({'error': 'Token is missing! Please log in first.'}), 401

        try:
            # Decode the token
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = data['user_id']
            

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired! Please log in again.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token!'}), 401

        # Pass the `user_id` to the wrapped function
        return f(user_id, *args, **kwargs)
    return decorated

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    hashed_password = generate_password_hash(data['password'])
    new_user = UserTable(
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        contact_number=data.get('contact_number')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully!'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = UserTable.query.filter_by(email=data['email']).first()
    # Check if user exists and password is correct
    if user and check_password_hash(user.password, data['password']):
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user.user_id,  # or any user data you want to include
            'exp': datetime.datetime.now() + datetime.timedelta(hours=1)  # Token expiration
        }, SECRET_KEY, algorithm='HS256')
        # Send the token back to the client
        return jsonify({'message': 'Login successful!', 'token': token})
    
    # If login fails
    return jsonify({'message': 'Invalid email or password!'}), 401

@app.route('/clustering', methods=['POST'])
@token_required
def cluster(user_id):
    try:
        # Parse request data        
        user = db.session.get(UserTable, user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        test_report = db.session.query(TestReports).filter_by(user_id=user_id).order_by(TestReports.report_id.desc()).first()
        if not test_report:
            return jsonify({"error": "Test report not found for the user."}), 404
        
        if test_report.ckd_report == 'No risk of CKD detected within the next 12 months.':
            return jsonify({"message": "No treatment required as no CKD risk detected."}), 200

        # Extract required medical features for clustering
        medical_features = [
            test_report.serum_creatinine, test_report.gfr, test_report.bun,
            test_report.serum_calcium, test_report.oxalate_levels, 
            test_report.urine_ph, test_report.blood_pressure
        ]
        
        
        # Ensure all features are present
        if None in medical_features:
            return jsonify({"error": "Missing required medical features for clustering."}), 400
        
        # Perform clustering
        cluster_label = cluster_model.predict([medical_features])[0]
        
        cluster_int = int(cluster_label)
        user.cluster_no = cluster_int
        db.session.commit()
        
        # Retrieve treatment plans for the predicted cluster
        treatment_plans = FinalTreatmentPlan.query.filter_by(cluster=cluster_int).all()
        if not treatment_plans:
            return jsonify({"message": "No treatment plans found for the predicted cluster.","cluster": cluster}), 404
        
        patient_data = {
            "serum_creatinine": test_report.serum_creatinine,
            "gfr": test_report.gfr,
            "bun": test_report.bun,
            "serum_calcium": test_report.serum_calcium,
            "oxalate_levels": test_report.oxalate_levels,
            "urine_ph": test_report.urine_ph,
            "blood_pressure": test_report.blood_pressure
        }
        

        response = []
        for plan in treatment_plans:
            treatment = {
                "serum_creatinine": plan.serum_creatinine,
                "gfr": plan.gfr,
                "bun": plan.bun,
                "serum_calcium": plan.serum_calcium,
                "oxalate_levels": oxalate(plan.oxalate_levels, test_report.oxalate_levels),
                "urine_ph": plan.urine_ph,
                "blood_pressure": plan.blood_pressure
            }
            modified_data = apply_treatment(patient_data, treatment)
            efficiency = calculate_efficiency(modified_data, patient_data)

            response.append({
                "id": plan.id,
                "sodium_intake": f"Allowed to intake maximum {plan.sodium_int} grams of sodium per day",
                "fluid_intake": f"Supposed to have minimum {plan.fluid_int} litres of fluid per day",
                "physical_activity": plan.physical_activity,
                "diet": plan.diet,
                "alcohol_limit": plan.alcohol_limit,
                "efficiency": round(efficiency, 2)
            })


        response = sorted(response, key=lambda x: x["efficiency"], reverse=True)

        return jsonify({"treatment_plans": response}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    

@app.route('/predict', methods=['POST', 'OPTIONS'])
@token_required
def predict(user_id):

    try:
        # Parse JSON data
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user = db.session.get(UserTable, user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Extract and validate inputs
        try:
            serum_creatinine = float(data.get('serumCreatinine', 0.0))
            gfr = float(data.get('gfr', 0.0))
            bun = float(data.get('bun', 0.0))
            serum_calcium = float(data.get('serumCalcium', 0.0))
            ana = float(data.get('ana', 0.0))
            c3c4 = float(data.get('c3c4', 0.0))
            hematuria = float(data.get('hematuria', 0.0))
            oxalate_levels = float(data.get('oxalateLevels', 0.0))
            urine_ph = float(data.get('urinePh', 0.0))
            blood_pressure = float(data.get('bloodPressure', 0.0))


            physical_activity = label_encoders['physical_activity'].transform([data.get('physicalActivity', 'weekly')])[0]
            age = data.get('age', 0)
            gender = data.get('gender', 'Male')
            diet = label_encoders['diet'].transform([data.get('diet', 'balanced')])[0]
            water_intake = float(data.get('waterIntake', 2.0))
            smoking = label_encoders['smoking'].transform([data.get('smoking', 'no')])[0]
            alcohol_consumption = label_encoders['alcohol'].transform([data.get('alcoholConsumption', 'occasionally')])[0]
            painkiller_usage = label_encoders['painkiller_usage'].transform([data.get('painkillerUsage', 'no')])[0]
            family_history = label_encoders['family_history'].transform([data.get('familyHistory', 'no')])[0]
            weight_changes = label_encoders['family_history'].transform([data.get('familyHistory', 'no')])[0]
            stress_level = label_encoders['stress_level'].transform([data.get('stressLevel', 'moderate')])[0]
            
            physical_activity_db = data.get('physicalActivity','weekly')
            diet_db = data.get('diet', 'balanced')
            smoking_db = data.get('smoking', 'no')
            alcohol_consumption_db = data.get('alcoholConsumption', 'occasionally')
            painkiller_usage_db = data.get('painkillerUsage', 'no')
            family_history_db = data.get('familyHistory', 'no')
            weight_changes_db = data.get('weightChanges', 'stable')
            stress_level_db = data.get('stressLevel', 'moderate')
            
        except ValueError as e:
            return jsonify({'error': 'Invalid input format', 'details': str(e)}), 400

        # Map lifestyle inputs to numerical values
        lifestyle_features = [
           physical_activity, diet, water_intake, smoking, alcohol_consumption, 
           painkiller_usage, family_history, weight_changes, stress_level
        ]
        

        
        future_serum_creatinine = float(data.get('serumCreatinine', 0.0))
        future_gfr = float(data.get('gfr', 0.0))
        future_bun = float(data.get('bun', 0.0))
        future_serum_calcium = float(data.get('serumCalcium', 0.0))
        future_ana = bool(data.get('ana', 0.0))
        future_c3c4 = float(data.get('c3c4', 0.0))
        future_hematuria = bool(data.get('hematuria', 0.0))
        future_oxalate_levels = float(data.get('oxalateLevels', 0.0))
        future_urine_ph = float(data.get('urinePh', 0.0))
        future_blood_pressure = float(data.get('bloodPressure', 0.0))

        # Medical feature inputs
        medical_features = [
            serum_creatinine, gfr, bun, serum_calcium, ana, c3c4,
            hematuria, oxalate_levels, urine_ph, blood_pressure
        ]

        combined_features = np.hstack([medical_features ,lifestyle_features]).reshape(1, -1)
        
        print("Shape of combined_features:", combined_features.shape)
        print("Combined features:", combined_features)
        
        standardized_features = scaler.transform(combined_features)
        number_of_months = 12
        
        future_features = [
            future_serum_creatinine, future_gfr, future_bun, future_serum_calcium, future_ana, future_c3c4,
            future_hematuria, future_oxalate_levels, future_urine_ph, future_blood_pressure  
        ]
        combined_future = np.hstack([future_features , lifestyle_features])
        combined_future = combined_future.reshape(1, -1)
        standardized_future = scaler.transform(combined_future)

        # Predict CKD progression
        ckd_report = 'No risk of CKD detected within the next 12 months.'
        ckd_prediction = ckd_new_model.predict(standardized_features)[0]
        if ckd_prediction != 0:
            ckd_report = f'Patient has CKD. Stage: {ckd_prediction}'     
        else:
            for month in range(1, number_of_months):
                future_features = param_model.predict([np.array(future_features) + month])[0]
                ckd_prediction = ckd_new_model.predict(standardized_future)[0]
                if ckd_prediction != 0:
                    ckd_report = f'At risk of CKD in {month} month(s).'
                    break

                


        # Fetch test report
        test_report = db.session.get(TestReports, user_id)
        if test_report:
            # Update existing report
            test_report.serum_creatinine = serum_creatinine
            test_report.gfr = gfr
            test_report.bun = bun
            test_report.serum_calcium = serum_calcium
            test_report.ana = ana
            test_report.c3_c4 = c3c4
            test_report.hematuria = hematuria
            test_report.oxalate_levels = oxalate_levels
            test_report.urine_ph = urine_ph
            test_report.blood_pressure = blood_pressure
            test_report.gender = gender
            test_report.age = age
            test_report.physical_activity = physical_activity_db
            test_report.diet = diet_db
            test_report.family_history = family_history_db
            test_report.water_intake = water_intake
            test_report.smoking = smoking_db
            test_report.alcohol_consumption = alcohol_consumption_db
            test_report.painkiller_usage = painkiller_usage_db
            test_report.weight_changes = weight_changes_db
            test_report.stress_level = stress_level_db
            test_report.ckd_report = ckd_report
            
        else:
            # Create a new test report
            test_report = TestReports(
                user_id=user_id,
                serum_creatinine=serum_creatinine,
                gfr=gfr,
                bun=bun,
                serum_calcium=serum_calcium,
                ana=ana,
                c3_c4=c3c4,
                hematuria=hematuria,
                oxalate_levels=oxalate_levels,
                urine_ph=urine_ph,
                blood_pressure=blood_pressure,
                gender=gender,
                age=age,
                physical_activity=physical_activity_db,
                diet=diet_db,
                family_history=family_history_db,
                water_intake=water_intake,
                smoking=smoking_db,
                alcohol_consumption=alcohol_consumption_db,
                painkiller_usage=painkiller_usage_db,
                weight_changes = weight_changes_db,
                stress_level=stress_level_db,
                ckd_report=ckd_report
            )
            db.session.add(test_report)

        try:
            db.session.add(test_report)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to save the test report', 'details': str(e)}), 500

        # Return response
        response = jsonify({'result': ckd_report})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
        return response

    except Exception as e:
        print("Error occurred:", str(e))  # For debugging
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@app.route('/select_treatment', methods=['POST'])
@token_required
def select_treatment(user_id):
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user = db.session.get(UserTable, user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        treatment_id = data.get("treatment_id")
        if not treatment_id:
            return jsonify({"error": "No treatment ID provided"}), 400
        print("working")
        
        # Fetch the selected treatment plan from FinalTreatmentPlan
        selected_treatment = db.session.query(FinalTreatmentPlan).filter_by(id=treatment_id).first()
        if not selected_treatment:
            return jsonify({"error": "Treatment plan not found"}), 404

        # Check if the user already has a selected treatment plan in FinalSelectedPlan
        selected_plan = db.session.query(FinalSelectedPlan).filter_by(user_id=user_id).first()

        if selected_plan:
            # Update existing treatment plan with new values or keep old ones
            selected_plan.sodium_int = data.get("sodium_int", selected_treatment.sodium_int)
            selected_plan.fluid_int = data.get("fluid_int", selected_treatment.fluid_int)
            selected_plan.physical_activity = data.get("physical_activity", selected_treatment.physical_activity)
            selected_plan.diet = data.get("diet", selected_treatment.diet)
            selected_plan.alcohol_limit = data.get("alcohol_limit", selected_treatment.alcohol_limit)
            selected_plan.plan_id = data.get("id", selected_treatment.id)
        else:
            # Create new treatment plan entry using values from FinalTreatmentPlan
            new_plan = FinalSelectedPlan(
                user_id=user_id,
                sodium_int=data.get("sodium_int", selected_treatment.sodium_int),
                fluid_int=data.get("fluid_int", selected_treatment.fluid_int),
                physical_activity=data.get("physical_activity", selected_treatment.physical_activity),
                diet=data.get("diet", selected_treatment.diet),
                alcohol_limit=data.get("alcohol_limit", selected_treatment.alcohol_limit),
                plan_id = data.get("id", selected_treatment.id)
            )
            db.session.add(new_plan)

        # Update user's final treatment ID
        user.final_treatment_id = treatment_id
        db.session.commit()

        return jsonify({"message": "Treatment plan selected/updated successfully"}), 200

    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        return jsonify({"error": str(e)}), 500



@app.route('/get_selected_treatment', methods=['POST'])
@token_required
def get_selected_treatment(user_id):
    # Fetch the treatment plan directly from FinalSelectedPlan using user_id
    plan = db.session.query(FinalSelectedPlan).filter_by(user_id=user_id).first()
    id = plan.plan_id
    
    report = db.session.query(TestReports).filter_by(user_id=user_id).first()
    
    orignal_plan = db.session.query(FinalTreatmentPlan).filter_by(id=id).first()
    
    if not orignal_plan:
        return jsonify({"error": "No orignal plan found"}), 404
    
    if not plan:
        return jsonify({"error": "No treatment plan found"}), 404
    
    gfr = individual_efficiency(report.gfr, orignal_plan.gfr)
    serum_creatinine = individual_efficiency(report.serum_creatinine, orignal_plan.serum_creatinine)
    bun = individual_efficiency(report.bun, orignal_plan.bun)
    serum_calcium = individual_efficiency(report.serum_calcium, orignal_plan.serum_calcium)
    oxalate_levels = individual_efficiency(report.oxalate_levels, orignal_plan.oxalate_levels)
    blood_pressure = individual_efficiency(report.blood_pressure, orignal_plan.blood_pressure)
    urine_ph = individual_efficiency(report.urine_ph, orignal_plan.urine_ph)
    
    
    

    return jsonify({
        "sodium_intake": plan.sodium_int,  # Return raw values, not formatted strings
        "fluid_intake": plan.fluid_int,
        "physical_activity": plan.physical_activity,
        "diet": plan.diet,
        "alcohol_limit": plan.alcohol_limit,
        "gfr": gfr,
        "serum_creatinine": serum_creatinine,
        "bun": bun,
        "serum_calcium": serum_calcium,
        "oxalate_levels": oxalate_levels,
        "blood_pressure": blood_pressure,
        "urine_ph": urine_ph
        
    }), 200
    
    
@app.route("/update-treatment", methods=["POST"])
@token_required
def update_treatment(user_id):
    try:
        # Fetch the latest test report for the user
        latest_report = db.session.query(TestReports).filter_by(user_id=user_id).order_by(TestReports.report_id.desc()).first()
        if not latest_report:
            return jsonify({"error": "No test report found for the user"}), 404

        # Build the old_state dictionary from test report fields
        old_state = {
            "serum_creatinine": latest_report.serum_creatinine,
            "gfr": latest_report.gfr,
            "bun": latest_report.bun,
            "serum_calcium": latest_report.serum_calcium,
            "ana": latest_report.ana,
            "c3_c4": latest_report.c3_c4,
            "hematuria": latest_report.hematuria,
            "oxalate_levels": latest_report.oxalate_levels,
            "urine_ph": latest_report.urine_ph,
            "blood_pressure": latest_report.blood_pressure,
        }

        # Retrieve the current treatment plan from the database
        selected_plan = db.session.query(FinalSelectedPlan).filter_by(user_id=user_id).first()
        if not selected_plan:
            return jsonify({"error": "No treatment plan found for the user"}), 404

        treatment_plan = {
            "sodium_limit": selected_plan.sodium_int,
            "fluid_intake": selected_plan.fluid_int,
            "physical_activity": selected_plan.physical_activity,
            "diet": selected_plan.diet,
            "alcohol_limit": selected_plan.alcohol_limit,
            # Optional keys if present in the plan
        }

        # Parse the new state from user input
        data = request.get_json()
        new_state = data.get("new_state")
        if not new_state:
            return jsonify({"error": "Missing new state"}), 400

        # Calculate difference between the old and new state
        difference = calculate_difference(old_state, new_state)

        # Select actions based on the observed differences
        selected_actions = select_actions(difference)

        # Get recommended adjustments based on the dynamic adjustment functions
        adjustments = dynamic_adjustment(old_state, difference)
        for action in selected_actions:
            if action == "adjust_sodium_limit":
                treatment_plan["sodium_limit"] -= adjustments.get("sodium_limit_adjustment", 0)
            elif action == "adjust_fluid_intake":
                treatment_plan["fluid_intake"] -= adjustments.get("fluid_intake_adjustment", 0)
            elif action == "modify_physical_activity":
                treatment_plan["physical_activity"] = adjustments.get("physical_activity_change", treatment_plan["physical_activity"])
            elif action == "update_diet":
                treatment_plan["diet"] = adjustments.get("diet_change", treatment_plan["diet"])
            elif action == "restrict_alcohol":
                treatment_plan["alcohol_limit"] = adjustments.get("alcohol_limit_change", treatment_plan["alcohol_limit"])
            
        # Compute the reward function (example formulation)
        reward = (new_state["gfr"] - old_state["gfr"]) - 5 * (1 if new_state.get("hematuria", False) else 0)

        # Update the Q-table based on the selected actions and reward
        update_q_table(selected_actions, reward)

        # Commit the updated treatment plan to the database
        selected_plan.sodium_int = round(treatment_plan["sodium_limit"], 2)
        selected_plan.fluid_int = round(treatment_plan["fluid_intake"], 2)
        selected_plan.physical_activity = treatment_plan["physical_activity"]
        selected_plan.diet = treatment_plan["diet"]
        selected_plan.alcohol_limit = treatment_plan["alcohol_limit"]

        db.session.commit()

        return jsonify({
            "updated_treatment_plan": treatment_plan,
            "reward": reward,
            "q_table": q_table
        }), 200

    except Exception as e:
        logging.error(f"Error updating treatment: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/health-data', methods=['GET'])
@token_required
def get_health_data(user_id):
    # Query the database for the user's health data
    health_data = TestReports.query.get(user_id)

    if not health_data:
        return jsonify({'error': 'User not found'}), 404

    # Convert the data to a dictionary
    data = {
        'serum_creatinine': health_data.serum_creatinine,
        'gfr': health_data.gfr,
        'bun': health_data.bun,
        'serum_calcium': health_data.serum_calcium,
        'ana': health_data.ana,
        'c3_c4': health_data.c3_c4,
        'hematuria': health_data.hematuria,
        'oxalate_levels': health_data.oxalate_levels,
        'urine_ph': health_data.urine_ph,
        'blood_pressure': health_data.blood_pressure,
        'gender': health_data.gender,
        'age': health_data.age,
        'physical_activity': health_data.physical_activity,
        'diet': health_data.diet,
        'family_history': health_data.family_history,
        'water_intake': health_data.water_intake,
        'smoking': health_data.smoking,
        'alcohol_consumption': health_data.alcohol_consumption,
        'painkiller_usage': health_data.painkiller_usage,
        'stress_level': health_data.stress_level,
        'weight_changes': health_data.weight_changes,
    }

    return jsonify(data), 200


if __name__ == "__main__":
    app.run(debug=True, port=8000)