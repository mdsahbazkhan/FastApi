from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


app = FastAPI()

# Limiter Setup
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."},
    )
    

# Rate-limited endpoint 

@app.get("/data")
@limiter.limit("5/minute")  # Limit to 5 requests per minute
def get_data(request: Request):
    return {"message": "This is some data."}