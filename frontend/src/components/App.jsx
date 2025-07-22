import React, { useState } from "react";
import InputForm from "./InputForm.jsx";
import CardResult  from "./CardResult.jsx";
import ErrorDisplay from "./ErrorDisplay.jsx";

function App() {
  //  A state variable to hold the data received from the form:
  const [responseData, setResponseData] = useState(null);

  //  Another state if error is received from the form:
  const [formError, setFormError] = useState(null);

  function handleResponseData(data) {
    setResponseData(data);
    setFormError(null); // Clear preview value if it is (just in case)
  };

  function handleError(error) {
    setFormError(error);
    setResponseData(null); // Same here
  }
  
  return (
      <div>
        {/* InputForm should always be rendered so the user can make a submission */}
        <InputForm dataSubmitted={handleResponseData} onError={handleError}/>

        {/* Conditionally rendered => : null at the end means render nothing at first*/}
        {responseData !== null ? (<CardResult pred={responseData} />) : formError !== null ? (<ErrorDisplay error={formError} />) : null}
      </div>
    );
  }

export default App;
