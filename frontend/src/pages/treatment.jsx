import { useState } from "react";
import NavigationBar from "../components/navbar";
import Footer from "../components/footer";

const TreatmentPlans = () => {
  const [treatmentPlans, setTreatmentPlans] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedPlanId, setSelectedPlanId] = useState(null);
  const [successMessage, setSuccessMessage] = useState(""); // State to track selected plan

  // Fetch treatment plans
  const fetchTreatmentPlans = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const token = localStorage.getItem('token')
      if (!token) {
        console.error('No token found. Please log in first.');
        return;
      }
      const response = await fetch("http://127.0.0.1:8000/clustering", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to fetch treatment plans");
      }

      const data = await response.json();
      console.log("API Response:", data);
      setTreatmentPlans(data.treatment_plans.map((plan, index) => ({
        id: plan.id || index + 1, // Use API ID if available, else generate one
        ...plan
      })));
      
    } catch (err) {
      console.error("Error fetching treatment plans:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Select treatment plan
  const selectTreatmentPlan = async (planId) => {
    setSelectedPlanId(planId); // Update state instantly for UI feedback

    try {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('No token found. Please log in first.');
        return;
      }

      const response = await fetch("http://127.0.0.1:8000/select_treatment", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ treatment_id: planId }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to select treatment plan");
      }

      console.log(`Successfully selected treatment plan ID: ${planId}`);
      setSuccessMessage("Treatment plan selected successfully")

    } catch (err) {
      console.error("Error selecting treatment plan:", err);
      setError(err.message);
    }
  };

  const getEfficiencyColor = (efficiency) => {
    if (efficiency >= 15) return "text-green-600"; // High efficiency
    if (efficiency >= 10) return "text-yellow-600"; // Moderate efficiency
    return "text-red-600"; // Low efficiency
  };

  return (
    <div>
      <NavigationBar/>
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4 pt-20">
        <h1 className="text-3xl font-bold mb-4">Treatment Plans</h1>
        <button
          onClick={fetchTreatmentPlans}
          className="px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-600 focus:outline-none"
        >
          Fetch Treatment Plans
        </button>

        {loading && <p className="mt-4 text-gray-700">Loading...</p>}
        {error && <p className="mt-4 text-red-500">{error}</p>}

        <div className="mt-6 w-full max-w-2xl">
          {treatmentPlans.length > 0 ? (
            <ul className="space-y-4">
              {treatmentPlans.map((plan) => (
                <li key={plan.id} className={"bg-white p-4 rounded-lg shadow-md "}>
                  <h2 className="text-xl font-semibold">Plan {plan.id}</h2>
                  <p><span className="font-semibold">Maximum daily sodium intake:</span> {plan.sodium_intake} g</p>
                  <p><span className="font-semibold">Minimum daily water intake:</span> {plan.fluid_intake} litres</p>
                  <p><span className="font-semibold">Diet:</span> {plan.diet}</p>
                  <p><span className="font-semibold">Alcohol Consumption:</span> {plan.alcohol_limit}</p>
                  <p><span className="font-semibold">Physical activity:</span> {plan.physical_activity}</p>
                  <p className={`text-lg font-semibold mt-2 ${getEfficiencyColor(plan.efficiency)}`}>
                    Improvement Rate: {plan.efficiency}%
                  </p>
                  <button
                    onClick={() => selectTreatmentPlan(plan.id)}
                    className="px-4 py-2 bg-green-500 text-white rounded-lg mt-2"
                  >
                    Select Plan
                  </button>
                  {
                    selectedPlanId === plan.id && successMessage && (
                      <p className="mt-2 text-green-600 font-semibold">{successMessage}</p>
                    )
                  }
                </li>
              ))}
            </ul>
          ) : (
            <p className="mt-4 text-gray-700">No treatment plans available</p>
          )}
        </div>
      </div>
      <Footer/>
    </div>
  );
};

export default TreatmentPlans;
