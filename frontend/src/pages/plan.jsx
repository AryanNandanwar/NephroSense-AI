import { useState, useEffect } from "react";
import NavigationBar from "../components/navbar";
import Footer from "../components/footer";

const SelectedTreatmentPlan = () => {
    const [selectedPlan, setSelectedPlan] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [medicalParams, setMedicalParams] = useState({
        serum_creatinine: "",
        gfr: "",
        bun: "",
        serum_calcium: "",
        ana: false,
        c3_c4: "",
        hematuria: false,
        oxalate_levels: "",
        urine_ph: "",
        blood_pressure: ""
    });

    useEffect(() => {
        fetchSelectedPlan();
    }, []);

    const fetchSelectedPlan = async () => {
        setLoading(true);
        setError(null);
    
        try {
            const token = localStorage.getItem("token");
            if (!token) {
                console.error("No token found. Please log in first.");
                return;
            }
    
            const response = await fetch("http://127.0.0.1:8000/get_selected_treatment", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
            });
    
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || "Failed to fetch selected treatment plan");
            }
    
            const data = await response.json();
            setSelectedPlan({
                sodium_intake: data.sodium_intake,  // Use raw value (e.g., 2300)
                fluid_intake: data.fluid_intake,    // Use raw value (e.g., 2.5)
                diet: data.diet,
                alcohol_limit: data.alcohol_limit,
                physical_activity: data.physical_activity
            });
            console.log("Fetched data:", data);
            setSelectedPlan({ ...data });
    
        } catch (err) {
            console.error("Error fetching selected treatment plan:", err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleInputChange = (e) => {
        const { name, value, type, checked } = e.target;
        setMedicalParams(prevState => ({
            ...prevState,
            [name]: type === "checkbox" ? checked : value
        }));
    };

    const updateTreatmentPlan = async () => {
        try {
            const token = localStorage.getItem("token");
            if (!token) {
                console.error("No token found. Please log in first.");
                return;
            }
    
            const formattedParams = {
                new_state: {
                    serum_creatinine: parseFloat(medicalParams.serum_creatinine),
                    gfr: parseFloat(medicalParams.gfr),
                    bun: parseFloat(medicalParams.bun),
                    serum_calcium: parseFloat(medicalParams.serum_calcium),
                    ana: medicalParams.ana,
                    c3_c4: parseFloat(medicalParams.c3_c4),
                    hematuria: medicalParams.hematuria,
                    oxalate_levels: parseFloat(medicalParams.oxalate_levels),
                    urine_ph: parseFloat(medicalParams.urine_ph),
                    blood_pressure: parseFloat(medicalParams.blood_pressure),
                }
            };
            

    
            const response = await fetch("http://127.0.0.1:8000/update-treatment", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                body: JSON.stringify(formattedParams),
            });
            

            
            if (!response.ok) {
                const errorData = await response.json();
                console.error("Error Response from Backend:", errorData);
                throw new Error(errorData.error || "Failed to update treatment plan");
            }
    
            await fetchSelectedPlan();
        } catch (err) {
            console.error("Error updating treatment plan:", err);
            setError("Error updating treatment plan. Please try again.");
        }
    };
    
    const autoFillFeedback = () => {
        setMedicalParams({
            serum_creatinine: "1.2",
            gfr: "90",
            bun: "15",
            serum_calcium: "9.5",
            ana: false,
            c3_c4: "0.8",
            hematuria: true,
            oxalate_levels: "3.5",
            urine_ph: "6.0",
            blood_pressure: "120"
        });
    };

    return (
        <div>
            <NavigationBar />
            <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4 pt-20">
                <h1 className="text-3xl font-bold mb-6">Your Selected Treatment Plan</h1>
                {loading && <p className="text-gray-700">Loading...</p>}
                {error && <p className="text-red-500">{error}</p>}
                {selectedPlan ? (
                    <div className="bg-white shadow-md rounded-lg p-6 max-w-lg w-full">
                        <p><strong>Maximum daily sodium intake:</strong> {selectedPlan.sodium_intake} g</p>
                        <p><strong>Minimum daily water intake:</strong> {selectedPlan.fluid_intake} litres</p>
                        <p><strong>Diet:</strong> {selectedPlan.diet}</p>
                        <p><strong>Alcohol Consumption:</strong> {selectedPlan.alcohol_limit}</p>
                        <p><strong>Physical activity:</strong> {selectedPlan.physical_activity}</p>
                        <p><strong>GFR Improvement Rate: </strong> {selectedPlan.gfr} %</p>
                        <p><strong>Serum Creatinine Improvement Rate:</strong> {selectedPlan.serum_creatinine} %</p>
                        <p><strong>BUN Improvement Rate:</strong> {selectedPlan.bun} %</p>
                        <p><strong>Serum Calcium Improvement Rate:</strong> {selectedPlan.serum_calcium} %</p>
                        <p><strong>Blood Pressure Improvement Rate:</strong> {selectedPlan.blood_pressure} %</p>
                        <p><strong>Oxalate Levels Improvement Rate:</strong> {selectedPlan.oxalate_levels} %</p>
                        <p><strong>Urine pH Improvement Rate:</strong> {selectedPlan.urine_ph} %</p>
                    </div>
                ) : (
                    <p className="text-gray-700">No treatment plan selected.</p>
                )}
                <div className="mt-6 bg-white shadow-md rounded-lg p-6 max-w-lg w-full">
                    <h2 className="text-xl font-semibold mb-4">Update Medical Parameters</h2>
                    {Object.keys(medicalParams).map(param => (
                        <div key={param} className="mb-4">
                            <label className="block text-gray-700 font-semibold">{param.replace("_", " ").toUpperCase()}</label>
                            {typeof medicalParams[param] === "boolean" ? (
                                <input
                                    type="checkbox"
                                    name={param}
                                    checked={medicalParams[param]}
                                    onChange={handleInputChange}
                                    className="mt-1"
                                />
                            ) : (
                                <input
                                    type="number"
                                    name={param}
                                    value={medicalParams[param]}
                                    onChange={handleInputChange}
                                    className="w-full p-2 border rounded-md focus:outline-none focus:ring focus:border-blue-500"
                                />
                            )}
                        </div>
                    ))}
                    <div className="flex space-x-4">
                        <button className="mt-4 px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600" onClick={autoFillFeedback}>Auto-Fill Feedback</button>
                        <button className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600" onClick={updateTreatmentPlan}>Update Treatment Plan</button>
                    </div>
                </div>
            </div>
            <Footer />
        </div>
    );
};

export default SelectedTreatmentPlan;
