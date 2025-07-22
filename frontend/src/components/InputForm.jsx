import React, { useState } from "react";
import './styles/InputForm.module.css';

function InputForm({dataSubmitted, onError}) { 
    // dataSubmitted will be a prop to pass the response data to its parent.
    // Think like a bypass between the form and other component.

    // First it's an empty form so:
    const [formData, completeForm] = useState({
        'heart_max_rate': '',
        'heart_min_rate' : '',
        'heart_rate': '',
        'stress_max': '',
        'stress_min': '',
        'heart_min_rate_lag1': '',
        'heart_min_rate_lag2': '',
        'heart_min_rate_lag3': ''
    });

    // Here, for each field, we need to catch the changes:
    function handleChange(event) {
        const {name, value} = event.target;
        completeForm(prevState => ({
            ...prevState,
            [name] : value
        }));
    };

    // As soon as the user complete the form and send it, then we need to start the flow:
    async function handleSubmit(event) {
        event.preventDefault(); // Prevent default bahavior of the browser (reloded)

        // Docker Compose automatically assigns DNS names to each service based on 
        // the services: name in docker-compose.yml.
        // await fetch('http://localhost:2000/predict' for local development and 
        // await fetch('http://backend:2000/predict' for Docker 
        // BUT JavaScript fetch command runs in the user's browser and the browser 
        // has no idea what the hostname backend means. That name only exists and 
        // is resolvable on the internal Docker network that your containers share. 
        // The fetch call is initiated from your browser, which is outside that network.
        // The browser needs to call an endpoint it can reach, which is your local machine (localhost).
            try {
                // POST request to the backend:
                const response = await fetch(`${import.meta.env.VITE_API_URL}/predict`, 
                    {method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(formData)
                    });

                if (!response.ok) {
                    const errorData = await response.json();
                    
                    // If the backend provided an 'Error' key in the JSON response (as setup in app.py)
                    if (errorData && errorData.Error) { 
                        // Pass the backend error message to the onError prop
                        onError(errorData.Error); 
                    } else {
                        // Fallback message if the backend didn't provide a specific error detail
                        onError(`HTTP error. Status: ${response.status}`);
                    }
                    
                    // We return here to stop the execution flow; we do not need to throw a new Error if we are handling it
                    return;
                }

                    // If everything worked OK then we got a prediction:
                    const data = await response.json()

                    // Now, we need to pass the data back up to a parent component or another handler.
                    // dataSubmitted will be a prop that will receive a function to get the response data
                    // that holds the form to another component.
                    if (dataSubmitted) {
                        dataSubmitted(data);
                    }

                    // Clear the form for the next POST request
                    completeForm({
                               'heart_max_rate': '',
                                'heart_min_rate' : '',
                                'heart_rate': '',
                                'stress_max': '',
                                'stress_min': '',
                                'heart_min_rate_lag1': '',
                                'heart_min_rate_lag2': '',
                                'heart_min_rate_lag3': ''
                            });
    } catch(error) {
        console.error('Error submitting form:', error);
    }
    };

    // Here remember that, we are inyecting JS on HTML for this reason the args will be
    // on camel case (htmlFor, onChange and so on)
    return(
        <div>
            <form onSubmit={handleSubmit}>
                <label htmlFor="heart_max_rate">Your Max Heart Rate of Today: </label>
                <input id="heart_max_rate" name="heart_max_rate" value={formData.heart_max_rate} onChange={handleChange}/>

                <label htmlFor="heart_min_rate">Your Min Heart Rate of Today: </label>
                <input id="heart_min_rate" name="heart_min_rate" value={formData.heart_min_rate} onChange={handleChange}/>

                <label htmlFor="heart_rate">Your Current Heart Rate: </label>
                <input id="heart_rate" name="heart_rate" value={formData.heart_rate} onChange={handleChange}/>
                                
                <label htmlFor="stress_max">Your Max Stress Score of Today: </label>
                <input id="stress_max" name="stress_max" value={formData.stress_max} onChange={handleChange}/>

                <label htmlFor="stress_min">Your Min Stress Score of Today: </label>
                <input id="stress_min" name="stress_min" value={formData.stress_min} onChange={handleChange}/>

                <label htmlFor="heart_min_rate_lag1">Your Min Heart Rate of Yesterday: </label>
                <input id="heart_min_rate_lag1" name="heart_min_rate_lag1" value={formData.heart_min_rate_lag1} onChange={handleChange}/>

                <label htmlFor="heart_min_rate_lag2">Your Min Heart Rate of two days ago: </label>
                <input id="heart_min_rate_lag2" name="heart_min_rate_lag2" value={formData.heart_min_rate_lag2} onChange={handleChange}/>

                <label htmlFor="heart_min_rate_lag3">Your Min Heart Rate of three days ago: </label>
                <input id="heart_min_rate_lag3" name="heart_min_rate_lag3" value={formData.heart_min_rate_lag3} onChange={handleChange}/>

                <button type="submit"> Predict my Stress Score for today</button>
            <footer>IMPORTANT: All the fields must be provided in order to predict your Stress Score. In other way, the app will be crash.</footer>
            </form>
        </div>
    );
}
export default InputForm;
