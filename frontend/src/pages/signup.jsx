// src/components/Signup.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import NavigationBar from '../components/navbar';
import Footer from '../components/footer';

function Signup() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [contact, setContact] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const newUser = { name, email, password, contact };

    try {
      // Replace with your actual API endpoint for signup
      const response = await fetch('http://localhost:8000/api/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newUser),
      });

      if (response.ok) {
        navigate('/login'); // Redirect to login after successful signup
      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.message || 'Signup failed');
      }
    } catch (error) {
      setErrorMessage('An error occurred. Please try again.');
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
        <h1 className="text-2xl font-semibold mb-4">Sign Up</h1>
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

          <div className="mb-4">
            <label htmlFor="name" className="block text-gray-600">Name</label>
            <input
                type="text"
                id="name"
                name="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500"
                autoComplete="off"
                required
            />
          </div>

        <div className="mb-4">
            <label htmlFor="contact" className="block text-gray-600">Contact Number</label>
            <input
                type="tel"
                id="contact"
                name="contact"
                value={contact}
                onChange={(e) => setContact(e.target.value)}
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
          
          
          {/* Forgot Password Link */}
          <div className="mb-6 text-blue-500">
            <a href="#" className="hover:underline">Forgot Password?</a>
          </div>
          {/* Login Button */}
          <button type="submit" className="bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-md py-2 px-4 w-full">
          Sign Up
          </button>
        </form>
        {/* Sign Up Link */}
        <div className="mt-6 text-blue-500 text-center ">
          <Link to="/login" className="hover:underline">Login Here</Link>
        </div>
      </div>
    </div>
    <Footer/>
    </>
  );
}

export default Signup;
