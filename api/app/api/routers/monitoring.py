"""
Monitoring router for exposing metrics and monitoring data.
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

from app.core.monitoring import monitoring_service

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


@router.get("/metrics")
def get_metrics() -> Dict[str, Any]:
    """Get all monitoring metrics."""
    try:
        return monitoring_service.get_all_metrics()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve metrics: {str(e)}",
        )


@router.get("/metrics/search")
def get_search_metrics() -> Dict[str, Any]:
    """Get search-specific metrics."""
    try:
        return monitoring_service.get_search_metrics()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve search metrics: {str(e)}",
        )


@router.get("/metrics/sort")
def get_sort_metrics() -> Dict[str, Any]:
    """Get sort-specific metrics."""
    try:
        return monitoring_service.get_sort_metrics()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve sort metrics: {str(e)}",
        )


@router.get("/health")
def get_monitoring_health() -> Dict[str, Any]:
    """Get monitoring service health status."""
    try:
        metrics = monitoring_service.get_all_metrics()
        return {
            "status": "healthy",
            "message": "Monitoring service is operational",
            "metrics_available": bool(metrics),
            "timestamp": metrics.get("timestamp"),
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"Monitoring service error: {str(e)}",
            "metrics_available": False,
            "timestamp": None,
        }
