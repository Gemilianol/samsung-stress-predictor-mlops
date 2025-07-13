import React from "react";
import style from './styles/CardResult.module.css';

function CardResult({ pred }) {
  // Ensure pred is not null, it's an object and has the 'Prediction' key on it
  if (pred && typeof pred === 'object' && 'Prediction' in pred) {
    return (
      <div id={style.resdiv}>
        <h3>Prediction Result:</h3>
        {/* Access the 'Prediction' key from the pred object */}
        <p>Your Prediction Score is: <strong>{ pred.Prediction }</strong></p> {/*pred will be an object and Prediction the key*/}
      </div>
    );
  } else {
    return null;
  }
}

export default CardResult;