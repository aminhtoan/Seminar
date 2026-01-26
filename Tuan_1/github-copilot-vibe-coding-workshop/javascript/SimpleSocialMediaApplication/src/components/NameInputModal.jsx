import React, { useState } from "react";

export default function NameInputModal({ onSubmit }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!username.trim()) {
      alert("Please enter your username!");
      return;
    }
    onSubmit(username);
  };

  return (
    <div className="name-modal-overlay">
      <div className="name-modal-content">
        <div className="name-modal-header">
          <h2>Welcome to SocialMedia! 👋</h2>
          <p>Please enter your information to continue</p>
        </div>

        <div className="name-modal-body">
          <form onSubmit={handleSubmit}>
            <div className="input-group">
              <label htmlFor="username">Username</label>
              <input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter your username"
                required
              />
              <p className="input-hint">This will be displayed as your public name</p>
            </div>

            <button type="submit" className="continue-btn">
              Continue
            </button>
          </form>
        </div>

        <div className="name-modal-footer">
          <p>By continuing, you agree to our Terms of Service</p>
        </div>
      </div>
    </div>
  );
}