# Nephosense AI  
### Predicting and Managing Chronic Kidney Disease (CKD) Using AI  

Nephosense AI is an advanced AI-powered healthcare application designed to predict the risk of **Chronic Kidney Disease (CKD)** and provide **personalized treatment recommendations** based on patient data. It leverages **machine learning, clustering, and reinforcement learning** to improve CKD diagnosis and management.  

---

## 🚀 Features  

### 🔍 CKD Prediction & Future Risk Analysis  
- Patients provide **test results** (e.g., GFR, Serum Creatinine, BUN).  
- Lifestyle factors like **diet, physical activity, and smoking habits** are collected.  
- The system checks for **CKD diagnosis** based on test results.  
- If no CKD is detected, it predicts:  
  - **Future values of GFR, Serum Creatinine, etc.**  
  - **Risk of CKD diagnosis in the next year.**  
  - **Approximate time when CKD might develop.**  

### 🩺 Personalized Treatment Plans  
- Uses **clustering (KMeans)** to group similar patients.  
- A **supervised learning algorithm** ranks treatment plans based on efficiency.  
- Top **3 recommended treatment plans** are displayed to the user.  
- Patients can provide **feedback**, and a **reinforcement learning model (Q Learning)** adjusts the treatment plan and saves a modified version.  

---

## 🛠 Tech Stack  
- **Frontend**: React (Tailwind CSS for UI)  
- **Backend**: Flask (Python)  
- **Database**: PostgreSQL  
- **Machine Learning**: Scikit-learn, XGBoost, Q-Learning

---

## 🔧 Setup & Installation  

### Backend (Flask) Setup  
```bash
# Clone the repository
git clone https://github.com/yourusername/Nephosense-AI.git
cd Nephosense-AI/backend

# Create a virtual environment and install dependencies
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

# Start the Flask server
python app.py
```

### Frontend (React) Setup  
```bash
# Navigate to the frontend directory
cd ../frontend

# Install dependencies
npm install

# Start the React app
npm start
```

---

## 📊 Database Schema (PostgreSQL)  
- **Patients Table**: Stores patient details, test results, and lifestyle data.  
- **CKD Predictions Table**: Stores past CKD predictions and risk assessments.  
- **Treatment Plans Table**: Stores predefined and dynamically generated treatment plans.  
- **User Feedback Table**: Stores feedback for reinforcement learning adjustments.  

---

## 📜 Machine Learning Approach  
1. **Clustering (DBSCAN)**: Groups patients based on similar medical profiles.  
2. **Supervised Learning Model**: Ranks treatment plans for each patient group.  
3. **Reinforcement Learning**: Improves treatment recommendations based on patient feedback.  

---

## 🛡 Future Enhancements  
- Adding **real-time monitoring** for kidney health.  
- Integrating **IoT wearable data** for better tracking.  
- Expanding the dataset for **more accurate predictions**.  

---

## 🤝 Contributing  

1. **Fork** the repository.  
2. **Create a new branch** (`git checkout -b feature-name`).  
3. **Commit changes** (`git commit -m "Added new feature"`).  
4. **Push to the branch** (`git push origin feature-name`).  
5. **Open a Pull Request**.  

---
.  
