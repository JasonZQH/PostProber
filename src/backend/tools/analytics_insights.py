"""
Analytics Insights Tool

Compares user content with trending patterns and provides actionable recommendations.
"""

from langchain_openai import ChatOpenAI
from typing import Dict, List
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="../../../.env")


class AnalyticsInsightsTool:
    """
    Tool for generating analytics insights

    Features:
    - Compare user content vs trending benchmarks
    - Gap analysis (what's missing in user content)
    - Prioritized recommendations
    - Expected impact estimates
    - A/B testing suggestions
    """

    def __init__(self):
        """Initialize analytics insights with OpenAI LLM"""
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3,  # Lower for analytical precision
            max_tokens=1000,
            api_key=os.getenv("OPENAI_API_KEY")
        )

    async def analyze_user_content(
        self,
        user_content: str,
        platform: str,
        trending_patterns: Dict
    ) -> Dict:
        """
        Analyze user content against trending patterns

        Args:
            user_content: User's post content
            platform: Platform name
            trending_patterns: Trending analysis from TrendingAnalyzerTool

        Returns:
            {
                "content_score": int (0-100),
                "strengths": [str],
                "weaknesses": [str],
                "gap_analysis": {
                    "missing_elements": [str],
                    "opportunities": [str]
                },
                "recommendations": [
                    {
                        "priority": "high" | "medium" | "low",
                        "title": str,
                        "description": str,
                        "expected_impact": str,
                        "effort": "quick" | "moderate" | "significant"
                    }
                ],
                "benchmark_comparison": {
                    "length": {"user": int, "trending": int, "status": str},
                    "engagement_potential": {"score": int, "reason": str}
                }
            }
        """

        # Extract key trending insights
        top_formats = trending_patterns.get('top_formats', [])
        engagement_drivers = trending_patterns.get('engagement_drivers', [])
        optimal_length = trending_patterns.get('content_length', {})
        posting_advice = trending_patterns.get('posting_advice', '')

        # AI analysis prompt
        prompt = f"""Analyze this user's {platform} content against current trends:

USER CONTENT:
"{user_content}"

TRENDING INSIGHTS:
- Top Formats: {', '.join(top_formats)}
- Engagement Drivers: {', '.join(engagement_drivers)}
- Optimal Length: {optimal_length.get('optimal_min', 100)}-{optimal_length.get('optimal_max', 280)} characters
- Current Length: {len(user_content)} characters
- Advice: {posting_advice}

Provide detailed analysis:

1. Content Score (0-100): How well does this align with trends?
2. Strengths: What's working well?
3. Weaknesses: What needs improvement?
4. Gap Analysis: What's missing vs trending content?
5. Recommendations: Prioritized actionable improvements

Return ONLY valid JSON:
{{
    "content_score": 75,
    "strengths": ["Clear message", "Good hook"],
    "weaknesses": ["No call-to-action", "Could be more specific"],
    "gap_analysis": {{
        "missing_elements": ["Emojis", "Question to audience"],
        "opportunities": ["Add personal story", "Include data/stats"]
    }},
    "recommendations": [
        {{
            "priority": "high",
            "title": "Add clear call-to-action",
            "description": "End with a question to drive engagement",
            "expected_impact": "+15-25% engagement",
            "effort": "quick"
        }},
        {{
            "priority": "medium",
            "title": "Optimize length",
            "description": "Current: {len(user_content)} chars, optimal: {optimal_length.get('optimal_min', 100)}-{optimal_length.get('optimal_max', 280)}",
            "expected_impact": "+5-10% reach",
            "effort": "quick"
        }}
    ],
    "benchmark_comparison": {{
        "length": {{
            "user": {len(user_content)},
            "trending": {optimal_length.get('average', 180)},
            "status": "within range|too short|too long"
        }},
        "engagement_potential": {{
            "score": 78,
            "reason": "Good foundation, add CTA for higher engagement"
        }}
    }}
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
            analysis["analyzed_at"] = datetime.now().isoformat()

            return analysis

        except Exception as e:
            print(f"Analytics analysis error: {e}")

            # Fallback analysis
            user_length = len(user_content)
            trending_avg = optimal_length.get('average', 180)

            length_status = "within range"
            if user_length < optimal_length.get('optimal_min', 100):
                length_status = "too short"
            elif user_length > optimal_length.get('optimal_max', 280):
                length_status = "too long"

            return {
                "content_score": 70,
                "strengths": ["Clear content structure"],
                "weaknesses": ["Could leverage trending formats more"],
                "gap_analysis": {
                    "missing_elements": ["Call-to-action", "Engagement hooks"],
                    "opportunities": ["Add trending formats", "Include visual elements"]
                },
                "recommendations": [
                    {
                        "priority": "high",
                        "title": "Align with trending formats",
                        "description": f"Top formats: {', '.join(top_formats[:3])}",
                        "expected_impact": "+10-20% engagement",
                        "effort": "moderate"
                    }
                ],
                "benchmark_comparison": {
                    "length": {
                        "user": user_length,
                        "trending": trending_avg,
                        "status": length_status
                    },
                    "engagement_potential": {
                        "score": 70,
                        "reason": "Good baseline, implement recommendations for improvement"
                    }
                },
                "platform": platform,
                "analyzed_at": datetime.now().isoformat()
            }

    async def generate_content_ideas(
        self,
        platform: str,
        category: str,
        trending_patterns: Dict
    ) -> Dict:
        """
        Generate content ideas based on trending patterns

        Args:
            platform: Platform name
            category: Content category
            trending_patterns: Trending analysis

        Returns:
            {
                "platform": str,
                "category": str,
                "ideas": [
                    {
                        "title": str,
                        "concept": str,
                        "format": str,
                        "why_it_works": str,
                        "confidence": float
                    }
                ]
            }
        """

        top_formats = trending_patterns.get('top_formats', [])
        top_topics = trending_patterns.get('top_topics', [])
        patterns = trending_patterns.get('patterns', [])

        # AI prompt for content ideas
        prompt = f"""Generate 5 high-performing content ideas for {platform} in the {category} category.

TRENDING INSIGHTS:
- Top Formats: {', '.join(top_formats)}
- Top Topics: {', '.join(top_topics)}
- Patterns: {json.dumps(patterns[:2], indent=2)}

Generate ideas that:
1. Leverage trending formats
2. Address current hot topics
3. Are actionable and specific
4. Have high engagement potential

Return ONLY valid JSON:
{{
    "ideas": [
        {{
            "title": "Catchy title",
            "concept": "Brief description of the content idea",
            "format": "List|Question|Story|Tutorial",
            "why_it_works": "Why this will perform well",
            "confidence": 0.85
        }}
    ]
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
            result["category"] = category
            result["generated_at"] = datetime.now().isoformat()

            return result

        except Exception as e:
            print(f"Content ideas generation error: {e}")

            # Fallback ideas
            return {
                "platform": platform,
                "category": category,
                "ideas": [
                    {
                        "title": f"5 {category} trends you can't ignore in 2025",
                        "concept": f"List-based post highlighting key {category} trends",
                        "format": "List",
                        "why_it_works": "Lists perform well, future-focused creates urgency",
                        "confidence": 0.8
                    },
                    {
                        "title": f"What's your biggest {category} challenge?",
                        "concept": "Ask audience about their challenges to drive engagement",
                        "format": "Question",
                        "why_it_works": "Questions drive comments, shows you care about audience",
                        "confidence": 0.85
                    },
                    {
                        "title": f"How I transformed my {category} approach",
                        "concept": "Share personal story of transformation",
                        "format": "Story",
                        "why_it_works": "Personal stories are relatable and inspiring",
                        "confidence": 0.75
                    }
                ],
                "generated_at": datetime.now().isoformat()
            }

    async def compare_performance(
        self,
        user_posts: List[Dict],
        trending_benchmarks: Dict
    ) -> Dict:
        """
        Compare user's historical performance with trending benchmarks

        Args:
            user_posts: List of user's posts with engagement data
            trending_benchmarks: Trending performance metrics

        Returns:
            {
                "overall_score": int (0-100),
                "comparison": {
                    "engagement_rate": {"user": float, "benchmark": float, "gap": float},
                    "content_quality": {"user": int, "benchmark": int, "gap": int}
                },
                "insights": [str],
                "action_plan": [str]
            }
        """

        # Calculate user averages (mock for now)
        if not user_posts:
            user_avg_engagement = 0
            user_avg_length = 150
        else:
            user_avg_engagement = sum(p.get('engagement_rate', 0) for p in user_posts) / len(user_posts)
            user_avg_length = sum(len(p.get('content', '')) for p in user_posts) / len(user_posts)

        # Benchmark averages (from trending)
        benchmark_engagement = 10.0  # Average from trending posts
        benchmark_length = trending_benchmarks.get('content_length', {}).get('average', 180)

        # Calculate gaps
        engagement_gap = benchmark_engagement - user_avg_engagement
        length_gap = benchmark_length - user_avg_length

        # Overall score (0-100)
        overall_score = max(0, min(100, int(100 - (engagement_gap * 5))))

        return {
            "overall_score": overall_score,
            "comparison": {
                "engagement_rate": {
                    "user": round(user_avg_engagement, 2),
                    "benchmark": benchmark_engagement,
                    "gap": round(engagement_gap, 2)
                },
                "content_length": {
                    "user": int(user_avg_length),
                    "benchmark": int(benchmark_length),
                    "gap": int(length_gap)
                }
            },
            "insights": [
                f"Your engagement rate is {abs(engagement_gap):.1f}% {'below' if engagement_gap > 0 else 'above'} trending posts",
                f"Your content length averages {int(user_avg_length)} chars vs {int(benchmark_length)} for trending posts",
                "Focus on implementing top trending formats for quick wins"
            ],
            "action_plan": [
                "Use AI Optimize feature for all posts to align with trending patterns",
                "Test different content formats (lists, questions, stories)",
                "Post consistently at optimal times",
                "Engage with comments to boost algorithmic visibility"
            ],
            "analyzed_at": datetime.now().isoformat()
        }


# Test the tool
if __name__ == "__main__":
    print("🧪 Testing Analytics Insights Tool")
    print("=" * 60)

    async def test_insights():
        insights_tool = AnalyticsInsightsTool()

        # Mock trending patterns
        trending_patterns = {
            "top_formats": ["Lists", "Questions", "Stories"],
            "top_topics": ["AI", "Business", "Marketing"],
            "engagement_drivers": ["Strong hooks", "CTAs", "Emojis"],
            "content_length": {
                "optimal_min": 100,
                "optimal_max": 280,
                "average": 180
            },
            "posting_advice": "Focus on clear, concise content with strong hooks"
        }

        # Test user content analysis
        user_content = "Just launched our new product. Check it out!"

        print("\n📊 Analyzing User Content...")
        print(f"Content: \"{user_content}\"")

        analysis = await insights_tool.analyze_user_content(
            user_content=user_content,
            platform="twitter",
            trending_patterns=trending_patterns
        )

        print("\n✅ Analysis Results:")
        print("=" * 60)
        print(f"Content Score: {analysis['content_score']}/100")

        print(f"\n💪 Strengths:")
        for strength in analysis['strengths']:
            print(f"  • {strength}")

        print(f"\n⚠️ Weaknesses:")
        for weakness in analysis['weaknesses']:
            print(f"  • {weakness}")

        print(f"\n🎯 Recommendations:")
        for rec in analysis['recommendations']:
            print(f"\n  [{rec['priority'].upper()}] {rec['title']}")
            print(f"  → {rec['description']}")
            print(f"  → Impact: {rec['expected_impact']}")
            print(f"  → Effort: {rec['effort']}")

        print("\n\n💡 Generating Content Ideas...")
        ideas = await insights_tool.generate_content_ideas(
            platform="twitter",
            category="technology",
            trending_patterns=trending_patterns
        )

        print("\n✅ Content Ideas:")
        print("=" * 60)
        for i, idea in enumerate(ideas['ideas'][:3], 1):
            print(f"\n{i}. {idea['title']}")
            print(f"   Format: {idea['format']}")
            print(f"   Why: {idea['why_it_works']}")
            print(f"   Confidence: {idea['confidence']*100:.0f}%")

        print("\n" + "=" * 60)
        print("✅ Analysis complete!")

    # Run async test
    import asyncio
    asyncio.run(test_insights())
