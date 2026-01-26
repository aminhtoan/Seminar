import React from "react";
// Danh sách bình luận cho một bài viết
export default function CommentList({ comments, onSelectComment }) {
  if (!comments) return null;
  return (
    <div>
      <h3>Comments</h3>
      {comments.length === 0 && <div>No comments yet.</div>}
      {comments.map(comment => (
        <div key={comment.id} onClick={() => onSelectComment(comment)} style={{marginBottom:8,cursor:'pointer'}}>
          <strong>{comment.username}</strong>: {comment.content}
        </div>
      ))}
    </div>
  );
}
