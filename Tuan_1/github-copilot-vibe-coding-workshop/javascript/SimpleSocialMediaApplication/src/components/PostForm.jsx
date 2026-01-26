import React, { useState } from "react";
// Form tạo/sửa bài viết
export default function PostForm({ initial, onSubmit }) {
  const [username, setUsername] = useState(initial?.username || "");
  const [content, setContent] = useState(initial?.content || "");
  return (
    <form onSubmit={e => {e.preventDefault();onSubmit({username,content});}}>
      <input value={username} onChange={e=>setUsername(e.target.value)} placeholder="Username" required maxLength={50} />
      <textarea value={content} onChange={e=>setContent(e.target.value)} placeholder="Content" required maxLength={2000} />
      <button type="submit">Submit</button>
    </form>
  );
}
