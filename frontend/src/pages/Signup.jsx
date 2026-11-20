import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./Signup.css";
import { signupUser } from "../services/authService";

function Signup() {

  const [formData, setFormData] = useState({
    name: "",
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

      const response = await signupUser(formData);

      setMessage("Signup successful!");

      console.log("User Registered:", response);

      setFormData({
        name: "",
        email: "",
        password: ""
      });

    } catch (error) {
      setMessage(
        error.response?.data?.detail || "Signup failed!"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="signup-container">
      <div className="signup-box">
        <h1>Create Account</h1>
        <form onSubmit={handleSubmit}>
          <input type="text" name="name" placeholder="Full Name" value={formData.name} onChange={handleChange} required/>
          <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required/>
          <input type="password" name="password" placeholder="Password" value={formData.password} onChange={handleChange} required minLength={8}/>
          <button type="submit" disabled={loading}>
            {loading ? "Creating Account..." : "Sign Up"} </button>
          {message && <p>{message}</p>}
          <p> Already have an account? <Link to="/"> Login</Link> </p>
        </form>
      </div>
    </div>
  );
}

export default Signup;
