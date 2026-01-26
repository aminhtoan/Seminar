import os
import yaml
import aiosqlite
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.responses import FileResponse
from typing import List

DB_PATH = os.path.join(os.path.dirname(__file__), "sns_api.db")
OPENAPI_PATH = os.path.join(os.path.dirname(__file__), "..", "openapi.yaml")

# Load OpenAPI YAML
with open(OPENAPI_PATH, "r", encoding="utf-8") as f:
    openapi_yaml = yaml.safe_load(f)

app = FastAPI(
    title=openapi_yaml["info"]["title"],
    description=openapi_yaml["info"].get("description", ""),
    version=openapi_yaml["info"].get("version", "1.0.0"),
    docs_url="/docs",
    redoc_url=None,
    openapi_url=None,  # We'll serve our own OpenAPI YAML
)

# Allow CORS from everywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DB INIT ---
CREATE_POSTS = """
CREATE TABLE IF NOT EXISTS posts (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    content TEXT NOT NULL,
    createdAt TEXT NOT NULL,
    updatedAt TEXT NOT NULL,
    likesCount INTEGER NOT NULL DEFAULT 0,
    commentsCount INTEGER NOT NULL DEFAULT 0
);
"""
CREATE_COMMENTS = """
CREATE TABLE IF NOT EXISTS comments (
    id TEXT PRIMARY KEY,
    postId TEXT NOT NULL,
    username TEXT NOT NULL,
    content TEXT NOT NULL,
    createdAt TEXT NOT NULL,
    updatedAt TEXT NOT NULL,
    FOREIGN KEY(postId) REFERENCES posts(id) ON DELETE CASCADE
);
"""
CREATE_LIKES = """
CREATE TABLE IF NOT EXISTS likes (
    postId TEXT NOT NULL,
    username TEXT NOT NULL,
    likedAt TEXT NOT NULL,
    PRIMARY KEY (postId, username),
    FOREIGN KEY(postId) REFERENCES posts(id) ON DELETE CASCADE
);
"""

@app.on_event("startup")
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(CREATE_POSTS)
        await db.execute(CREATE_COMMENTS)
        await db.execute(CREATE_LIKES)
        await db.commit()

# --- Serve OpenAPI YAML at /openapi.yaml ---
@app.get("/openapi.yaml", include_in_schema=False)
async def serve_openapi_yaml():
    return FileResponse(OPENAPI_PATH, media_type="application/yaml")

# --- Serve Swagger UI at /docs (default FastAPI) ---
# Already handled by FastAPI's docs_url

# --- API ENDPOINTS ---
# Implement endpoints exactly as defined in openapi.yaml
# ... (to be implemented in next steps)

# --- Error Handlers ---
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # Map to openapi.yaml error schema
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "ERROR",
            "message": exc.detail if isinstance(exc.detail, str) else str(exc.detail),
        },
    )

# --- API ENDPOINTS ---
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

# Pydantic Models
class PostBase(BaseModel):
    username: str
    content: str

class PostCreate(PostBase):
    id: Optional[str] = None

class PostResponse(PostBase):
    id: str
    createdAt: str
    updatedAt: str
    likesCount: int
    commentsCount: int

class CommentBase(BaseModel):
    username: str
    content: str

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: str
    postId: str
    createdAt: str
    updatedAt: str

# POSTS ENDPOINTS

@app.get("/api/posts", response_model=List[PostResponse])
async def get_posts():
    """Get all posts"""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT id, username, content, createdAt, updatedAt, likesCount, commentsCount 
            FROM posts 
            ORDER BY createdAt DESC
        """)
        rows = await cursor.fetchall()
        
        posts = []
        for row in rows:
            posts.append({
                "id": row[0],
                "username": row[1],
                "content": row[2],
                "createdAt": row[3],
                "updatedAt": row[4],
                "likesCount": row[5],
                "commentsCount": row[6]
            })
        return posts

@app.post("/api/posts", response_model=PostResponse)
async def create_post(post: PostCreate):
    """Create a new post"""
    post_id = post.id if post.id else str(uuid.uuid4())
    current_time = datetime.now().isoformat()
    
    async with aiosqlite.connect(DB_PATH) as db:
        # Check if post exists
        cursor = await db.execute("SELECT id FROM posts WHERE id = ?", (post_id,))
        if await cursor.fetchone():
            raise HTTPException(status_code=400, detail="Post ID already exists")
        
        # Insert post
        await db.execute("""
            INSERT INTO posts (id, username, content, createdAt, updatedAt, likesCount, commentsCount)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (post_id, post.username, post.content, current_time, current_time, 0, 0))
        
        await db.commit()
    
    return {
        "id": post_id,
        "username": post.username,
        "content": post.content,
        "createdAt": current_time,
        "updatedAt": current_time,
        "likesCount": 0,
        "commentsCount": 0
    }

@app.get("/api/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: str):
    """Get a specific post by ID"""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT id, username, content, createdAt, updatedAt, likesCount, commentsCount 
            FROM posts 
            WHERE id = ?
        """, (post_id,))
        
        row = await cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Post not found")
        
        return {
            "id": row[0],
            "username": row[1],
            "content": row[2],
            "createdAt": row[3],
            "updatedAt": row[4],
            "likesCount": row[5],
            "commentsCount": row[6]
        }

@app.delete("/api/posts/{post_id}")
async def delete_post(post_id: str):
    """Delete a post"""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT id FROM posts WHERE id = ?", (post_id,))
        if not await cursor.fetchone():
            raise HTTPException(status_code=404, detail="Post not found")
        
        await db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        await db.commit()
    
    return {"message": "Post deleted successfully"}

# COMMENTS ENDPOINTS

@app.get("/api/posts/{post_id}/comments", response_model=List[CommentResponse])
async def get_comments(post_id: str):
    """Get all comments for a post"""
    async with aiosqlite.connect(DB_PATH) as db:
        # Check if post exists
        cursor = await db.execute("SELECT id FROM posts WHERE id = ?", (post_id,))
        if not await cursor.fetchone():
            raise HTTPException(status_code=404, detail="Post not found")
        
        cursor = await db.execute("""
            SELECT id, postId, username, content, createdAt, updatedAt 
            FROM comments 
            WHERE postId = ? 
            ORDER BY createdAt DESC
        """, (post_id,))
        
        rows = await cursor.fetchall()
        comments = []
        for row in rows:
            comments.append({
                "id": row[0],
                "postId": row[1],
                "username": row[2],
                "content": row[3],
                "createdAt": row[4],
                "updatedAt": row[5]
            })
        return comments

@app.post("/api/posts/{post_id}/comments", response_model=CommentResponse)
async def create_comment(post_id: str, comment: CommentCreate):
    """Create a comment on a post"""
    # Check if post exists
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT id FROM posts WHERE id = ?", (post_id,))
        if not await cursor.fetchone():
            raise HTTPException(status_code=404, detail="Post not found")
        
        comment_id = str(uuid.uuid4())
        current_time = datetime.now().isoformat()
        
        # Insert comment
        await db.execute("""
            INSERT INTO comments (id, postId, username, content, createdAt, updatedAt)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (comment_id, post_id, comment.username, comment.content, current_time, current_time))
        
        # Update comment count in posts table
        await db.execute("""
            UPDATE posts 
            SET commentsCount = commentsCount + 1, updatedAt = ?
            WHERE id = ?
        """, (current_time, post_id))
        
        await db.commit()
    
    return {
        "id": comment_id,
        "postId": post_id,
        "username": comment.username,
        "content": comment.content,
        "createdAt": current_time,
        "updatedAt": current_time
    }

# LIKES ENDPOINTS

@app.post("/api/posts/{post_id}/like")
async def like_post(post_id: str, username: str):
    """Like a post"""
    async with aiosqlite.connect(DB_PATH) as db:
        # Check if post exists
        cursor = await db.execute("SELECT id FROM posts WHERE id = ?", (post_id,))
        if not await cursor.fetchone():
            raise HTTPException(status_code=404, detail="Post not found")
        
        # Check if already liked
        cursor = await db.execute("""
            SELECT postId, username FROM likes 
            WHERE postId = ? AND username = ?
        """, (post_id, username))
        
        if await cursor.fetchone():
            raise HTTPException(status_code=400, detail="Already liked this post")
        
        current_time = datetime.now().isoformat()
        
        # Add like
        await db.execute("""
            INSERT INTO likes (postId, username, likedAt)
            VALUES (?, ?, ?)
        """, (post_id, username, current_time))
        
        # Update like count
        await db.execute("""
            UPDATE posts 
            SET likesCount = likesCount + 1, updatedAt = ?
            WHERE id = ?
        """, (current_time, post_id))
        
        await db.commit()
    
    return {"message": "Post liked successfully"}

@app.delete("/api/posts/{post_id}/like")
async def unlike_post(post_id: str, username: str):
    """Unlike a post"""
    async with aiosqlite.connect(DB_PATH) as db:
        # Check if like exists
        cursor = await db.execute("""
            SELECT postId, username FROM likes 
            WHERE postId = ? AND username = ?
        """, (post_id, username))
        
        if not await cursor.fetchone():
            raise HTTPException(status_code=404, detail="Like not found")
        
        # Remove like
        await db.execute("""
            DELETE FROM likes 
            WHERE postId = ? AND username = ?
        """, (post_id, username))
        
        # Update like count
        current_time = datetime.now().isoformat()
        await db.execute("""
            UPDATE posts 
            SET likesCount = likesCount - 1, updatedAt = ?
            WHERE id = ?
        """, (current_time, post_id))
        
        await db.commit()
    
    return {"message": "Post unliked successfully"}

# HEALTH CHECK
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/")
async def root():
    return {
        "message": "Social Media API", 
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.yaml"
    }