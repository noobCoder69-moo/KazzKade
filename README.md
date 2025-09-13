# KazzKade

KazzKade is a Django-based social media API inspired by platforms like Facebook. It supports user registration, authentication, posts, comments, and likes with proper ownership restrictions.

## Features

- **User Management:** Register, login, and logout securely with JWT stored in cookies.  
- **Posts:** Users can create, read, update, and delete their own posts.  
- **Comments:** Users can comment on posts and manage their own comments.  
- **Likes:** Users can like/unlike posts and comments.  
- **Permissions:** Only owners can update or delete their posts/comments.  
- **CORS & CSRF:** Configured for safe frontend integration.

## Tech Stack

- **Backend:** Django 5.2.5, Django REST Framework  
- **Authentication:** JWT (cookie-based)  
- **Database:** SQLite (configurable via `.env`)  
- **Others:** `django-cors-headers` for frontend integration  
