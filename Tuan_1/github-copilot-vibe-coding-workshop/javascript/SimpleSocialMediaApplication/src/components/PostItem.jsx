import React, { useState } from "react";

export default function PostItem({ 
  post, 
  currentUser, 
  onSelect, 
  onLike, 
  onUnlike, 
  onDelete, 
  onEdit 
}) {
  const [isLiked, setIsLiked] = useState(false);

  const handleLike = () => {
    if (isLiked) {
      onUnlike();
      setIsLiked(false);
    } else {
      onLike();
      setIsLiked(true);
    }
  };

  return (
    <div className="post-item" onClick={onSelect}>
      <div className="post-item-header">
        <div className="user-avatar-small">
          {post.username.charAt(0).toUpperCase()}
        </div>
        <div className="post-user-info">
          <h4>@{post.username}</h4>
          <span className="post-time">
            {new Date(post.createdAt).toLocaleString()}
          </span>
        </div>
      </div>
      
      <div className="post-content">
        {post.content}
      </div>
      
      <div className="post-stats">
        <span>❤️ {post.likesCount} likes</span>
        <span>💬 {post.commentsCount} comments</span>
      </div>
      
      <div className="post-actions">
        <button 
          className={`action-btn like-btn ${isLiked ? 'liked' : ''}`}
          onClick={(e) => {
            e.stopPropagation();
            handleLike();
          }}
        >
          {isLiked ? '❤️ Liked' : '🤍 Like'}
        </button>
        
        {post.username === currentUser && (
          <>
            <button 
              className="action-btn edit-btn"
              onClick={(e) => {
                e.stopPropagation();
                onEdit();
              }}
            >
              ✏️ Edit
            </button>
            <button 
              className="action-btn delete-btn"
              onClick={(e) => {
                e.stopPropagation();
                onDelete();
              }}
            >
              🗑️ Delete
            </button>
          </>
        )}
      </div>
    </div>
  );
}