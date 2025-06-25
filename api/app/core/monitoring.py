"""
Monitoring and logging utilities for tracking search and sort events.
"""

import logging
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
from .timezone import now

logger = logging.getLogger(__name__)


class EventType(Enum):
    """Types of events that can be monitored."""

    SEARCH = "search"
    SORT = "sort"
    API_REQUEST = "api_request"
    ERROR = "error"


@dataclass
class SearchEvent:
    """Data structure for search events."""

    event_type: str = EventType.SEARCH.value
    timestamp: str = None
    endpoint: str = None
    resource_type: str = None  # "people" or "planets"
    search_params: Dict[str, str] = None
    results_count: int = None
    total_count: int = None
    page: int = None
    size: int = None
    execution_time_ms: float = None
    user_agent: str = None
    client_ip: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = now().isoformat()


@dataclass
class SortEvent:
    """Data structure for sort events."""

    event_type: str = EventType.SORT.value
    timestamp: str = None
    endpoint: str = None
    resource_type: str = None  # "people" or "planets"
    sort_field: str = None
    sort_order: str = None
    results_count: int = None
    total_count: int = None
    page: int = None
    size: int = None
    execution_time_ms: float = None
    user_agent: str = None
    client_ip: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = now().isoformat()


class MonitoringService:
    """Service for monitoring and logging application events."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._search_metrics = {
            "total_searches": 0,
            "searches_by_resource": {"people": 0, "planets": 0},
            "popular_search_terms": {},
            "average_execution_time": 0.0,
        }
        self._sort_metrics = {
            "total_sorts": 0,
            "sorts_by_resource": {"people": 0, "planets": 0},
            "popular_sort_fields": {},
            "sort_order_distribution": {"asc": 0, "desc": 0},
            "average_execution_time": 0.0,
        }

    def log_search_event(self, event: SearchEvent):
        """Log a search event with structured data."""
        try:
            # Update metrics
            self._search_metrics["total_searches"] += 1
            if event.resource_type:
                self._search_metrics["searches_by_resource"][event.resource_type] += 1

            # Track popular search terms
            if event.search_params:
                for field, value in event.search_params.items():
                    term_key = f"{field}:{value.lower()}"
                    self._search_metrics["popular_search_terms"][term_key] = (
                        self._search_metrics["popular_search_terms"].get(term_key, 0)
                        + 1
                    )

            # Update average execution time
            if event.execution_time_ms:
                current_avg = self._search_metrics["average_execution_time"]
                total_searches = self._search_metrics["total_searches"]
                self._search_metrics["average_execution_time"] = (
                    current_avg * (total_searches - 1) + event.execution_time_ms
                ) / total_searches

            # Log the event
            self.logger.info(
                "Search event",
                extra={
                    "event_type": "search",
                    "event_data": asdict(event),
                    "metrics": self._search_metrics,
                },
            )

        except Exception as e:
            self.logger.error(f"Error logging search event: {e}")

    def log_sort_event(self, event: SortEvent):
        """Log a sort event with structured data."""
        try:
            # Update metrics
            self._sort_metrics["total_sorts"] += 1
            if event.resource_type:
                self._sort_metrics["sorts_by_resource"][event.resource_type] += 1

            # Track popular sort fields
            if event.sort_field:
                self._sort_metrics["popular_sort_fields"][event.sort_field] = (
                    self._sort_metrics["popular_sort_fields"].get(event.sort_field, 0)
                    + 1
                )

            # Track sort order distribution
            if event.sort_order:
                self._sort_metrics["sort_order_distribution"][event.sort_order] += 1

            # Update average execution time
            if event.execution_time_ms:
                current_avg = self._sort_metrics["average_execution_time"]
                total_sorts = self._sort_metrics["total_sorts"]
                self._sort_metrics["average_execution_time"] = (
                    current_avg * (total_sorts - 1) + event.execution_time_ms
                ) / total_sorts

            # Log the event
            self.logger.info(
                "Sort event",
                extra={
                    "event_type": "sort",
                    "event_data": asdict(event),
                    "metrics": self._sort_metrics,
                },
            )

        except Exception as e:
            self.logger.error(f"Error logging sort event: {e}")

    def log_api_request(
        self,
        method: str,
        path: str,
        status_code: int,
        execution_time_ms: float,
        user_agent: str = None,
        client_ip: str = None,
    ):
        """Log API request events."""
        try:
            event_data = {
                "event_type": EventType.API_REQUEST.value,
                "timestamp": now().isoformat(),
                "method": method,
                "path": path,
                "status_code": status_code,
                "execution_time_ms": execution_time_ms,
                "user_agent": user_agent,
                "client_ip": client_ip,
            }

            self.logger.info(
                "API request",
                extra={"event_type": "api_request", "event_data": event_data},
            )

        except Exception as e:
            self.logger.error(f"Error logging API request: {e}")

    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        """Log error events."""
        try:
            event_data = {
                "event_type": EventType.ERROR.value,
                "timestamp": now().isoformat(),
                "error_type": type(error).__name__,
                "error_message": str(error),
                "context": context or {},
            }

            self.logger.error(
                "Application error",
                extra={"event_type": "error", "event_data": event_data},
                exc_info=True,
            )

        except Exception as e:
            self.logger.error(f"Error logging error event: {e}")

    def get_search_metrics(self) -> Dict[str, Any]:
        """Get current search metrics."""
        return self._search_metrics.copy()

    def get_sort_metrics(self) -> Dict[str, Any]:
        """Get current sort metrics."""
        return self._sort_metrics.copy()

    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all monitoring metrics."""
        return {
            "search_metrics": self.get_search_metrics(),
            "sort_metrics": self.get_sort_metrics(),
            "timestamp": now().isoformat(),
        }


# Global monitoring service instance
monitoring_service = MonitoringService()


def log_search_operation(
    resource_type: str,
    search_params: Dict[str, str],
    results_count: int,
    total_count: int,
    page: int,
    size: int,
    execution_time_ms: float,
    endpoint: str = None,
    user_agent: str = None,
    client_ip: str = None,
):
    """Convenience function to log search operations."""
    event = SearchEvent(
        endpoint=endpoint,
        resource_type=resource_type,
        search_params=search_params,
        results_count=results_count,
        total_count=total_count,
        page=page,
        size=size,
        execution_time_ms=execution_time_ms,
        user_agent=user_agent,
        client_ip=client_ip,
    )
    monitoring_service.log_search_event(event)


def log_sort_operation(
    resource_type: str,
    sort_field: str,
    sort_order: str,
    results_count: int,
    total_count: int,
    page: int,
    size: int,
    execution_time_ms: float,
    endpoint: str = None,
    user_agent: str = None,
    client_ip: str = None,
):
    """Convenience function to log sort operations."""
    event = SortEvent(
        endpoint=endpoint,
        resource_type=resource_type,
        sort_field=sort_field,
        sort_order=sort_order,
        results_count=results_count,
        total_count=total_count,
        page=page,
        size=size,
        execution_time_ms=execution_time_ms,
        user_agent=user_agent,
        client_ip=client_ip,
    )
    monitoring_service.log_sort_event(event)
