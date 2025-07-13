import React from "react";
import style from './styles/ErrorDisplay.module.css';

function ErrorDisplay({ error }) {
  if (error !== null) {
    return (
      <div>
        <h3 id={style.invalid}>Something was wrong:</h3>
        <p id={style.invalid}><strong>{ error }</strong></p>
      </div>
    );
  } else {
    return null;
  }
}

export default ErrorDisplay;