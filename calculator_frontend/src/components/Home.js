import React from "react";
import Calculator from "./Calculator";
import History from "./History";
import "../styles/Home.css";

const Home = () => {
  return (
    <div className="home-container">
      <Calculator />
      <History />
    </div>
  );
};

export default Home;
