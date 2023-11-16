import React, { useState, useContext } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import "../styles/Register.css";

const Register = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [registerError, setRegisterError] = useState("");
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setRegisterError("");

    try {
      const response = await axios.post(
        "http://localhost:8000/api/auth/register/",
        { username, email, password }
      );
      if (response.status === 201) {
        localStorage.setItem("authToken", response.data.token);
        login();
        navigate("/");
      }
    } catch (error) {
      console.error("Registration error", error.response?.data);
      setRegisterError("Registration failed. Please try again.");
    }
  };

  return (
    <div className="register-container">
      <h1>Register</h1>
      <form onSubmit={handleSubmit} className="register-form">
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
          required
        />
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <button type="submit">Register</button>
      </form>
      {registerError && <p style={{ color: "red" }}>{registerError}</p>}
    </div>
  );
};

export default Register;
