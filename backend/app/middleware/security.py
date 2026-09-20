import time
from typing import Dict, Tuple
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.core.config import settings

# In-memory sliding-window bucket store: { client_ip: [(timestamp1), (timestamp2), ...] }
_memory_rate_limit_store: Dict[str, list] = {}


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # Strict Security Headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self' 'unsafe-inline' https:; "
            "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
            "font-src 'self' https://cdn.jsdelivr.net https://fonts.gstatic.com data:; "
            "img-src 'self' data: https:; "
            "connect-src 'self' http://localhost:8000 http://localhost:3000 https:;"
        )
        response.headers["Permissions-Policy"] = "microphone=(self), geolocation=(), camera=()"
        return response


class SlidingWindowRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 30, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    async def dispatch(self, request: Request, call_next):
        # Health check and static docs exempt from rate limiting
        if request.url.path in ["/api/health", "/docs", "/openapi.json", "/"]:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown_client"
        now = time.time()
        window_start = now - self.window_seconds

        # Sliding window filter
        timestamps = _memory_rate_limit_store.get(client_ip, [])
        # Retain only timestamps within the active sliding window
        valid_timestamps = [t for t in timestamps if t > window_start]

        if len(valid_timestamps) >= self.max_requests:
            retry_after = int(self.window_seconds - (now - valid_timestamps[0]))
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Maximum {self.max_requests} requests per {self.window_seconds}s.",
                    "retry_after_seconds": max(1, retry_after),
                    "standard": "RFC 6585",
                },
                headers={"Retry-After": str(max(1, retry_after))},
            )

        valid_timestamps.append(now)
        _memory_rate_limit_store[client_ip] = valid_timestamps

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(self.max_requests - len(valid_timestamps))
        return response
