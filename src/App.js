import io from 'socket.io-client';
import './App.css';
import React, { useEffect, useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import axios from 'axios';

const socket = io.connect('http://localhost:3001');

function App() {
  const [sessionId, setSessionId] = useState('');
  const [ipAddress, setIPAddress] = useState('');
  const [pasteCount, setPasteCount] = useState(0);
  const [clickCount, setClickCount] = useState(0);
  const [cursorPosition, setCursorPosition] = useState({
    x: 0,
    y: 0,
    timestamp: 0,
  });

  useEffect(() => {
    // Check if session ID exists in local storage
    const storedSessionId = localStorage.getItem('sessionId');
    const storedTimestamp = localStorage.getItem('timestamp');

    if (storedSessionId && storedTimestamp) {
      const currentTime = new Date().getTime();
      const storedTime = parseInt(storedTimestamp, 10);

      if (currentTime - storedTime <= 120000) {
        // Session ID is still valid, set it from local storage
        setSessionId(storedSessionId);
        localStorage.setItem('timestamp', new Date().getTime().toString());
        return;
      }
    }

    // Generate a new session ID and update local storage
    const generatedSessionId = uuidv4();
    setSessionId(generatedSessionId);
    localStorage.setItem('sessionId', generatedSessionId);
    localStorage.setItem('timestamp', new Date().getTime().toString());
  }, []);

  useEffect(() => {
    // Document event listener for cursor position
    const handleMouseMove = (event) => {
      const { clientX, clientY } = event;
      const timestampCursor = new Date().getTime();
      setCursorPosition({ x: clientX, y: clientY, timestamp: timestampCursor });
      socket.emit('cursorMove', {
        sessionId: sessionId,
        x: event.clientX,
        y: event.clientY,
        timestamp_cursor: timestampCursor,
      });
    };

    document.addEventListener('mousemove', handleMouseMove);

    return () => {
      // Cleanup the event listener when component unmounts
      document.removeEventListener('mousemove', handleMouseMove);
    };
  }, [sessionId]);

  // Generate Location Country via external API
  useEffect(() => {
    const fetchIPAddress = async () => {
      try {
        const response = await axios.get(
          'https://ipinfo.io/json?token=c072b528ff98a3'
        );
        const { country } = response.data;
        setIPAddress(country);
      } catch (error) {
        console.log(error);
      }
    };
    fetchIPAddress();
  }, []);

  // Generate Copy-Paste Count in Password Field
  const handlePaste = (event) => {
    if (event.target.type === 'password') {
      setPasteCount((prevCount) => prevCount + 1);
    }
  };

  // Mouse Click Events
  const handleMouseDown = (event) => {
    const timestampClick = new Date().getTime();
    if (event.button === 0) {
      // Only capture left mouse clicks (button code 0)
      setClickCount((prevCount) => prevCount + 1);
      socket.emit('mouseClick', {
        sessionId: sessionId,
        event: 'clickity',
        timestamp_clicks: timestampClick,
      });
    }
  };

  const handleLoginCheck = async (event) => {
    event.preventDefault();
    const body = {
      sessionId: sessionId,
      IP_country_code: ipAddress,
      paste_count: pasteCount,
    };
    try {
      const response = await axios.post(
        'http://localhost:3001/session_input',
        body
      );
      console.log(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div onMouseDown={handleMouseDown}>
      <center>
        <p />
        <br />
        <h1>Welcome!</h1>
        <h4>powered by Flink </h4>
        <h1>🐿️</h1>
        <br />
        <br />
        <form onSubmit={handleLoginCheck}>
          <input
            type="text"
            placeholder="E-mail"
          />
          <p />
          <input
            type="password"
            placeholder="Password"
            onPaste={handlePaste}
          />
          <p />
          <button type="submit">Log In</button>
        </form>
        <p />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <p>Session ID: {sessionId}</p>
        <p />
        <p>Your IP Address is: {ipAddress}</p>
        <p />
        <p>Number of times password was copy-pasted: {pasteCount}</p>
        <p>Number of left mouse clicks: {clickCount}</p>
        <p>
          {' '}
          Cursor Position: X: {cursorPosition.x}, Y: {cursorPosition.y},
          Timestamp: {cursorPosition.timestamp}{' '}
        </p>
      </center>
    </div>
  );
}

export default App;
