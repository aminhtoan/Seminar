import React, { useEffect, useState } from "react";

const API_BASE_URL = "http://localhost:8000";

export default function HealthIndicator() {
  const [status, setStatus] = useState("checking");
  const [lastCheck, setLastCheck] = useState(null);

  const checkHealth = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/health`);
      if (res.ok) {
        setStatus("online");
      } else {
        setStatus("offline");
      }
    } catch {
      setStatus("offline");
    } finally {
      setLastCheck(new Date());
    }
  };

  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 30000); // Check every 30s
    
    return () => clearInterval(interval);
  }, []);

  if (status === "checking") {
    return (
      <div style={{
        background: '#fff3cd', 
        color: '#856404', 
        padding: 8, 
        textAlign: 'center',
        fontSize: '14px'
      }}>
        Checking backend connection...
      </div>
    );
  }
  
  if (status === "online") {
    return (
      <div style={{
        background: '#d4edda', 
        color: '#155724', 
        padding: 8, 
        textAlign: 'center',
        fontSize: '14px',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        gap: '10px'
      }}>
        <span style={{fontSize: '16px'}}>✓</span>
        <span>Backend connected {lastCheck && `(Last check: ${lastCheck.toLocaleTimeString()})`}</span>
      </div>
    );
  }
  
  return (
    <div style={{
      background: '#f8d7da', 
      color: '#721c24', 
      padding: 12, 
      textAlign: 'center',
      fontSize: '14px',
      fontWeight: 'bold'
    }}>
      ⚠️ Backend API is unavailable or unreachable. Some features may not work.
      <div style={{marginTop: '5px', fontSize: '12px', fontWeight: 'normal'}}>
        Make sure the server is running at {API_BASE_URL}
      </div>
    </div>
  );
}