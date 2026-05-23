"""
Background scheduler for periodic live AQI data fetching.

Uses APScheduler to run the AQI fetcher every 30 minutes.
Only activates when a valid WAQI API token is configured.
"""

import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.core.config import get_settings

logger = logging.getLogger(__name__)

_scheduler: BackgroundScheduler | None = None


def start_scheduler() -> None:
    """Start the background AQI fetch scheduler."""
    global _scheduler

    settings = get_settings()
    token = settings.WAQI_API_TOKEN

    if not token or token == "demo":
        logger.info("⏭️ WAQI token not set — live AQI scheduler disabled")
        return

    if _scheduler is not None:
        logger.info("Scheduler already running")
        return

    from app.services.aqi_fetcher import fetch_all_cities

    _scheduler = BackgroundScheduler(daemon=True)
    _scheduler.add_job(
        fetch_all_cities,
        trigger=IntervalTrigger(minutes=30),
        id="live_aqi_fetch",
        name="Fetch live AQI for all cities",
        replace_existing=True,
    )
    _scheduler.start()
    logger.info("🕐 Live AQI scheduler started — fetching every 30 minutes")

    # Run immediately on startup
    fetch_all_cities()


def stop_scheduler() -> None:
    """Stop the background scheduler."""
    global _scheduler
    if _scheduler:
        _scheduler.shutdown(wait=False)
        _scheduler = None
        logger.info("🛑 Live AQI scheduler stopped")
