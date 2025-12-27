import React from "react";
import "../styles/ProgressBar.scss";

const ProgressBar = ({ progress }) => {
  return (
    <div className="progress-bar-container progress-bar-container-warning">
      <div className="progress-bar" style={{ width: `${progress}%` }}></div>
    </div>
  );
};

export default ProgressBar;
