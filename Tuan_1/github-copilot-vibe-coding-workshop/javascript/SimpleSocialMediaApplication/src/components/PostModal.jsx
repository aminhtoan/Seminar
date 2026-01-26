import React, { useState, useEffect } from "react";

export default function PostModal({ post, currentUser, onSubmit, onClose }) {
  const [content, setContent] = useState(post?.content || "");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!content.trim()) {
      alert("Please write something!");
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit({ content });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{post ? 'Edit Post' : 'Create New Post'}</h2>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        <div className="modal-body">
          <div className="user-info">
            <div className="avatar-small">
              {currentUser.charAt(0).toUpperCase()}
            </div>
            <div>
              <strong>@{currentUser}</strong>
              <p>Posting to everyone</p>
            </div>
          </div>

          <form onSubmit={handleSubmit}>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="What's on your mind?"
              rows="6"
              maxLength="2000"
              required
            />
            
            <div className="modal-actions">
              <button 
                type="button" 
                className="cancel-btn"
                onClick={onClose}
                disabled={isSubmitting}
              >
                Cancel
              </button>
              <button 
                type="submit" 
                className="submit-btn"
                disabled={isSubmitting || !content.trim()}
              >
                {isSubmitting ? 'Posting...' : (post ? 'Update' : 'Post')}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}