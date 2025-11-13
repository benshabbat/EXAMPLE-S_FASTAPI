# מדריך Middleware ב-FastAPI

## מהו Middleware?

Middleware הוא פונקציה שרצה לפני ואחרי כל request. הוא מאפשר לבצע פעולות כמו:
- לוגינג של בקשות
- אימות והרשאות
- מדידת זמן ביצוע
- הוספת headers
- טיפול בשגיאות
- CORS

## סוגי Middleware

### 1. Middleware Function (הפשוט ביותר)

```python
from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### 2. Class-Based Middleware

```python
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

app = FastAPI()
app.add_middleware(TimingMiddleware)
```

## דוגמאות שימושיות

### Logging Middleware

```python
from fastapi import FastAPI, Request
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response
```

### Authentication Middleware

```python
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # בדוק אם יש token בheader
        token = request.headers.get("Authorization")
        
        # נתיבים שלא דורשים אימות
        public_paths = ["/", "/docs", "/openapi.json"]
        
        if request.url.path not in public_paths:
            if not token:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Missing authentication token"}
                )
            
            if not token.startswith("Bearer "):
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid authentication scheme"}
                )
        
        response = await call_next(request)
        return response

app = FastAPI()
app.add_middleware(AuthMiddleware)
```

### CORS Middleware

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Rate Limiting Middleware

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import time
from collections import defaultdict

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        
        # נקה בקשות ישנות (מעל דקה)
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if current_time - req_time < 60
        ]
        
        # בדוק אם עבר את המגבלה
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests"}
            )
        
        self.requests[client_ip].append(current_time)
        response = await call_next(request)
        return response

app = FastAPI()
app.add_middleware(RateLimitMiddleware, requests_per_minute=100)
```

### Error Handling Middleware

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"}
            )

app = FastAPI()
app.add_middleware(ErrorHandlerMiddleware)
```

### Request ID Middleware

```python
from fastapi import FastAPI, Request
import uuid

app = FastAPI()

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
```

## דוגמה מלאה עם כמה Middlewares

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# 1. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Timing Middleware
@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    return response

# 3. Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"→ {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"← {response.status_code}")
    return response

# Routes
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/slow")
async def slow_endpoint():
    time.sleep(2)
    return {"message": "This was slow"}
```

## סדר הרצת Middlewares

⚠️ **חשוב:** Middlewares רצים בסדר **הפוך** לסדר ההוספה!

```python
app.add_middleware(Middleware1)  # רץ שלישי
app.add_middleware(Middleware2)  # רץ שני
app.add_middleware(Middleware3)  # רץ ראשון
```

## גישה למידע מה-Request

```python
@app.middleware("http")
async def example_middleware(request: Request, call_next):
    # גישה לנתוני הrequest
    method = request.method
    url = request.url
    headers = request.headers
    client = request.client.host
    
    # שמירת מידע ב-state
    request.state.user_id = "12345"
    
    response = await call_next(request)
    return response
```

## שימוש ב-Request State בroutes

```python
from fastapi import FastAPI, Request

@app.get("/profile")
async def get_profile(request: Request):
    user_id = request.state.user_id
    return {"user_id": user_id}
```

## טיפים חשובים

1. **ביצועים:** Middleware רץ על כל request - שמור על קוד יעיל
2. **סדר:** שים לב לסדר הוספת ה-middlewares
3. **Exceptions:** תפוס exceptions כדי למנוע קריסות
4. **Async:** השתמש ב-async/await לביצועים טובים יותר
5. **Testing:** בדוק middlewares בנפרד עם unit tests

## הרצה

```bash
# התקנת dependencies
pip install fastapi uvicorn

# הרצת השרת
uvicorn main:app --reload
```

## בדיקה

```bash
# בדיקת timing middleware
curl -i http://localhost:8000/

# תראה בheaders:
# X-Process-Time: 0.0023
```
