import React, { useState, useContext } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import "../styles/Login.css";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loginError, setLoginError] = useState("");
  const { isAuthenticated, login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoginError("");

    try {
      const response = await axios.post(
        "http://localhost:8000/api/auth/login/",
        { username, password }
      );
      if (response.status === 200) {
        localStorage.setItem("authToken", response.data.token);
        login();
        navigate("/");
      }
    } catch (error) {
      if (error.response && error.response.status === 401) {
        setLoginError("Invalid credentials. Please try again.");
      } else {
        setLoginError("Login failed. Please try again later.");
      }
      console.error("Login error", error.response?.data);
    }
  };

  if (isAuthenticated) {
    navigate("/");
    return null;
  }

  return (
    <div className="login-container">
      <h1 className="login-title">Login</h1>
      <form onSubmit={handleSubmit} className="login-form">
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <button type="submit">Login</button>
      </form>
      {loginError && <p style={{ color: "red" }}>{loginError}</p>}
    </div>
  );
};

export default Login;
