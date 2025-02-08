Nephosense AI
Predicting and Managing Chronic Kidney Disease (CKD) Using AI
🚀 Overview
Nephosense AI is an advanced AI-powered healthcare application designed to predict the risk of Chronic Kidney Disease (CKD) and provide personalized treatment recommendations based on patient data. It leverages machine learning, clustering, and reinforcement learning to improve CKD diagnosis and management.

🏗 Features
🔍 CKD Prediction & Future Risk Analysis
Patients provide blood and urine test results (e.g., GFR, Serum Creatinine, BUN).
Lifestyle factors like diet, physical activity, and smoking habits are collected.
The system checks for CKD diagnosis based on test results.
If no CKD is detected, it predicts:
Future values of GFR, Serum Creatinine, etc.
Risk of CKD diagnosis in the next year.
Approximate time when CKD might develop.
🩺 Personalized Treatment Plans
Uses clustering (DBSCAN) to group similar patients.
A supervised learning algorithm ranks treatment plans based on efficiency.
Top 3 recommended treatment plans are displayed to the user.
Patients can provide feedback, and a reinforcement learning model adjusts the treatment plan and saves a modified version.
🛠 Tech Stack
Frontend: React (Tailwind CSS for UI)
Backend: Flask (Python)
Database: PostgreSQL
Machine Learning: Scikit-learn, XGBoost, Reinforcement Learning Algorithms
🔧 Setup & Installation
Backend (Flask) Setup
Clone the repository:
bash
Copy
Edit
git clone https://github.com/yourusername/Nephosense-AI.git
cd Nephosense-AI/backend
Create a virtual environment and install dependencies:
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
Start the Flask server:
bash
Copy
Edit
python app.py
Frontend (React) Setup
Navigate to the frontend directory:
bash
Copy
Edit
cd ../frontend
Install dependencies:
bash
Copy
Edit
npm install
Start the React app:
bash
Copy
Edit
npm start
📊 Database Schema (PostgreSQL)
Patients Table: Stores patient details, test results, and lifestyle data.
CKD Predictions Table: Stores past CKD predictions and risk assessments.
Treatment Plans Table: Stores predefined and dynamically generated treatment plans.
User Feedback Table: Stores feedback for reinforcement learning adjustments.
📜 Machine Learning Approach
Clustering (DBSCAN): Groups patients based on similar medical profiles.
Supervised Learning Model: Ranks treatment plans for each patient group.
Reinforcement Learning: Improves treatment recommendations based on patient feedback.
🛡 Future Enhancements
Adding real-time monitoring for kidney health.
Integrating IoT wearable data for better tracking.
Expanding the dataset for more accurate predictions.
🤝 Contributing
Fork the repository.
Create a new branch (git checkout -b feature-name).
Commit changes (git commit -m "Added new feature").
Push to the branch (git push origin feature-name).
Open a Pull Request.
