import React, { useState, useContext } from "react";
import axios from "axios";
import { AuthContext } from "../context/AuthContext";
import "../styles/Calculator.css";

const Calculator = () => {
  const [expression, setExpression] = useState("");
  const [result, setResult] = useState("");
  const { isAuthenticated } = useContext(AuthContext);
  const token = localStorage.getItem("authToken");

  const handleEvaluate = async () => {
    try {
      const config = isAuthenticated
        ? { headers: { Authorization: `Token ${token}` } }
        : {};

      const response = await axios.post(
        "http://localhost:8000/api/calculation/evaluate/",
        { expression },
        config
      );

      if (response.status === 200) {
        setResult(response.data.result);
      }
    } catch (error) {
      console.error("Evaluation error", error.response.data);
      setResult("Error in evaluation");
    }
  };

  return (
    <div className="calculator">
      <h1>Calculator</h1>
      <input
        type="text"
        value={expression}
        onChange={(e) => setExpression(e.target.value)}
        placeholder="Enter expression"
        className="calculator-input"
      />
      <button onClick={handleEvaluate} className="calculator-button">
        Evaluate
      </button>
      <div className="calculator-display">
        <strong>Result:</strong> {result}
      </div>
    </div>
  );
};

export default Calculator;
