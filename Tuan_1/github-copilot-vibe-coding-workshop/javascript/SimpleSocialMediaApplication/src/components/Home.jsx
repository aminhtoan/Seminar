import React from "react";
import PostItem from "./PostItem";

export default function Home({ posts, onSelectPost, currentUser, onLike, onUnlike, onDelete, onEdit }) {
  return (
    <div className="home">
      <div className="home-header">
        <h2>Home Feed</h2>
        <p className="subtitle">Latest posts from everyone</p>
      </div>
      
      <div className="posts-feed">
        {posts.length === 0 ? (
          <div className="empty-feed">
            <p>No posts yet. Be the first to create one!</p>
          </div>
        ) : (
          posts.map(post => (
            <PostItem 
              key={post.id}
              post={post}
              currentUser={currentUser}
              onSelect={() => onSelectPost(post)}
              onLike={() => onLike(post.id)}
              onUnlike={() => onUnlike(post.id)}
              onDelete={() => onDelete(post.id)}
              onEdit={() => onEdit(post)}
            />
          ))
        )}
      </div>
    </div>
  );
}