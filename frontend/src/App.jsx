import Home from "./pages/home"
import Signup from "./pages/signup";
import Login from "./pages/login";
import Dashboard from "./pages/dashboard";
import GeneralAnalysis from "./pages/generalAnalysis";
import TreatmentPlans from "./pages/treatment";
import SelectedTreatmentPlan from "./pages/plan";
import PrivateRoute from "./components/privateRoute";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';


function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/general" element={<GeneralAnalysis />} />
          <Route path="/treatment" element={<TreatmentPlans />} />
          <Route path="/plan" element={<SelectedTreatmentPlan />} />
          <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
