
import NavigationBar from "../components/navbar";
import Footer from "../components/footer";
import React, { useEffect, useState } from 'react';
import { Bar, Line, Pie } from 'react-chartjs-2';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const Dashboard = () => {
  const [healthData, setHealthData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHealthData = async () => {
      try {
        const token = localStorage.getItem('token'); // Assuming token is stored in localStorage
        const response = await fetch('http://localhost:8000/health-data', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch health data');
        }

        const data = await response.json();
        setHealthData(data);
        setLoading(false);
      } catch (error) {
        setError(error.message);
        setLoading(false);
      }
    };

    fetchHealthData();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;
  if (!healthData) return <p>No data available</p>;

  const {
    serum_creatinine,
    gfr,
    bun,
    serum_calcium,
    ana,
    c3_c4,
    hematuria,
    oxalate_levels,
    urine_ph,
    blood_pressure,
    physical_activity,
    diet,
    water_intake,
    smoking,
    alcohol_consumption,
    painkiller_usage,
    stress_level,
    weight_changes,
  } = healthData;

  const medicalData = {
    labels: ['Serum Creatinine', 'GFR', 'BUN', 'Serum Calcium', 'C3/C4', 'Oxalate Levels', 'Urine pH', 'Blood Pressure'],
    datasets: [
      {
        label: 'Medical Parameters',
        data: [serum_creatinine, gfr, bun, serum_calcium, c3_c4, oxalate_levels, urine_ph, blood_pressure],
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  const lifestyleData = {
    labels: ['Physical Activity', 'Diet', 'Water Intake', 'Smoking', 'Alcohol', 'Painkiller Usage', 'Stress Level', 'Weight Changes'],
    datasets: [
      {
        label: 'Lifestyle Parameters',
        data: [
          physical_activity === 'weekly' ? 1 : 0,
          diet === 'balanced' ? 1 : 0,
          parseFloat(water_intake),
          smoking === 'yes' ? 1 : 0,
          alcohol_consumption === 'yes' ? 1 : 0,
          painkiller_usage === 'yes' ? 1 : 0,
          stress_level === 'high' ? 1 : 0,
          weight_changes === 'yes' ? 1 : 0,
        ],
        backgroundColor: 'rgba(153, 102, 255, 0.6)',
        borderColor: 'rgba(153, 102, 255, 1)',
        borderWidth: 1,
      },
    ],
  };

  const booleanData = {
    labels: ['ANA', 'Hematuria'],
    datasets: [
      {
        label: 'Boolean Parameters',
        data: [ana ? 1 : 0, hematuria ? 1 : 0],
        backgroundColor: ['rgba(255, 99, 132, 0.6)', 'rgba(54, 162, 235, 0.6)'],
        borderColor: ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)'],
        borderWidth: 1,
      },
    ],
  };

  return (
    <div>
      <NavigationBar/>
    <div className="p-6 bg-gray-100 min-h-screen">
      
      <h1 className="text-3xl font-bold mb-6">Health Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Medical Parameters</h2>
          <Bar data={medicalData} />
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Lifestyle Parameters</h2>
          <Line data={lifestyleData} />
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Boolean Parameters</h2>
          <Pie data={booleanData} />
        </div>
      </div>
      
    </div>
    <Footer/>
    </div>
  );
};

export default Dashboard;
