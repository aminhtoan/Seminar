import asyncio
import aiosqlite
from datetime import datetime
import uuid

DB_PATH = "sns_api.db"

async def seed():
    async with aiosqlite.connect(DB_PATH) as db:
        # Sample posts
        posts = [
            {
                "id": str(uuid.uuid4()),
                "username": "alice",
                "content": "Hello world! This is Alice.",
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "updatedAt": datetime.utcnow().isoformat() + "Z",
                "likesCount": 1,
                "commentsCount": 1,
            },
            {
                "id": str(uuid.uuid4()),
                "username": "bob",
                "content": "Bob's first post.",
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "updatedAt": datetime.utcnow().isoformat() + "Z",
                "likesCount": 1,
                "commentsCount": 1,
            },
            {
                "id": str(uuid.uuid4()),
                "username": "carol",
                "content": "Carol here! Enjoying FastAPI.",
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "updatedAt": datetime.utcnow().isoformat() + "Z",
                "likesCount": 1,
                "commentsCount": 1,
            },
        ]
        print("Seeding posts...")
        for post in posts:
            await db.execute(
                """
                INSERT INTO posts (id, username, content, createdAt, updatedAt, likesCount, commentsCount)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    post["id"],
                    post["username"],
                    post["content"],
                    post["createdAt"],
                    post["updatedAt"],
                    post["likesCount"],
                    post["commentsCount"],
                ),
            )
        await db.commit()
        print("Seeded 3 posts.")

        # Sample comments
        comments = [
            {
                "id": str(uuid.uuid4()),
                "postId": posts[0]["id"],
                "username": "bob",
                "content": "Nice to meet you Alice!",
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "updatedAt": datetime.utcnow().isoformat() + "Z",
            },
            {
                "id": str(uuid.uuid4()),
                "postId": posts[1]["id"],
                "username": "carol",
                "content": "Welcome Bob!",
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "updatedAt": datetime.utcnow().isoformat() + "Z",
            },
            {
                "id": str(uuid.uuid4()),
                "postId": posts[2]["id"],
                "username": "alice",
                "content": "Glad you like FastAPI, Carol!",
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "updatedAt": datetime.utcnow().isoformat() + "Z",
            },
        ]
        print("Seeding comments...")
        for comment in comments:
            await db.execute(
                """
                INSERT INTO comments (id, postId, username, content, createdAt, updatedAt)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    comment["id"],
                    comment["postId"],
                    comment["username"],
                    comment["content"],
                    comment["createdAt"],
                    comment["updatedAt"],
                ),
            )
        await db.commit()
        print("Seeded 3 comments.")

        # Sample likes
        likes = [
            {
                "postId": posts[0]["id"],
                "username": "bob",
                "likedAt": datetime.utcnow().isoformat() + "Z",
            },
            {
                "postId": posts[1]["id"],
                "username": "carol",
                "likedAt": datetime.utcnow().isoformat() + "Z",
            },
            {
                "postId": posts[2]["id"],
                "username": "alice",
                "likedAt": datetime.utcnow().isoformat() + "Z",
            },
        ]
        print("Seeding likes...")
        for like in likes:
            await db.execute(
                """
                INSERT INTO likes (postId, username, likedAt)
                VALUES (?, ?, ?)
                """,
                (
                    like["postId"],
                    like["username"],
                    like["likedAt"],
                ),
            )
        await db.commit()
        print("Seeded 3 likes.")

if __name__ == "__main__":
    asyncio.run(seed())
