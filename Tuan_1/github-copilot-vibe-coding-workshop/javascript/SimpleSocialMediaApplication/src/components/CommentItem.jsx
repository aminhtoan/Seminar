import React from "react";
// Hiển thị chi tiết một bình luận
export default function CommentItem({ comment, onEdit, onDelete }) {
  if (!comment) return null;
  return (
    <div style={{border:'1px solid #eee',padding:8,marginBottom:8}}>
      <div><strong>{comment.username}</strong></div>
      <div>{comment.content}</div>
      <button onClick={onEdit}>Edit</button>
      <button onClick={onDelete}>Delete</button>
    </div>
  );
}
