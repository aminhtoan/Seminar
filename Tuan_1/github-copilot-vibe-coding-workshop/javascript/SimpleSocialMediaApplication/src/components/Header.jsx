import React from "react";

export default function Header({ currentUser, onLogout }) {
  return (
    <header className="header">
      <div className="header-container">
        <div className="logo">
          <h1>📱 SocialMedia</h1>
        </div>
        
        <div className="header-actions">
          {currentUser && (
            <>
              <span className="welcome-text">Welcome, @{currentUser}!</span>
              <button className="logout-btn" onClick={onLogout}>
                Logout
              </button>
            </>
          )}
        </div>
      </div>
    </header>
  );
}