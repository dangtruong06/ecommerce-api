## Structure & Design

### 1. Split endpoints into routers
Group related API endpoints into separate routers.

Example:
`routers/users.py`
`routers/expenses.py`

This keeps `main.py` small and makes the API easier to navigate.

### 2. Move operations out of endpoints
Use a layered structure:

Router → Service → Database

Routes handle HTTP requests, while services contain business logic.
This makes logic easier to test and reuse.

### 3. Design for deployment
Set up project scaffolding early:

app/
├── main.py
├── routers/
├── services/
├── models/
├── tests/
└── Dockerfile

Use environment variables for things like database URLs and secrets.

### 4. Control access
Protect endpoints with authentication, authorization, and rate limiting.

Request → Auth → Rate Limit → Router → Service

### 5. Write tests
Test both successful requests and failure cases.

Example:
- Creating an expense → `201`
- Missing authentication → `401`
- Invalid input → `400`
- Accessing another user's expense → `403`
