import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import { AuthContext } from "../context/AuthContext";

const History = () => {
  const [history, setHistory] = useState([]);
  const { isAuthenticated } = useContext(AuthContext);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const token = localStorage.getItem("authToken");
        const config = {
          headers: { Authorization: `Token ${token}` },
        };

        const response = await axios.get(
          "http://localhost:8000/api/calculation/history/",
          config
        );
        if (response.status === 200) {
          setHistory(response.data);
        }
      } catch (error) {
        console.error("Error fetching history", error.response.data);
      }
    };

    if (isAuthenticated) {
      fetchHistory();
    }
  }, [isAuthenticated]);

  if (!isAuthenticated) {
    return <div>Login to access your calculations history</div>;
  }

  return (
    <div>
      <h1>Calculation History</h1>
      <ul>
        {history.map((item, index) => (
          <li key={index}>
            {item.expression} = {item.result}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default History;
