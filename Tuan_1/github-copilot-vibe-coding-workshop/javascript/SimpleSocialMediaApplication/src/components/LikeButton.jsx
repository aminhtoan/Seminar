import React from "react";
// Nút like bài viết
export default function LikeButton({ liked, onLike, onUnlike }) {
  return (
    <button onClick={liked ? onUnlike : onLike} style={{color: liked ? 'red' : 'black'}}>
      {liked ? 'Unlike' : 'Like'}
    </button>
  );
}
