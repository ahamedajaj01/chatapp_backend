# Chat App Backend

This is a simple backend for a chat application built using FastAPI, PostgreSQL, and WebSockets.

---

## What this project does

- Users can signup and login
- JWT authentication is used
- Roles are supported (admin / user)
- Real-time chat using WebSockets
- Messages are saved in database
- Multiple chat rooms supported

---

## Tech used

- FastAPI
- PostgreSQL
- SQLAlchemy
- WebSockets
- JWT (python-jose)
- passlib (for password hashing)

---

## Setup

### 1. Clone project

```bash
git clone https://github.com/ahamedajaj01/chatapp_backend.git
cd chatapp_backend
```
### 2. Set up virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # for Windows
```
### 3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

### 4. Create the Database
   Make sure PostgreSQL is running and create a new database:
   ```sql
   CREATE DATABASE chatdb;
   ```
### 5. Create .env file
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/chatdb
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```
### 6. Run the application
Start the server using Uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```

### The API documentation will be available at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### API Endpoints

### Authentication
- `POST /auth/signup`: Create a new user account.
payload example:
```json
{
  "username": "test",
  "email": "test@gmail.com",
  "password": "123456",
  "role": "user" or "admin" # Defaults to user if not provided
}
```
- `POST /auth/login`: Authenticate and receive a JWT token.
payload example:
```json
{
  "email": "test@gmail.com",
  "password": "123456"
}
``` 
### Rooms & Messages
- `POST /rooms/`: Create a new chat room (Protected).
payload example:
```json
{
  "name": "General",
  "description": "General chat room"
}
```
- `GET /rooms/{room_id}/messages`: Fetch paginated message history (Protected, Cursor-based).

### WebSocket
- `WS /ws/{room_id}?token=JWT_TOKEN`: Establish a real-time chat connection.

## Quick Testing Tool
I have included a `test_websocket.html` file in the root directory to manually test the WebSocket functionality. It allows you to connect to a chat room and send messages in real-time.
1. Open `test_websocket.html` in your browser.
2. Login via Swagger/Postman to get a JWT token.
3. Paste the token and Room ID into the tool and click Connect button.
4. You can open multiple tabs to test real-time messaging between users.


### Admin (RBAC Demo)
- `GET /admin/protected`: An endpoint accessible only to users with the `admin` role.

## Data Model

- **User**: Stores user profile and credentials.
- **Room**: Represents chat rooms.
- **Message**: Stores chat messages with associations to User and Room.