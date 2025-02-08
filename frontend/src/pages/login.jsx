
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import NavigationBar from '../components/navbar';
import Footer from '../components/footer';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    const user = { email, password };
  
    try {
      const response = await fetch('http://localhost:8000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(user),
      });
  
      if (response.ok) {
        const data = await response.json();  // Extract the token from the response JSON
        localStorage.setItem('token', data.token);  // Store the token
        navigate('/dashboard');  // Redirect to the dashboard
      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.message || 'Invalid credentials');
        setTimeout(() => {
          setErrorMessage('');
        }, 5000);
      }
    } catch (error) {
      setErrorMessage('An error occurred. Please try again.');
      setTimeout(() => {
        setErrorMessage('');
      }, 5000);
    }
  };
  

  return (
    <>
    <NavigationBar />

    <div className="bg-gray-100 flex justify-center items-center h-screen">
      {/* Left: Image */}
      <div className="w-1/2 h-screen hidden lg:block">
        <img
          src="https://medlineplus.gov/images/ChronicKidneyDisease_share.jpg"
          alt="Placeholder"
          className="object-cover w-full h-full"
        />
      </div>
      {/* Right: Login Form */}
      <div className="lg:p-36 md:p-52 sm:p-20 p-8 w-full lg:w-1/2">
        <h1 className="text-2xl font-semibold mb-4">Login</h1>
        {errorMessage && <p className="text-red-500">{errorMessage}</p>}
        <form onSubmit={handleSubmit}>
          {/* Email Input */}
          <div className="mb-4">
            <label htmlFor="email" className="block text-gray-600">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500"
              autoComplete="off"
              required
            />
          </div>
          {/* Password Input */}
          <div className="mb-4">
            <label htmlFor="password" className="block text-gray-600">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500"
              autoComplete="off"
              required
            />
          </div>
          {/* Remember Me Checkbox */}
          <div className="mb-4 flex items-center">
            <input type="checkbox" id="remember" name="remember" className="text-blue-500" />
            <label htmlFor="remember" className="text-gray-600 ml-2">Remember Me</label>
          </div>
          {/* Forgot Password Link */}
          <div className="mb-6 text-blue-500">
            <a href="#" className="hover:underline">Forgot Password?</a>
          </div>
          {/* Login Button */}
          <button type="submit" className="bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-md py-2 px-4 w-full">
            Login
          </button>
        </form>
        {/* Sign Up Link */}
        <div className="mt-6 text-blue-500 text-center ">
          <Link to="/signup" className="hover:underline">Signup Here</Link>
        </div>
      </div>
    </div>
    <Footer/>
    </>
  );
}

export default Login;
