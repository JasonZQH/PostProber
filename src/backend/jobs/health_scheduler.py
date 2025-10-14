"""
Health Monitoring Background Scheduler

Runs periodic health checks and broadcasts alerts via WebSocket.
Uses APScheduler for job management.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import logging
import asyncio
from typing import Dict, List

from tools.health_monitor import HealthMonitorTool
from services.websocket_manager import manager as ws_manager

logger = logging.getLogger(__name__)


class HealthScheduler:
    """
    Background scheduler for health monitoring

    Features:
    - Periodic health checks (every 5 minutes)
    - AI-powered anomaly detection
    - Real-time WebSocket alerts
    - Alert deduplication
    - Graceful start/stop
    """

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.health_monitor = HealthMonitorTool()

        # Track last alert state to avoid duplicate alerts
        self.last_alert_state: Dict[str, str] = {}  # platform -> severity

        # Track when we last sent alerts for each platform
        self.last_alert_time: Dict[str, datetime] = {}

        # Minimum time between identical alerts (minutes)
        self.alert_cooldown = 15

        # Store last health check results
        self.last_health_check: List[Dict] = []

    async def check_health_and_alert(self):
        """
        Perform health check and send alerts if needed

        This runs periodically (default: every 5 minutes)
        """
        try:
            logger.info("🔍 Running scheduled health check...")

            # Check all platforms
            results = await self.health_monitor.check_all_platforms()

            # Store results
            self.last_health_check = results

            # Broadcast health update to all clients
            await ws_manager.broadcast_health_update(results)

            # Check each platform for alerts
            for result in results:
                await self._process_platform_alert(result)

            logger.info(f"✅ Health check complete. Checked {len(results)} platforms.")

        except Exception as e:
            logger.error(f"❌ Error in health check: {e}")

    async def _process_platform_alert(self, result: Dict):
        """
        Process a single platform's health result and send alert if needed

        Args:
            result: Health check result with analysis
        """
        platform = result["platform"]
        analysis = result.get("analysis", {})

        should_alert = analysis.get("should_alert", False)
        severity = analysis.get("severity", "info")

        if not should_alert:
            # No alert needed - clear previous state
            self.last_alert_state.pop(platform, None)
            return

        # Check if we should send this alert
        if self._should_send_alert(platform, severity):
            # Create alert object
            alert = {
                "platform": platform,
                "severity": severity,
                "message": analysis.get("message", ""),
                "recommended_action": analysis.get("recommended_action", ""),
                "status": result.get("status", "unknown"),
                "response_time": result.get("response_time", 0),
                "error_rate": result.get("error_rate", 0),
                "rate_limit_used": result.get("rate_limit_used", 0),
                "rate_limit_total": result.get("rate_limit_total", 1000),
                "timestamp": datetime.now().isoformat()
            }

            # Broadcast alert
            await ws_manager.broadcast_health_alert(alert)

            # Update state
            self.last_alert_state[platform] = severity
            self.last_alert_time[platform] = datetime.now()

            logger.warning(f"🚨 Alert sent for {platform}: {severity.upper()} - {alert['message']}")

    def _should_send_alert(self, platform: str, severity: str) -> bool:
        """
        Determine if we should send an alert based on deduplication rules

        Args:
            platform: Platform name
            severity: Alert severity

        Returns:
            True if alert should be sent, False otherwise
        """
        # Always send critical alerts
        if severity == "critical":
            return True

        # Check if state changed
        last_severity = self.last_alert_state.get(platform)

        if last_severity != severity:
            # State changed - send alert
            return True

        # Same state - check cooldown period
        last_alert = self.last_alert_time.get(platform)

        if last_alert is None:
            # First alert - send it
            return True

        # Check if cooldown period has passed
        minutes_since_last = (datetime.now() - last_alert).total_seconds() / 60

        if minutes_since_last >= self.alert_cooldown:
            # Cooldown passed - send reminder
            return True

        # Still in cooldown - don't send
        return False

    def get_last_results(self) -> List[Dict]:
        """
        Get the last health check results

        Returns:
            List of health check results
        """
        return self.last_health_check

    def start(self):
        """
        Start the health monitoring scheduler
        """
        if self.scheduler.running:
            logger.warning("Scheduler is already running")
            return

        # Add health check job (every 5 minutes)
        self.scheduler.add_job(
            self.check_health_and_alert,
            trigger=IntervalTrigger(minutes=5),
            id="health_check",
            name="Platform Health Check",
            replace_existing=True
        )

        # Start scheduler
        self.scheduler.start()

        logger.info("✅ Health monitoring scheduler started")
        logger.info("📅 Health checks will run every 5 minutes")

    async def start_async(self):
        """
        Start the scheduler and run initial health check
        """
        self.start()

        # Run initial health check immediately
        logger.info("🚀 Running initial health check...")
        await self.check_health_and_alert()

    def stop(self):
        """
        Stop the health monitoring scheduler
        """
        if not self.scheduler.running:
            logger.warning("Scheduler is not running")
            return

        self.scheduler.shutdown(wait=True)
        logger.info("⏹️ Health monitoring scheduler stopped")

    def get_job_status(self) -> Dict:
        """
        Get status of scheduled jobs

        Returns:
            Job status dictionary
        """
        jobs = self.scheduler.get_jobs()

        return {
            "running": self.scheduler.running,
            "jobs": [
                {
                    "id": job.id,
                    "name": job.name,
                    "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
                    "trigger": str(job.trigger)
                }
                for job in jobs
            ]
        }


# Global instance
health_scheduler = HealthScheduler()


# Helper functions for FastAPI lifecycle
async def start_health_monitoring():
    """
    Start health monitoring on application startup
    """
    logger.info("🚀 Starting health monitoring system...")
    await health_scheduler.start_async()


def stop_health_monitoring():
    """
    Stop health monitoring on application shutdown
    """
    logger.info("⏹️ Stopping health monitoring system...")
    health_scheduler.stop()


# Test the scheduler
if __name__ == "__main__":
    print("🧪 Testing Health Scheduler")
    print("=" * 60)

    async def test_scheduler():
        scheduler = HealthScheduler()

        print("\n🚀 Starting scheduler...")
        await scheduler.start_async()

        print("\n📊 Job Status:")
        status = scheduler.get_job_status()
        print(f"Running: {status['running']}")
        for job in status['jobs']:
            print(f"  - {job['name']} (ID: {job['id']})")
            print(f"    Next run: {job['next_run']}")
            print(f"    Trigger: {job['trigger']}")

        print("\n⏳ Waiting 10 seconds...")
        await asyncio.sleep(10)

        print("\n📋 Last Health Check Results:")
        results = scheduler.get_last_results()
        for result in results:
            platform = result['platform']
            status_val = result['status']
            response_time = result['response_time']

            status_icon = {
                "healthy": "✅",
                "degraded": "⚠️",
                "down": "🔴"
            }.get(status_val, "❓")

            print(f"  {status_icon} {platform.upper()}: {status_val} ({response_time}ms)")

        print("\n⏹️ Stopping scheduler...")
        scheduler.stop()

        print("\n✅ Test complete!")

    # Run test
    asyncio.run(test_scheduler())
