"""
Health Monitor Tool

Real-time platform health monitoring with AI-powered anomaly detection.
Monitors API health, response times, error rates, and rate limits.
"""

from langchain_openai import ChatOpenAI
from typing import Dict, List
import asyncio
import aiohttp
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="../../../.env")


class HealthMonitorTool:
    """
    Tool for monitoring platform API health

    Features:
    - Response time monitoring
    - Error rate tracking
    - Rate limit monitoring
    - AI-powered anomaly detection
    - Severity classification (critical/warning/info)
    """

    def __init__(self):
        """Initialize health monitor with OpenAI LLM"""
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3,  # Lower temperature for analytical tasks
            max_tokens=400,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # Baseline health metrics (normal operating ranges)
        self.baselines = {
            "twitter": {
                "response_time": 250,  # ms
                "error_rate": 0.5,      # %
                "description": "Twitter API v2"
            },
            "linkedin": {
                "response_time": 300,
                "error_rate": 0.8,
                "description": "LinkedIn API"
            },
            "instagram": {
                "response_time": 400,
                "error_rate": 1.0,
                "description": "Instagram Graph API"
            },
            "facebook": {
                "response_time": 350,
                "error_rate": 1.0,
                "description": "Facebook Graph API"
            }
        }

    async def check_platform_health(self, platform: str) -> Dict:
        """
        Check health of a single platform

        Args:
            platform: Platform name (twitter, linkedin, instagram, facebook)

        Returns:
            {
                "platform": str,
                "status": "healthy" | "degraded" | "down",
                "response_time": float (ms),
                "error_rate": float (%),
                "rate_limit_used": int,
                "rate_limit_total": int,
                "last_check": str (ISO timestamp),
                "details": str
            }
        """

        start_time = datetime.now()

        try:
            # Mock health check for now
            # In production, replace with actual platform API health endpoints

            # Simulate different health scenarios for demo
            mock_scenarios = {
                "twitter": {"status": 200, "delay": 0.25},
                "linkedin": {"status": 200, "delay": 0.30},
                "instagram": {"status": 200, "delay": 0.40},
                "facebook": {"status": 200, "delay": 0.35}
            }

            scenario = mock_scenarios.get(platform, {"status": 200, "delay": 0.3})

            # Simulate API call with delay
            await asyncio.sleep(scenario["delay"])

            response_time = (datetime.now() - start_time).total_seconds() * 1000

            # Determine status based on response
            if scenario["status"] == 200:
                status = "healthy"
                error_rate = 0.0
            elif scenario["status"] >= 500:
                status = "down"
                error_rate = 100.0
            else:
                status = "degraded"
                error_rate = 5.0

            # Mock rate limit data
            rate_limit_data = {
                "twitter": (450, 1000),
                "linkedin": (80, 100),
                "instagram": (150, 200),
                "facebook": (180, 200)
            }

            rate_used, rate_total = rate_limit_data.get(platform, (0, 1000))

            health_data = {
                "platform": platform,
                "status": status,
                "response_time": round(response_time, 2),
                "error_rate": error_rate,
                "rate_limit_used": rate_used,
                "rate_limit_total": rate_total,
                "last_check": datetime.now().isoformat(),
                "details": f"{self.baselines[platform]['description']} is responding normally"
            }

            return health_data

        except asyncio.TimeoutError:
            return {
                "platform": platform,
                "status": "down",
                "response_time": 5000,  # Timeout
                "error_rate": 100,
                "rate_limit_used": 0,
                "rate_limit_total": 1000,
                "last_check": datetime.now().isoformat(),
                "details": "Request timed out after 5 seconds"
            }

        except Exception as e:
            return {
                "platform": platform,
                "status": "down",
                "response_time": 0,
                "error_rate": 100,
                "rate_limit_used": 0,
                "rate_limit_total": 1000,
                "last_check": datetime.now().isoformat(),
                "details": f"Error: {str(e)}"
            }

    async def analyze_health(self, health_data: Dict) -> Dict:
        """
        AI analyzes health data and determines if alerting is needed

        Args:
            health_data: Health metrics from check_platform_health()

        Returns:
            {
                "should_alert": bool,
                "severity": "critical" | "warning" | "info",
                "message": str (user-friendly),
                "recommended_action": str,
                "issue_detected": bool
            }
        """

        platform = health_data["platform"]
        baseline = self.baselines.get(platform, {})

        # Calculate deviations from baseline
        response_time = health_data.get("response_time", 0)
        baseline_rt = baseline.get("response_time", 300)
        error_rate = health_data.get("error_rate", 0)
        status = health_data.get("status", "unknown")
        rate_used = health_data.get("rate_limit_used", 0)
        rate_total = health_data.get("rate_limit_total", 1000)
        rate_percentage = (rate_used / rate_total * 100) if rate_total > 0 else 0

        # Create AI analysis prompt
        prompt = f"""Analyze {platform} API health and determine if users need an alert:

Current Status:
- Status: {status}
- Response time: {response_time}ms (baseline: {baseline_rt}ms)
- Error rate: {error_rate}%
- Rate limit: {rate_used}/{rate_total} ({rate_percentage:.1f}% used)

Determine:
1. Is there an actionable issue? (yes/no)
2. Severity level:
   - "critical": Platform down, auth failed, complete failure
   - "warning": 2-3x slower than normal, elevated errors, rate limit approaching
   - "info": Minor delays, low-priority notifications
3. User-friendly message (max 80 characters)
4. Recommended action
5. Should we send an alert? (yes/no)

Return ONLY valid JSON:
{{
    "should_alert": true,
    "severity": "warning",
    "message": "{platform.title()} API is running slow",
    "recommended_action": "Posts may be delayed but will succeed",
    "issue_detected": true
}}
"""

        try:
            response = await self.llm.ainvoke(prompt)

            # Parse response
            content = response.content.strip()
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            content = content.strip()

            analysis = json.loads(content)
            return analysis

        except Exception as e:
            print(f"AI analysis error: {e}")

            # Fallback logic based on simple rules
            if status == "down":
                return {
                    "should_alert": True,
                    "severity": "critical",
                    "message": f"{platform.title()} API is currently down",
                    "recommended_action": "Please check your connection. Posts cannot be published.",
                    "issue_detected": True
                }

            elif response_time > baseline_rt * 3:  # 3x slower
                return {
                    "should_alert": True,
                    "severity": "warning",
                    "message": f"{platform.title()} API is running slow ({response_time:.0f}ms)",
                    "recommended_action": "Posts may be delayed but will succeed",
                    "issue_detected": True
                }

            elif rate_percentage > 85:  # >85% rate limit used
                return {
                    "should_alert": True,
                    "severity": "info",
                    "message": f"{platform.title()} rate limit at {rate_percentage:.0f}%",
                    "recommended_action": "Posting may be throttled soon",
                    "issue_detected": True
                }

            else:
                return {
                    "should_alert": False,
                    "severity": "info",
                    "message": f"{platform.title()} is healthy",
                    "recommended_action": "No action needed",
                    "issue_detected": False
                }

    async def check_all_platforms(self) -> List[Dict]:
        """
        Check health of all platforms simultaneously

        Returns:
            List of health check results with analysis
        """

        platforms = ["twitter", "linkedin", "instagram", "facebook"]

        # Check all platforms in parallel
        health_checks = [
            self.check_platform_health(platform)
            for platform in platforms
        ]

        health_results = await asyncio.gather(*health_checks)

        # Analyze each result
        analyzed_results = []
        for health_data in health_results:
            analysis = await self.analyze_health(health_data)

            # Combine health data with analysis
            result = {
                **health_data,
                "analysis": analysis
            }

            analyzed_results.append(result)

        return analyzed_results


# Test the tool
if __name__ == "__main__":
    print("🧪 Testing Health Monitor Tool")
    print("=" * 60)

    async def test_monitor():
        monitor = HealthMonitorTool()

        print("\n🔍 Checking all platforms...")
        results = await monitor.check_all_platforms()

        print("\n📊 Health Check Results:")
        print("=" * 60)

        for result in results:
            platform = result["platform"]
            status = result["status"]
            response_time = result["response_time"]
            analysis = result.get("analysis", {})

            status_icon = {
                "healthy": "✅",
                "degraded": "⚠️",
                "down": "🔴"
            }.get(status, "❓")

            print(f"\n{status_icon} {platform.upper()}")
            print(f"  Status: {status}")
            print(f"  Response Time: {response_time}ms")
            print(f"  Rate Limit: {result['rate_limit_used']}/{result['rate_limit_total']}")

            if analysis.get("should_alert"):
                severity_icon = {
                    "critical": "🔴",
                    "warning": "🟡",
                    "info": "🔵"
                }.get(analysis.get("severity", "info"), "•")

                print(f"\n  {severity_icon} ALERT: {analysis.get('message', '')}")
                print(f"  Action: {analysis.get('recommended_action', '')}")

        print("\n" + "=" * 60)
        print("✅ Health check complete!")

    # Run async test
    asyncio.run(test_monitor())
