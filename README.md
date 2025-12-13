# MyBlog
一个基于 **Django + Django REST Framework** 的 Headless 博客系统，支持前后端分离架构，覆盖从 API 设计、数据建模、测试、前端交互、OAuth 登录、Docker 化部署到 CI/CD 的完整软件工程流程。

本项目适用于：
- 个人博客系统
- 后端 / 全栈学习项目
- 简历展示项目（Backend / Full-Stack）

---

## 1. Project Overview

### 1.1 Project Goals
- 构建一个 **Headless CMS 风格** 的博客系统
- 前后端通过 REST API 解耦
- 遵循标准软件工程开发流程（需求 → 设计 → 实现 → 测试 → 部署）
- 具备良好的可扩展性与工程规范

### 1.2 Target Users
- 博客作者（内容管理）
- 普通访客（浏览、搜索、评论）
- 管理员（系统配置与内容审核）

---

## 2. Functional Requirements

### 2.1 Blog Frontend Features（用户侧）
- 博客首页（文章列表）
- 博客搜索
- 博客文章浏览
- 博客文章详情页
- 博客评论
- 专栏 / 分类页
- 标签页
- 归档页（按时间）
- 关于我（About）
- 留言板
- 登录页面（OAuth / 本地）

### 2.2 Admin Backend Features（管理侧）
- 管理员登录与身份认证
- 博客文章管理（CRUD）
- Markdown 编辑器整合
- 分类管理
- 标签管理
- 评论管理
- 友链管理
- 文件上传与管理
- 菜单与页面配置
- 系统配置
- 数据统计与常用交互功能

---

## 3. System Architecture

### 3.1 High-Level Architecture
- **Backend**: Django + Django REST Framework
- **Frontend**: Web UI（通过 REST API 交互）
- **Database**: MySQL
- **Authentication**: Google / GitHub OAuth2
- **Containerization**: Docker / Docker Compose
- **CI/CD**: GitHub Actions → Docker Hub

---

## 4. API Design (Headless Blog API)

### 4.1 Blog Post API

#### 4.1.1 List Blog Posts
**Endpoint**
GET /blog/

**Sample Command**
```bash
curl http://localhost:8080/blog/
```
Response Example
```json
{
  "posts": [
    {
      "id": 1,
      "title": "First Post",
      "content": "This is the content of the first post."
    },
    {
      "id": 2,
      "title": "Second Post",
      "content": "This is the content of the second post."
    }
  ]
}
```
#### 4.1.2 Create Blog Post
```code
POST /blog/
```

**sample command**
```bash
curl -X POST http://localhost:8080/blog/ \
-H "Content-Type: application/json" \
-d '{
  "title": "First Post",
  "content": "This is the content of the first post."
}'
```
#### 4.1.3 Retrieve Single Post
```
GET /blog/{id}/
```

#### 4.1.4 Update Blog Post
```
PUT /blog/{id}/
```

#### 4.1.5 Delete Blog Post
```
DELETE /blog/{id}/
```

### 4.2 Taxonomy & Query API (Search / Category / Tag / Archive)

> 本节 API 用于支撑：博客搜索、专栏分类页、标签页、归档页等功能。
> 推荐约定：所有列表接口默认分页（page/page_size），默认按 created_at 倒序。

#### 4.2.1 Search Posts
**Endpoint**
``GET /blog/search/?q={keyword}&page=1&page_size=10``

**Sample Command**
```bash
curl "http://localhost:8080/blog/search/?q=django&page=1&page_size=10"
```
**Response Example**
```json
{
  "query": "django",
  "page": 1,
  "page_size": 10,
  "total": 2,
  "posts": [
    {
      "id": 12,
      "title": "Django REST Framework Basics",
      "excerpt": "This post introduces DRF serialization...",
      "author": "odie",
      "created_at": "2025-12-01T10:21:12Z",
      "tags": ["django", "drf"],
      "category": "Backend"
    }
  ]
}
```
#### 4.2.2 List Categories
Endpoint
```GET /categories/```

Sample Command
```bash
curl http://localhost:8080/categories/
```
Response Example
```bash
{
  "categories": [
    { "id": 1, "name": "Backend", "slug": "backend", "post_count": 12 },
    { "id": 2, "name": "ML", "slug": "ml", "post_count": 7 }
  ]
}
```
#### 4.2.3 List Posts by Category (Category Page)
Endpoint
```GET /categories/{category_id}/posts/?page=1&page_size=10```

Sample Command
```bash
curl "http://localhost:8080/categories/1/posts/?page=1&page_size=10"
```

Response Example
```json
{
  "category": { "id": 1, "name": "Backend", "slug": "backend" },
  "page": 1,
  "page_size": 10,
  "total": 12,
  "posts": [
    {
      "id": 12,
      "title": "Django REST Framework Basics",
      "excerpt": "This post introduces DRF serialization...",
      "created_at": "2025-12-01T10:21:12Z"
    }
  ]
}
```
#### 4.2.4 List Tags
Endpoint
```GET /tags/```

#### 4.2.5 List Posts by Tag (Tag Page)
Endpoint
```GET /tags/{tag_id}/posts/?page=1&page_size=10```

Sample Command
```curl "http://localhost:8080/tags/1/posts/?page=1&page_size=10"```

Response Example
```json
{
  "tag": { "id": 1, "name": "django", "slug": "django" },
  "page": 1,
  "page_size": 10,
  "total": 9,
  "posts": [
    {
      "id": 12,
      "title": "Django REST Framework Basics",
      "excerpt": "This post introduces DRF serialization...",
      "created_at": "2025-12-01T10:21:12Z"
    }
  ]
}
```
#### 4.2.6 Archive Months (Archive Page Index)
Endpoint
```GET /archives/```
Sample Command
```bash
curl http://localhost:8080/archives/
```
Response Example
```json
{
  "archives": [
    { "year": 2025, "month": 12, "post_count": 4 },
    { "year": 2025, "month": 11, "post_count": 6 }
  ]
}
```

#### 4.2.7 List Posts by Archive Month
Endpoint
```GET /archives/{year}/{month}/posts/?page=1&page_size=10```

Sample Command
```bash
curl "http://localhost:8080/archives/2025/12/posts/?page=1&page_size=10"
```

Response Example
```json
{
  "archive": { "year": 2025, "month": 12 },
  "page": 1,
  "page_size": 10,
  "total": 4,
  "posts": [
    {
      "id": 25,
      "title": "MySQL Index Tuning Notes",
      "excerpt": "We discuss B-Tree index...",
      "created_at": "2025-12-07T09:00:00Z"
    }
  ]
}
```

### 4.3 Interaction & Auth API (Comments / Message Board / Login)
> 本节 API 用于支撑：博客评论、留言页面、登录页面（含 OAuth2）。
> 推荐约定：写操作需要鉴权（Authorization: Bearer ）。

#### 4.3.1 List Comments of a Post
Endpoint
```GET /blog/{post_id}/comments/?page=1&page_size=20```

Sample Command
```bash
curl "http://localhost:8080/blog/12/comments/?page=1&page_size=20"
```
Response Example
```json
{
  "post_id": 12,
  "page": 1,
  "page_size": 20,
  "total": 2,
  "comments": [
    {
      "id": 101,
      "author_name": "Alice",
      "content": "Nice post, very helpful!",
      "created_at": "2025-12-10T02:12:30Z"
    }
  ]
}
```
#### 4.3.2 Create Comment
Endpoint
```POST /blog/{post_id}/comments/```

Sample Command
```bash
curl -X POST "http://localhost:8080/blog/12/comments/" \
-H "Content-Type: application/json" \
-d '{
  "author_name": "Alice",
  "author_email": "alice@example.com",
  "content": "Nice post, very helpful!"
}'
```
Response Example
```json
{
  "id": 101,
  "post_id": 12,
  "author_name": "Alice",
  "content": "Nice post, very helpful!",
  "created_at": "2025-12-10T02:12:30Z"
}
```

#### 4.3.3 Delete Comment (Admin)
Endpoint
```DELETE /admin/comments/{comment_id}/```
Sample Command
```bash
curl -X DELETE "http://localhost:8080/admin/comments/101/" \
-H "Authorization: Bearer <ADMIN_TOKEN>"
```
#### 4.3.4 Message Board - List Messages
Endpoint
```GET /messages/?page=1&page_size=20```
Sample Command
```bash
curl "http://localhost:8080/messages/?page=1&page_size=20"
```
Response Example
```json
{
  "page": 1,
  "page_size": 20,
  "total": 1,
  "messages": [
    {
      "id": 1,
      "author_name": "Visitor",
      "content": "Hello! Great blog.",
      "created_at": "2025-12-10T03:00:00Z"
    }
  ]
}
```
#### 4.3.5 Message Board - Create Message
Endpoint
```POST /messages/```

Sample Command
```bash
curl -X POST "http://localhost:8080/messages/" \
-H "Content-Type: application/json" \
-d '{
  "author_name": "Visitor",
  "author_email": "visitor@example.com",
  "content": "Hello! Great blog."
}'
```

#### 4.3.6 OAuth2 Login (Google / GitHub)
> 这里给出“API 约定”，具体实现可以选 Django Allauth / Social Auth 等。

Endpoint
```GET /auth/{provider}/redirect/```

- provider: google | github
- 回第三方授权跳转链接（或直接 302 重定向）

Sample Command
```bash
curl -i "http://localhost:8080/auth/google/redirect/"
```
#### 4.3.7 OAuth2 Callback
Endpoint
```GET /auth/{provider}/callback/?code=xxx&state=yyy```

Expected Behavior
- 校验 code/state
- 换取用户信息
- 更新用户
- session 或 token

response example(token-based)
```json
{
  "access_token": "ACCESS_TOKEN",
  "token_type": "Bearer",
  "expires_in": 3600,
  "user": {
    "id": 7,
    "username": "odie",
    "email": "odie@example.com"
  }
}
```

#### 4.3.8 Logout
Endpoint
```POST /auth/logout/```

Sample Command
```bash
curl -X POST "http://localhost:8080/auth/logout/" \
-H "Authorization: Bearer <TOKEN>"
```

### 4.4 Admin Management API (Admin / Settings / Links)

> 本节 API 用于支撑：后台管理系统。
> 所有接口默认需要 **管理员权限**（Authorization: Bearer <ADMIN_TOKEN>）。

#### 4.4.1 Admin Login
**Endpoint**

POST /admin/auth/login/

**Sample Command**
```bash
curl -X POST http://localhost:8080/admin/auth/login/ \
-H "Content-Type: application/json" \
-d '{
  "username": "admin",
  "password": "admin123"
}'
```
Response Example
```json
{
  "access_token": "ADMIN_ACCESS_TOKEN",
  "token_type": "Bearer",
  "expires_in": 3600
}
```
#### 4.4.2 Admin Logout
Endpoint
```POST /admin/auth/logout/```

#### 4.4.3 Admin - List Posts
Endpoint
```GET /admin/posts/?page=1&page_size=20```

Description
- 后台文章列表
- 包含草稿 / 发布状态


#### 4.4.4 Admin - Create / Update Post
Endpoint
```
POST /admin/posts/
PUT  /admin/posts/{id}/
```

Sample Command
```bash
curl -X POST http://localhost:8080/admin/posts/ \
-H "Authorization: Bearer <ADMIN_TOKEN>" \
-H "Content-Type: application/json" \
-d '{
  "title": "Admin Created Post",
  "content_markdown": "# Hello Admin",
  "status": "published",
  "category_id": 1,
  "tag_ids": [1, 2]
}'
```
#### 4.4.5 Admin - Delete Post
Endpoint
```DELETE /admin/posts/{id}/```

#### 4.4.6 Category Management
Endpoints
```
GET    /admin/categories/
POST   /admin/categories/
PUT    /admin/categories/{id}/
DELETE /admin/categories/{id}/
```

#### 4.4.7 Tag Management
Endpoints
```
GET    /admin/tags/
POST   /admin/tags/
PUT    /admin/tags/{id}/
DELETE /admin/tags/{id}/
```

#### 4.4.8 Friend Links Management
Endpoints
```
GET    /admin/links/
POST   /admin/links/
PUT    /admin/links/{id}/
DELETE /admin/links/{id}/
```
Link Object Example
```json
{
  "name": "GitHub",
  "url": "https://github.com/odie",
  "description": "My GitHub Profile"
}
```

#### 4.4.9 System Settings
Endpoint
```
GET /admin/settings/
PUT /admin/settings/
```
Settings Example
```json
{
  "site_name": "Odie's Blog",
  "site_description": "Thoughts on CS and life",
  "comment_enabled": true,
  "maintenance_mode": false
}
```

### 4.5 File, Markdown & Statistics API
>本节 API 用于支撑：文件上传管理、Markdown 编辑器整合、数据统计。
>默认需要管理员权限。

#### 4.5.1 File Upload
Endpoint
```
POST /admin/files/upload/
```
Sample Command
```bash
curl -X POST http://localhost:8080/admin/files/upload/ \
-H "Authorization: Bearer <ADMIN_TOKEN>" \
-F "file=@image.png"
```

Response Example
```json
{
  "id": 23,
  "filename": "image.png",
  "url": "https://cdn.example.com/uploads/image.png"
}
```
#### 4.5.2 File List & Delete
Endpoints
```
GET    /admin/files/
DELETE /admin/files/{id}/
```

#### 4.5.3 Markdown Preview
Endpoint
```
POST /admin/markdown/preview/
```
Description: 用于 Markdown 编辑器实时预览

Sample Command
```bash
curl -X POST http://localhost:8080/admin/markdown/preview/ \
-H "Authorization: Bearer <ADMIN_TOKEN>" \
-H "Content-Type: application/json" \
-d '{
  "markdown": "# Hello World\nThis is a preview."
}'
```
Response Example
```json
{
  "html": "<h1>Hello World</h1><p>This is a preview.</p>"
}
```

#### 4.5.4 Statistics Overview
Endpoint
```GET /admin/stats/overview/```
Response Example
```json
{
  "total_posts": 42,
  "total_comments": 128,
  "total_messages": 15,
  "total_views": 10452
}
```

#### 4.5.5 Post View Statistics
Endpoint
```GET /admin/stats/posts/```
Response Example
```json
{
  "posts": [
    {
      "post_id": 12,
      "title": "Django REST Framework Basics",
      "views": 1532,
      "comments": 12
    }
  ]
}
```
## 5.Development Phases & Milestones

### 5.1 In-Memory Version
- 使用 In-Memory 数据存储（无数据库）
- 验证 API 设计
- 完整 curl 示例

### 5.2 Testing
- 为现有 API / Service Layer 添加测试
- Django Test Framework
- CRUD 核心路径

### 5.3 Database Layer
- 使用 MySQL
- Blog / Author / Comment 等核心模型
- DDL 用于 Review
- Migration： Post 增加 author 字段（练习迁移）

### 5.4 Frontend UI
- 前端页面通过 API 进行数据交互
- 覆盖
- 博客列表
- 博客详情
- 创建 / 编辑文章
- 登录流程

### 5.5 OAuth2 Login
- 支持 Google / GitHub OAuth2
- 提供「Login with Google / GitHub」按钮

### 5.6 Dependency Management
- 使用 Pipfile + Pipfile.lock
- 锁定依赖版本，保证环境一致性
- 参考方案 [here](`https://stackoverflow.com/questions/62440310/django-how-to-create-the-pip-and-piplock-file`)

### 5.7 Dockerization
- 构建 Docker Image
- 提供
  - ld 指令
  - Run 指令
- 支持本地 & CI 环境

### 5.8 System Design (UML)
- 系统架构图 
- 交互时序图
- 数据模型结构图（Post / Author / Comment 等）

### 5.9 Docker Compose（本地开发）
- 仅用于本地环境
- 服务包括：
  - Django App
  - MySQL
- 一键启动开发环境

### 5.10: CI/CD
- GitHub Actions
- 自动
  - Build Docker Image
  - Publish 到 Docker Hub

## 6. How to Run
### 6.1 Local Development
```bash
pipenv install
pipenv shell
python manage.py runserver
```
### 6.2 Docker
```bash
docker build -t django-blog .
docker run -p 8080:8080 django-blog
```
### 6.3 Docker Compose
```bash
docker-compose up
```
## 7. Usage Guide

- Blog API
  - curl 或 Postman 调用 API
  - 所有 API 返回 JSON
- Admin Panel
  - Django Admin 进行管理
  - 支持 Markdown 编辑

## 8. Future Improvements
- 搜索优化（全文检索）
- 缓存（Redis）
- 权限分级
- 博客访问统计
- 多主题前端支持

## 9. License
MIT License