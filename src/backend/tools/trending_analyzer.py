"""
Trending Content Analyzer Tool

Analyzes trending content patterns across social media platforms.
Provides insights on what's working NOW in the market.
"""

from langchain_openai import ChatOpenAI
from typing import Dict, List
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="../../../.env")


class TrendingAnalyzerTool:
    """
    Tool for analyzing trending content patterns

    Features:
    - Fetch trending topics (mocked for now, ready for real API integration)
    - AI-powered pattern analysis
    - Category classification (tech, business, lifestyle, etc.)
    - Engagement metrics analysis
    - Content format recommendations
    """

    def __init__(self):
        """Initialize trending analyzer with OpenAI LLM"""
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.4,  # Balanced for analytical + creative
            max_tokens=800,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # Mock trending data (in production, fetch from platform APIs)
        self.trending_categories = [
            "technology", "business", "marketing", "lifestyle",
            "health", "finance", "education", "entertainment"
        ]

    async def fetch_trending_content(self, platform: str, category: str = None) -> List[Dict]:
        """
        Fetch trending content for a platform

        In production, this would call platform APIs:
        - Twitter: GET /2/tweets/search/recent with "sort_order=relevancy"
        - LinkedIn: LinkedIn API trending posts
        - Instagram: Instagram Graph API trending hashtags

        Args:
            platform: Platform name (twitter, linkedin, instagram, facebook)
            category: Optional category filter

        Returns:
            List of trending posts with metadata
        """

        # Mock trending content (replace with real API calls)
        mock_trending = {
            "twitter": [
                {
                    "id": "1",
                    "content": "Just launched our new AI feature! 🚀 It's changing how we work. #AI #Tech",
                    "author": "@techstartup",
                    "engagement": {
                        "likes": 1250,
                        "retweets": 340,
                        "comments": 89,
                        "engagement_rate": 8.5
                    },
                    "posted_at": "2025-10-13T08:30:00",
                    "category": "technology"
                },
                {
                    "id": "2",
                    "content": "5 lessons learned from building a $10M business:\n1. Start before you're ready\n2. Focus on solving real problems\n3. Build in public\n4. Listen to customers\n5. Stay consistent\n\nWhat would you add? 💼",
                    "author": "@businessguru",
                    "engagement": {
                        "likes": 2800,
                        "retweets": 890,
                        "comments": 234,
                        "engagement_rate": 12.3
                    },
                    "posted_at": "2025-10-13T09:15:00",
                    "category": "business"
                },
                {
                    "id": "3",
                    "content": "Content marketing in 2025:\n\n✅ Short-form video\n✅ AI-powered personalization\n✅ Interactive content\n✅ Community building\n\nWhat's working for you? #Marketing",
                    "author": "@marketingpro",
                    "engagement": {
                        "likes": 1890,
                        "retweets": 567,
                        "comments": 145,
                        "engagement_rate": 10.2
                    },
                    "posted_at": "2025-10-13T10:00:00",
                    "category": "marketing"
                }
            ],
            "linkedin": [
                {
                    "id": "4",
                    "content": "Excited to share that we've just closed our Series A! 🎉\n\nKey learnings from our fundraising journey:\n\n→ Build relationships before you need them\n→ Focus on metrics that matter\n→ Tell a compelling story\n→ Be prepared for 'no' (and learn from it)\n\nHappy to connect with other founders going through this!",
                    "author": "Sarah Chen",
                    "engagement": {
                        "likes": 3200,
                        "comments": 189,
                        "shares": 234,
                        "engagement_rate": 15.6
                    },
                    "posted_at": "2025-10-13T07:45:00",
                    "category": "business"
                },
                {
                    "id": "5",
                    "content": "AI is not replacing jobs. It's replacing tasks.\n\nThe real question is: Are you learning to work WITH AI, or competing AGAINST it?\n\nHere's what I've learned after implementing AI in our workflow...\n\n[Thread continues with insights]",
                    "author": "Mike Johnson",
                    "engagement": {
                        "likes": 4500,
                        "comments": 312,
                        "shares": 890,
                        "engagement_rate": 18.9
                    },
                    "posted_at": "2025-10-13T08:00:00",
                    "category": "technology"
                }
            ]
        }

        trending_posts = mock_trending.get(platform, [])

        # Filter by category if specified
        if category:
            trending_posts = [p for p in trending_posts if p["category"] == category]

        return trending_posts

    async def analyze_trending_patterns(self, platform: str, category: str = None) -> Dict:
        """
        Analyze trending content patterns using AI

        Args:
            platform: Platform name
            category: Optional category filter

        Returns:
            {
                "platform": str,
                "category": str,
                "patterns": [
                    {
                        "pattern": str,
                        "examples": [str],
                        "why_it_works": str,
                        "confidence": float
                    }
                ],
                "top_formats": [str],
                "top_topics": [str],
                "engagement_drivers": [str],
                "content_length": {
                    "optimal_min": int,
                    "optimal_max": int,
                    "average": int
                },
                "posting_advice": str
            }
        """

        # Fetch trending content
        trending_posts = await self.fetch_trending_content(platform, category)

        if not trending_posts:
            return {
                "platform": platform,
                "category": category,
                "patterns": [],
                "top_formats": [],
                "top_topics": [],
                "engagement_drivers": [],
                "content_length": {"optimal_min": 50, "optimal_max": 280, "average": 150},
                "posting_advice": "No trending data available for analysis"
            }

        # Prepare data for AI analysis
        posts_summary = "\n\n".join([
            f"Post {i+1}:\n"
            f"Content: {post['content']}\n"
            f"Engagement Rate: {post['engagement']['engagement_rate']}%\n"
            f"Likes: {post['engagement']['likes']}\n"
            f"Category: {post['category']}"
            for i, post in enumerate(trending_posts[:5])  # Analyze top 5
        ])

        # AI analysis prompt
        prompt = f"""Analyze trending {platform} content and identify patterns:

{posts_summary}

Identify:
1. Common content patterns (formats, structures)
2. Top content formats (lists, questions, stories, etc.)
3. Top topics/themes
4. What drives engagement (hooks, CTAs, emotional triggers)
5. Optimal content length
6. Posting advice for creators

Return ONLY valid JSON:
{{
    "patterns": [
        {{
            "pattern": "Pattern description",
            "examples": ["Example 1", "Example 2"],
            "why_it_works": "Explanation",
            "confidence": 0.85
        }}
    ],
    "top_formats": ["List-based", "Question-based", "Story-telling"],
    "top_topics": ["AI", "Business Growth", "Marketing"],
    "engagement_drivers": ["Strong hooks", "Clear CTAs", "Emotional appeal"],
    "content_length": {{
        "optimal_min": 100,
        "optimal_max": 250,
        "average": 180
    }},
    "posting_advice": "Concise, actionable advice"
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

            # Add metadata
            analysis["platform"] = platform
            analysis["category"] = category or "all"
            analysis["analyzed_posts"] = len(trending_posts)
            analysis["timestamp"] = datetime.now().isoformat()

            return analysis

        except Exception as e:
            print(f"AI analysis error: {e}")

            # Fallback analysis based on simple rules
            return {
                "platform": platform,
                "category": category or "all",
                "patterns": [
                    {
                        "pattern": "High-performing posts use clear, action-oriented language",
                        "examples": ["Just launched...", "5 lessons learned..."],
                        "why_it_works": "Creates immediate interest and promises value",
                        "confidence": 0.75
                    }
                ],
                "top_formats": ["Lists", "Questions", "Announcements"],
                "top_topics": ["Technology", "Business", "Marketing"],
                "engagement_drivers": ["Strong hooks", "Visual elements", "Call-to-action"],
                "content_length": {
                    "optimal_min": 100,
                    "optimal_max": 280,
                    "average": 180
                },
                "posting_advice": "Focus on clear, concise content with strong opening hooks",
                "analyzed_posts": len(trending_posts),
                "timestamp": datetime.now().isoformat()
            }

    async def get_best_posting_times(self, platform: str) -> Dict:
        """
        Get optimal posting times based on trending data analysis

        Args:
            platform: Platform name

        Returns:
            {
                "platform": str,
                "recommendations": [
                    {
                        "day": str,
                        "time_slots": [str],
                        "confidence": str,
                        "reason": str
                    }
                ],
                "timezone": str
            }
        """

        # AI analysis of posting times
        prompt = f"""Based on {platform} engagement patterns, recommend the best times to post.

Consider:
- When users are most active
- Competition levels at different times
- Content type considerations

Return ONLY valid JSON:
{{
    "recommendations": [
        {{
            "day": "Monday-Friday",
            "time_slots": ["8:00 AM - 10:00 AM", "12:00 PM - 1:00 PM", "5:00 PM - 7:00 PM"],
            "confidence": "high",
            "reason": "Peak engagement during commute and lunch breaks"
        }},
        {{
            "day": "Saturday-Sunday",
            "time_slots": ["10:00 AM - 12:00 PM", "7:00 PM - 9:00 PM"],
            "confidence": "medium",
            "reason": "Weekend leisure browsing"
        }}
    ],
    "timezone": "User's local time",
    "general_advice": "Post consistently at the same times to build audience expectations"
}}
"""

        try:
            response = await self.llm.ainvoke(prompt)

            content = response.content.strip()
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            content = content.strip()

            result = json.loads(content)
            result["platform"] = platform
            result["timestamp"] = datetime.now().isoformat()

            return result

        except Exception as e:
            print(f"Posting times analysis error: {e}")

            # Fallback recommendations
            return {
                "platform": platform,
                "recommendations": [
                    {
                        "day": "Monday-Friday",
                        "time_slots": ["8:00 AM - 10:00 AM", "12:00 PM - 1:00 PM", "5:00 PM - 7:00 PM"],
                        "confidence": "high",
                        "reason": "Peak engagement during commute and lunch breaks"
                    },
                    {
                        "day": "Saturday-Sunday",
                        "time_slots": ["10:00 AM - 12:00 PM", "7:00 PM - 9:00 PM"],
                        "confidence": "medium",
                        "reason": "Weekend leisure browsing"
                    }
                ],
                "timezone": "User's local time",
                "general_advice": "Test different times and track what works for your audience",
                "timestamp": datetime.now().isoformat()
            }


# Test the tool
if __name__ == "__main__":
    print("🧪 Testing Trending Analyzer Tool")
    print("=" * 60)

    async def test_analyzer():
        analyzer = TrendingAnalyzerTool()

        print("\n📊 Analyzing Twitter Trends...")
        trends = await analyzer.analyze_trending_patterns("twitter")

        print("\n✅ Analysis Results:")
        print("=" * 60)
        print(f"Platform: {trends['platform']}")
        print(f"Analyzed Posts: {trends['analyzed_posts']}")
        print(f"\n📈 Top Formats:")
        for fmt in trends['top_formats']:
            print(f"  • {fmt}")

        print(f"\n🔥 Top Topics:")
        for topic in trends['top_topics']:
            print(f"  • {topic}")

        print(f"\n💡 Engagement Drivers:")
        for driver in trends['engagement_drivers']:
            print(f"  • {driver}")

        print(f"\n📝 Content Length:")
        print(f"  Optimal: {trends['content_length']['optimal_min']}-{trends['content_length']['optimal_max']} chars")
        print(f"  Average: {trends['content_length']['average']} chars")

        print(f"\n💬 Posting Advice:")
        print(f"  {trends['posting_advice']}")

        print("\n\n⏰ Best Posting Times...")
        times = await analyzer.get_best_posting_times("twitter")

        print("\n✅ Recommendations:")
        print("=" * 60)
        for rec in times['recommendations']:
            print(f"\n📅 {rec['day']} ({rec['confidence']} confidence)")
            print(f"   Times: {', '.join(rec['time_slots'])}")
            print(f"   Why: {rec['reason']}")

        print(f"\n💡 General Advice: {times['general_advice']}")

        print("\n" + "=" * 60)
        print("✅ Analysis complete!")

    # Run async test
    import asyncio
    asyncio.run(test_analyzer())
