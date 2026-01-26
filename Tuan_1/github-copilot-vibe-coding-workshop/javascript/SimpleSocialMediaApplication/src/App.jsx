import { useState, useEffect } from 'react'
import './App.css'
import Header from './components/Header'
import Home from './components/Home'
import PostDetails from './components/PostDetails'
import PostModal from './components/PostModal'
import NameInputModal from './components/NameInputModal'
import Search from './components/Search'

const API_BASE_URL = 'http://localhost:8000'

function App() {
  const [posts, setPosts] = useState([])
  const [selectedPost, setSelectedPost] = useState(null)
  const [showPostModal, setShowPostModal] = useState(false)
  const [showNameModal, setShowNameModal] = useState(true) // Hiển thị modal nhập tên ban đầu
  const [currentUser, setCurrentUser] = useState('')
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [editingPost, setEditingPost] = useState(null)

  // Fetch posts từ backend
  const fetchPosts = async () => {
    try {
      setLoading(true)
      const response = await fetch(`${API_BASE_URL}/posts`)
      if (!response.ok) throw new Error('Failed to fetch posts')
      const data = await response.json()
      setPosts(data)
    } catch (error) {
      console.error('Error fetching posts:', error)
      // Fallback to mock data
      loadMockData()
    } finally {
      setLoading(false)
    }
  }

  const loadMockData = () => {
    const mockPosts = [
      {
        id: '1',
        username: 'john_doe',
        content: 'Hello everyone! Just joined this awesome platform!',
        createdAt: '2024-01-15T10:30:00Z',
        updatedAt: '2024-01-15T10:30:00Z',
        likesCount: 15,
        commentsCount: 3,
      },
      {
        id: '2',
        username: 'jane_smith',
        content: 'Working on my new React project. So excited!',
        createdAt: '2024-01-14T14:20:00Z',
        updatedAt: '2024-01-14T14:20:00Z',
        likesCount: 28,
        commentsCount: 5,
      },
      {
        id: '3',
        username: 'alex_wong',
        content: 'Just deployed my first full-stack application!',
        createdAt: '2024-01-13T09:15:00Z',
        updatedAt: '2024-01-13T09:15:00Z',
        likesCount: 42,
        commentsCount: 7,
      }
    ]
    setPosts(mockPosts)
  }

  // Load posts khi component mount
  useEffect(() => {
    fetchPosts()
    
    // Kiểm tra nếu có user đã lưu
    const savedUser = localStorage.getItem('socialMediaUser')
    if (savedUser) {
      setCurrentUser(savedUser)
      setShowNameModal(false)
    }
  }, [])

  // Lưu user vào localStorage
  useEffect(() => {
    if (currentUser) {
      localStorage.setItem('socialMediaUser', currentUser)
    }
  }, [currentUser])

  const handleSelectPost = async (post) => {
    try {
      // Fetch post details với comments
      const [postResponse, commentsResponse] = await Promise.all([
        fetch(`${API_BASE_URL}/posts/${post.id}`),
        fetch(`${API_BASE_URL}/posts/${post.id}/comments`)
      ])
      
      if (!postResponse.ok) throw new Error('Failed to fetch post details')
      
      const postDetails = await postResponse.json()
      const comments = commentsResponse.ok ? await commentsResponse.json() : []
      
      setSelectedPost({
        ...postDetails,
        comments
      })
    } catch (error) {
      console.error('Error fetching post details:', error)
      setSelectedPost(post)
    }
  }

  const handleCreatePost = async (postData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/posts`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: currentUser,
          content: postData.content
        })
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.message || 'Failed to create post')
      }

      const newPost = await response.json()
      setPosts([newPost, ...posts])
      setShowPostModal(false)
      
      alert('Post created successfully!')
      
      // Refresh posts list
      fetchPosts()
    } catch (error) {
      console.error('Error creating post:', error)
      alert(`Failed to create post: ${error.message}`)
    }
  }

  const handleDeletePost = async (postId) => {
    if (!window.confirm('Are you sure you want to delete this post?')) {
      return
    }

    try {
      const response = await fetch(`${API_BASE_URL}/posts/${postId}`, {
        method: 'DELETE'
      })

      if (!response.ok) {
        throw new Error('Failed to delete post')
      }

      setPosts(posts.filter(post => post.id !== postId))
      if (selectedPost?.id === postId) {
        setSelectedPost(null)
      }
      
      alert('Post deleted successfully!')
    } catch (error) {
      console.error('Error deleting post:', error)
      alert('Failed to delete post')
    }
  }

  const handleLikePost = async (postId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/posts/${postId}/like?username=${currentUser}`, {
        method: 'POST'
      })
      
      if (response.ok) {
        // Update local state
        setPosts(posts.map(post => 
          post.id === postId 
            ? { ...post, likesCount: post.likesCount + 1 }
            : post
        ))
        
        if (selectedPost?.id === postId) {
          setSelectedPost(prev => ({
            ...prev,
            likesCount: prev.likesCount + 1
          }))
        }
      }
    } catch (error) {
      console.error('Error liking post:', error)
      alert('Failed to like post')
    }
  }

  const handleUnlikePost = async (postId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/posts/${postId}/like?username=${currentUser}`, {
        method: 'DELETE'
      })
      
      if (response.ok) {
        setPosts(posts.map(post => 
          post.id === postId 
            ? { ...post, likesCount: Math.max(0, post.likesCount - 1) }
            : post
        ))
        
        if (selectedPost?.id === postId) {
          setSelectedPost(prev => ({
            ...prev,
            likesCount: Math.max(0, prev.likesCount - 1)
          }))
        }
      }
    } catch (error) {
      console.error('Error unliking post:', error)
      alert('Failed to unlike post')
    }
  }

  const handleAddComment = async (postId, commentData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/posts/${postId}/comments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: currentUser,
          content: commentData.content
        })
      })

      if (!response.ok) {
        throw new Error('Failed to add comment')
      }

      const newComment = await response.json()
      
      // Update selected post
      if (selectedPost?.id === postId) {
        setSelectedPost(prev => ({
          ...prev,
          comments: [newComment, ...(prev.comments || [])],
          commentsCount: prev.commentsCount + 1
        }))
      }
      
      // Update posts list
      setPosts(posts.map(post => 
        post.id === postId 
          ? { ...post, commentsCount: post.commentsCount + 1 }
          : post
      ))
      
      alert('Comment added successfully!')
    } catch (error) {
      console.error('Error adding comment:', error)
      alert('Failed to add comment')
    }
  }

  const handleSearch = (query) => {
    setSearchQuery(query)
  }

  // Filter posts based on search query
  const filteredPosts = posts.filter(post => {
    if (!searchQuery) return true
    const query = searchQuery.toLowerCase()
    return (
      post.content.toLowerCase().includes(query) ||
      post.username.toLowerCase().includes(query)
    )
  })

  const handleEditPost = (post) => {
    setEditingPost(post)
    setShowPostModal(true)
  }

  const handleUpdatePost = async (postId, postData) => {
    // For now, we'll delete and recreate since backend doesn't have update
    await handleDeletePost(postId)
    await handleCreatePost(postData)
    setEditingPost(null)
  }

  if (loading) {
    return (
      <div className="app loading">
        <div className="loading-spinner"></div>
        <p>Loading...</p>
      </div>
    )
  }

  return (
    <div className="app">
      {/* Name Input Modal */}
      {showNameModal && (
        <NameInputModal
          onSubmit={(username) => {
            setCurrentUser(username)
            setShowNameModal(false)
          }}
        />
      )}

      {/* Header */}
      <Header 
        currentUser={currentUser}
        onLogout={() => {
          localStorage.removeItem('socialMediaUser')
          setCurrentUser('')
          setShowNameModal(true)
        }}
      />

      {/* Main Content */}
      <div className="main-content">
        {/* Sidebar */}
        <div className="sidebar">
          <div className="user-profile">
            <div className="avatar">
              {currentUser.charAt(0).toUpperCase()}
            </div>
            <div className="user-info">
              <h3>Hi, There!</h3>
              <p>@{currentUser}</p>
            </div>
          </div>

          <div className="sidebar-menu">
            <button 
              className={`menu-item ${!selectedPost ? 'active' : ''}`}
              onClick={() => setSelectedPost(null)}
            >
              <span className="icon">🏠</span>
              <span>Home</span>
            </button>
            
            <div className="menu-item">
              <span className="icon">🔍</span>
              <Search onSearch={handleSearch} />
            </div>

            <button 
              className="menu-item create-post-btn"
              onClick={() => {
                setEditingPost(null)
                setShowPostModal(true)
              }}
            >
              <span className="icon">✏️</span>
              <span>Create Post</span>
            </button>
          </div>

          {/* Posts List */}
          <div className="posts-preview">
            <h3>Recent Posts</h3>
            <div className="posts-list">
              {filteredPosts.slice(0, 5).map(post => (
                <div 
                  key={post.id} 
                  className={`post-preview ${selectedPost?.id === post.id ? 'active' : ''}`}
                  onClick={() => handleSelectPost(post)}
                >
                  <div className="post-preview-header">
                    <span className="username">@{post.username}</span>
                    <span className="time">{new Date(post.createdAt).toLocaleDateString()}</span>
                  </div>
                  <p className="preview-content">
                    {post.content.length > 50 
                      ? `${post.content.substring(0, 50)}...` 
                      : post.content}
                  </p>
                  <div className="post-stats">
                    <span>❤️ {post.likesCount}</span>
                    <span>💬 {post.commentsCount}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Main Area */}
        <div className="main-area">
          {selectedPost ? (
            <PostDetails
              post={selectedPost}
              currentUser={currentUser}
              onBack={() => setSelectedPost(null)}
              onLike={() => handleLikePost(selectedPost.id)}
              onUnlike={() => handleUnlikePost(selectedPost.id)}
              onDelete={() => handleDeletePost(selectedPost.id)}
              onEdit={() => handleEditPost(selectedPost)}
              onAddComment={handleAddComment}
            />
          ) : (
            <Home 
              posts={filteredPosts}
              onSelectPost={handleSelectPost}
              currentUser={currentUser}
              onLike={handleLikePost}
              onUnlike={handleUnlikePost}
              onDelete={handleDeletePost}
              onEdit={handleEditPost}
            />
          )}
        </div>
      </div>

      {/* Post Modal */}
      {showPostModal && (
        <PostModal
          post={editingPost}
          currentUser={currentUser}
          onSubmit={(data) => {
            if (editingPost) {
              handleUpdatePost(editingPost.id, data)
            } else {
              handleCreatePost(data)
            }
            setShowPostModal(false)
            setEditingPost(null)
          }}
          onClose={() => {
            setShowPostModal(false)
            setEditingPost(null)
          }}
        />
      )}

      {/* Footer */}
      <footer className="footer">
        <p>Simple Social Media © 2024</p>
      </footer>
    </div>
  )
}

export default App