"""
Middleware for request monitoring and logging.
"""

import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.core.monitoring import monitoring_service

logger = logging.getLogger(__name__)


class MonitoringMiddleware(BaseHTTPMiddleware):
    """Middleware for monitoring API requests and responses."""

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.logger = logging.getLogger(__name__)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process the request and log monitoring information."""
        start_time = time.time()

        # Extract client information
        client_ip = self._get_client_ip(request)
        user_agent = request.headers.get("user-agent", "")

        try:
            # Process the request
            response = await call_next(request)

            # Calculate execution time
            execution_time = (
                time.time() - start_time
            ) * 1000  # Convert to milliseconds

            # Log the API request
            monitoring_service.log_api_request(
                method=request.method,
                path=str(request.url.path),
                status_code=response.status_code,
                execution_time_ms=execution_time,
                user_agent=user_agent,
                client_ip=client_ip,
            )

            # Add custom headers for monitoring
            response.headers["X-Execution-Time"] = f"{execution_time:.2f}ms"
            response.headers["X-Request-ID"] = self._generate_request_id()

            return response

        except Exception as e:
            # Calculate execution time for failed requests
            execution_time = (time.time() - start_time) * 1000

            # Log the error
            monitoring_service.log_error(
                error=e,
                context={
                    "method": request.method,
                    "path": str(request.url.path),
                    "client_ip": client_ip,
                    "user_agent": user_agent,
                    "execution_time_ms": execution_time,
                },
            )

            # Re-raise the exception
            raise

    def _get_client_ip(self, request: Request) -> str:
        """Extract the real client IP address."""
        # Check for forwarded headers (common in proxy setups)
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip

        # Fallback to the direct client IP
        return request.client.host if request.client else "unknown"

    def _generate_request_id(self) -> str:
        """Generate a unique request ID."""
        import uuid

        return str(uuid.uuid4())


class RequestTimingMiddleware(BaseHTTPMiddleware):
    """Simple middleware for timing requests."""

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.logger = logging.getLogger(__name__)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Add timing information to requests."""
        start_time = time.time()

        response = await call_next(request)

        execution_time = (time.time() - start_time) * 1000

        # Log slow requests (over 1 second)
        if execution_time > 1000:
            self.logger.warning(
                f"Slow request detected: {request.method} {request.url.path} "
                f"took {execution_time:.2f}ms"
            )

        # Add timing header
        response.headers["X-Request-Time"] = f"{execution_time:.2f}ms"

        return response
