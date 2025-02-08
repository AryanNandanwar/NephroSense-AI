import React, { useState } from 'react';
import axios from 'axios';
import NavigationBar from '../components/navbar';
import Footer from '../components/footer';

const LifestyleMedicalAnalysis = () => {
  const defaultValues = {
    serumCreatinine: '1.2',
    gfr: '90',
    bun: '15',
    serumCalcium: '9.5',
    ana: '1.0',
    c3c4: '0.8',
    hematuria: '0',
    oxalateLevels: '1.5',
    urinePh: '6.0',
    bloodPressure: '120',
    physicalActivity: 'daily',
    diet: 'balanced',
    waterIntake: '2',
    smoking: 'No',
    alcoholConsumption: 'occasionally',
    painkillerUsage: 'No',
    familyHistory: 'No',
    weightChanges: 'stable',
    stressLevel: 'low',
    age:'25',
    gender: 'Male'
  };



  const [formData, setFormData] = useState({
    serumCreatinine: '',
    gfr: '',
    bun: '',
    serumCalcium: '',
    ana: '',
    c3c4: '',
    hematuria: '',
    oxalateLevels: '',
    urinePh: '',
    bloodPressure: '',
    physicalActivity: '',
    diet: '',
    waterIntake: '',
    smoking: '',
    alcoholConsumption: '',
    painkillerUsage: '',
    familyHistory: '',
    weightChanges: '',
    stressLevel: '',
    age:'',
    gender:''
  });

  

  const [prediction, setPrediction] = useState(null);
  

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const token = localStorage.getItem('token')
      if (!token) {
        console.error('No token found. Please log in first.');
        return;
      }
      console.log('Submitting form data:', formData);
      console.log('Using token:', token);
      const response = await axios.post('http://127.0.0.1:8000/predict', 
       formData,
       {
       headers: {
        'Authorization': `Bearer ${token}`, // Include the token
        'Content-Type': 'application/json',
       },
      }
      )

      console.log('Response from backend:', response.data);
      setPrediction(response.data.result);
    } catch (error) {
      if (error.response) {
    // Server responded with a status code outside the 2xx range
    console.error('Backend responded with an error:', error.response.data);
    console.error('Status code:', error.response.status);
  } else if (error.request) {
    // Request was made but no response was received
    console.error('No response received from backend:', error.request);
  } else {
    // Something else happened while setting up the request
    console.error('Error setting up the request:', error.message);
  }
    }
  };

  const handleFillDefaultValues = () => {
    setFormData(defaultValues);
  };

  return (
    <>
      <NavigationBar />
      <div className="w-full py-8">
        <h2 className="pt-16 text-3xl font-bold mb-6 text-center">Comprehensive Health Prediction</h2>
        <form onSubmit={handleSubmit} className="space-y-4 max-w-4xl mx-auto">

        <button
            type="button"
            onClick={handleFillDefaultValues}
            className="mb-4 bg-gray-500 text-white py-2 px-4 rounded-md hover:bg-gray-600"
          >
            Fill Default Values
          </button>
          <h3 className="text-xl font-semibold">Medical Parameters</h3>

          {/* Medical Parameters */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Serum Creatinine</label>
            <input
              type="number"
              name="serumCreatinine"
              value={formData.serumCreatinine}
              onChange={handleChange}
              required
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">GFR</label>
            <input
              type="number"
              name="gfr"
              value={formData.gfr}
              onChange={handleChange}
              required
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">BUN</label>
            <input
              type="number"
              name="bun"
              value={formData.bun}
              onChange={handleChange}
              required
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Serum Calcium</label>
            <input
              type="number"
              name="serumCalcium"
              value={formData.serumCalcium}
              onChange={handleChange}
              required
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">ANA</label>
            <input
              type="number"
              name="ana"
              value={formData.ana}
              onChange={handleChange}
              required
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">C3 and C4</label>
            <input
              type="number"
              name="c3c4"
              value={formData.c3c4}
              onChange={handleChange}
              required
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700">Hematuria</label>
            <input
              type="number"
              name="hematuria"
              value={formData.hematuria}
              onChange={handleChange}
              required
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Oxalate Levels</label>
            <input
              type="number"
              name="oxalateLevels"
              value={formData.oxalateLevels}
              onChange={handleChange}
              required
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Urine pH</label>
            <input
              type="number"
              name="urinePh"
              value={formData.urinePh}
              onChange={handleChange}
              required
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Blood Pressure</label>
            <input
              type="number"
              name="bloodPressure"
              value={formData.bloodPressure}
              onChange={handleChange}
              required
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          

          <h3 className="text-xl font-semibold mt-8">Lifestyle Inputs</h3>

          {/* Lifestyle Inputs */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Physical Activity</label>
            <select
              name="physicalActivity"
              value={formData.physicalActivity}
              onChange={handleChange}
              required
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="">Select</option>
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="rarely">Rarely</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Diet</label>
            <select
              name="diet"
              value={formData.diet}
              onChange={handleChange}
              required
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="">Select</option>
              <option value="high protein">High Protein</option>
              <option value="balanced">Balanced</option>
              <option value="low salt">Low Protein</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Water Intake (liters/day)</label>
            <input
              type="number"
              name="waterIntake"
              value={formData.waterIntake}
              onChange={handleChange}
              required
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Gender</label>
            <select
              name="gender"
              value={formData.gender}
              onChange={handleChange}
              required
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="">Select</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Age</label>
            <input
              type="number"
              name="age"
              value={formData.age}
              onChange={handleChange}
              required
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Smoking</label>
            <select
              name="smoking"
              value={formData.smoking}
              onChange={handleChange}
              required
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="">Select</option>
              <option value="yes">Yes</option>
              <option value="no">No</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Alcohol Consumption</label>
            <select
              name="alcoholConsumption"
              value={formData.alcoholConsumption}
              onChange={handleChange}
              required
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="">Select</option>
              <option value="daily">Daily</option>
              <option value="occasionally">Occasionally</option>
              <option value="never">Never</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Painkiller Usage</label>
            <select
              name="painkillerUsage"
              value={formData.painkillerUsage}
              onChange={handleChange}
              required
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="">Select</option>
              <option value="yes">Yes</option>
              <option value="no">No</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Family History</label>
            <select
              name="familyHistory"
              value={formData.familyHistory}
              onChange={handleChange}
              required
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="">Select</option>
              <option value="yes">Yes</option>
              <option value="no">No</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Weight Changes</label>
            <select
              name="weightChanges"
              value={formData.weightChanges}
              onChange={handleChange}
              required
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="">Select</option>
              <option value="stable">Stable</option>
              <option value="gain">Gain</option>
              <option value="loss">Loss</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Stress Level</label>
            <select
              name="stressLevel"
              value={formData.stressLevel}
              onChange={handleChange}
              required
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="">Select</option>
              <option value="low">Low</option>
              <option value="moderate">Moderate</option>
              <option value="high">High</option>
            </select>
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md mt-6 hover:bg-blue-700"
          >
            Predict
          </button>
        </form>

        {prediction && (
          <div className="mt-8 p-4 bg-green-100 border border-green-500 rounded-md">
            <h3 className="text-lg font-medium">Prediction Result:</h3>
            <p>{prediction}</p>
          </div>
        )}
      </div>
      <Footer />
    </>
  );
};

export default LifestyleMedicalAnalysis;
