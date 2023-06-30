
import './App.css';
import React, { useEffect, useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import axios from 'axios';


function App() {
  const [sessionId, setSessionId] = useState('');
  const [ipAddress, setIPAddress] = useState('');
  const [pasteCount, setPasteCount] = useState(0);
  const [clickCount, setClickCount] = useState(0);

  useEffect(() => {
    // Check if session ID exists in local storage
    const storedSessionId = localStorage.getItem('sessionId');
    const storedTimestamp = localStorage.getItem('timestamp');

    if (storedSessionId && storedTimestamp) {
      const currentTime = new Date().getTime();
      const storedTime = parseInt(storedTimestamp, 10);

      if (currentTime - storedTime <= 300000) {
        // Session ID is still valid, set it from local storage
        setSessionId(storedSessionId);
        return;
      }
    }


    // Generate a new session ID and update local storage
    const generatedSessionId = uuidv4();
    setSessionId(generatedSessionId);
    localStorage.setItem('sessionId', generatedSessionId);
    localStorage.setItem('timestamp', new Date().getTime().toString());
  }, []);


    // Generate Location Country via external API
    const fetchIPAddress = async () => {
      try {
        const response = await axios.get('https://ipinfo.io/json?token=c072b528ff98a3');
        const { country } = response.data;
        setIPAddress(country);
      } catch (error) {
        console.log(error);
      }
    };
    fetchIPAddress();


    // Generate Copy-Paste Count in Password Field 
    const handlePaste = (event) => {
      if (event.target.type === 'password') {
        setPasteCount((prevCount) => prevCount + 1);
      }
    };

    // HHH
    const handleMouseDown = (event) => {
      if (event.button === 0) { // Only capture left mouse clicks (button code 0)
        setClickCount((prevCount) => prevCount + 1);
      }
    };


  return (
    <div onMouseDown={handleMouseDown} >
      <center>
        <p />
        <br />
        <h1>Welcome!</h1>
        <h4>powered by Flink 🐿️</h4>
        <br />
        <br />
        <form>
          <input type="text" placeholder="E-mail" />
          <p />
          <input type="password" placeholder="Password" onPaste={handlePaste} />
          <p />
          <button type="submit">Log In</button>
        </form>
        <p />
        <br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br />
        <p>Session ID: {sessionId}</p> 
        <p />
        <p>Your IP Address is: {ipAddress}</p> 
        <p />
        <p>Number of times password was copy-pasted: {pasteCount}</p>
        <p>Number of left mouse clicks: {clickCount}</p>
      </center>
    </div>
  );
}

export default App;

