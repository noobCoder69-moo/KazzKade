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

## API

- User authentication -> `/register/`, `/login/`, `/logout/`
- Global feed -> `/posts/` & `posts/:id/`
- Comments -> `/posts/:id/comments/` & `/comments/:id`
- `/likes/<object_id>/<content_type>/`

# MIT License

© 2025 Kalpan Talukder

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
