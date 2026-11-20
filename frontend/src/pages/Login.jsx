import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Login.css";
import { loginUser } from "../services/authService";

function Login() {

  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    email: "",
    password: ""
  });
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);
      setMessage("");
      const response = await loginUser(formData);
      console.log("Login Response:", response);
      localStorage.setItem("token", response.access_token);
      setMessage("Login successful!");
      navigate("/dashboard");
      
    } catch (error) {
      setMessage(
        error.response?.data?.detail || "Invalid email or password"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <h1>Login Here</h1>
        <input type="email" name="email" placeholder="Enter Email" value={formData.email} onChange={handleChange} required/>
        <input type="password" name="password" placeholder="Enter Password" value={formData.password} onChange={handleChange} required />
        <button type="submit" disabled={loading}>{loading ? "Logging in..." : "Login"} </button>
        {message && <p>{message}</p>}
        <p> Don't have an account? <Link to="/signup"> Sign Up</Link> </p>
      </form>
    </div>
  );
}

export default Login;
