"""
Timezone utilities for the application.
"""

from datetime import datetime, timezone
from typing import Optional
import pytz
from .config import settings


def get_current_timezone() -> timezone:
    """Get the current timezone based on configuration."""
    if settings.USE_TIMEZONE:
        try:
            return pytz.timezone(settings.TIMEZONE)
        except pytz.exceptions.UnknownTimeZoneError:
            # Fallback to UTC if timezone is invalid
            return timezone.utc
    return timezone.utc


def now() -> datetime:
    """Get current datetime with proper timezone."""
    if settings.USE_TIMEZONE:
        tz = get_current_timezone()
        return datetime.now(tz)
    return datetime.now(timezone.utc)


def utcnow() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


def make_timezone_aware(dt: datetime, tz: Optional[timezone] = None) -> datetime:
    """Make a datetime timezone-aware."""
    if dt.tzinfo is None:
        if tz is None:
            tz = get_current_timezone()
        return dt.replace(tzinfo=tz)
    return dt


def convert_timezone(dt: datetime, target_tz: timezone) -> datetime:
    """Convert datetime to target timezone."""
    if dt.tzinfo is None:
        # If naive datetime, assume it's in UTC
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(target_tz)
