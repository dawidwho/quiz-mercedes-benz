import httpx
from typing import Dict, Any
from sqlalchemy import text
from app.db.session import SessionLocal


async def check_basic_health() -> Dict[str, Any]:
    """Basic health check without external dependencies"""
    return {"status": "healthy", "message": "Application is running"}


async def check_postgresql_health() -> Dict[str, Any]:
    """Check PostgreSQL database connection health"""
    try:
        db = SessionLocal()
        # Execute a simple query to test the connection
        result = db.execute(text("SELECT 1"))
        result.fetchone()
        db.close()
        return {"status": "connected"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def check_star_wars_api_health(api_url: str) -> Dict[str, Any]:
    """Check Star Wars API health by making a request to the specified endpoint"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{api_url}people/?page=3&nrp=2", timeout=10.0)
            if response.status_code == 200:
                return {"status": "connected"}
            else:
                return {"status": "error", "message": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def get_health_status(
    app_name: str, app_version: str, star_wars_api_url: str
) -> Dict[str, Any]:
    """Get comprehensive health status for all services"""
    health_status = {
        "status": "healthy",
        "app_name": app_name,
        "version": app_version,
        "services": {},
    }

    # Check PostgreSQL database connection
    postgresql_health = await check_postgresql_health()
    health_status["services"]["postgresql"] = postgresql_health
    if postgresql_health["status"] != "connected":
        health_status["status"] = "unhealthy"

    # Check Star Wars API
    star_wars_health = await check_star_wars_api_health(star_wars_api_url)
    health_status["services"]["star_wars_api"] = star_wars_health
    if star_wars_health["status"] != "connected":
        health_status["status"] = "unhealthy"

    return health_status
