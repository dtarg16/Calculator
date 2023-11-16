import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import "../styles/Navigation.css";

const Navigation = () => {
  const { isAuthenticated, logout } = useContext(AuthContext);

  return (
    <nav className="navigation">
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        {!isAuthenticated && (
          <li>
            <Link to="/register">Register</Link>
          </li>
        )}
        {!isAuthenticated && (
          <li>
            <Link to="/login">Login</Link>
          </li>
        )}
        {isAuthenticated && (
          <li>
            {isAuthenticated && (
              <button className="logout-button" onClick={() => logout()}>
                Logout
              </button>
            )}
          </li>
        )}
      </ul>
    </nav>
  );
};

export default Navigation;
