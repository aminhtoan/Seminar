import React, { useState } from "react";
import CommentForm from "./CommentForm";

export default function PostDetails({
  post,
  currentUser,
  onBack,
  onLike,
  onUnlike,
  onDelete,
  onEdit,
  onAddComment,
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
    <div className="post-details">
      <div className="details-header">
        <button className="back-btn" onClick={onBack}>
          ← Back to Home
        </button>

        {post.username === currentUser && (
          <div className="post-actions">
            <button className="edit-btn" onClick={onEdit}>
              Edit
            </button>
            <button className="delete-btn" onClick={onDelete}>
              Delete
            </button>
          </div>
        )}
      </div>

      <div className="post-content">
        <div className="post-header">
          <div className="user-avatar">
            {post.username.charAt(0).toUpperCase()}
          </div>
          <div className="user-info">
            <h3>@{post.username}</h3>
            <span className="post-time">
              {new Date(post.createdAt).toLocaleString()}
            </span>
          </div>
        </div>

        <div className="post-text">
          <p>{post.content}</p>
        </div>

        <div className="post-stats">
          <button
            className={`like-btn ${isLiked ? "liked" : ""}`}
            onClick={handleLike}
          >
            {isLiked ? "❤️ Liked" : "🤍 Like"} ({post.likesCount})
          </button>
          <span className="comments-count">
            💬 {post.commentsCount} comments
          </span>
        </div>
      </div>

      {/* Comments Section */}
      <div className="comments-section">
        <h3>Comments ({post.commentsCount})</h3>

        <div className="add-comment">
          <CommentForm
            onSubmit={(data) => onAddComment(post.id, data)}
            placeholder="Add a comment..."
          />
        </div>

        <div className="comments-list">
          {post.comments && post.comments.length > 0 ? (
            post.comments.map((comment) => (
              <div key={comment.id} className="comment-item">
                <div className="comment-header">
                  <span className="comment-user">@{comment.username}</span>
                  <span className="comment-time">
                    {new Date(comment.createdAt).toLocaleDateString()}
                  </span>
                </div>
                <div className="comment-content">{comment.content}</div>
              </div>
            ))
          ) : (
            <div className="no-comments">
              <p>No comments yet. Be the first to comment!</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
