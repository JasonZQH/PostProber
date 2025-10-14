"""
Hashtag Generator Tool

AI-powered tool that generates strategic hashtag mixes for social media posts.
Uses LangChain + OpenAI to analyze content and suggest relevant hashtags.
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from typing import Dict, List
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="../../../.env")


class HashtagGeneratorTool:
    """
    Tool for generating strategic hashtag mixes

    Creates an optimal mix of:
    - Trending/popular hashtags (broad reach)
    - Niche/community hashtags (engaged audience)
    - Branded/unique hashtags (brand identity)
    """

    def __init__(self):
        """Initialize the hashtag generator with OpenAI LLM"""
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.8,  # Higher for creative hashtag generation
            max_tokens=500,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # Platform-specific hashtag guidelines
        self.platform_guidelines = {
            "twitter": {
                "optimal_count": (2, 3),
                "max_count": 5,
                "style": "concise, trending-focused"
            },
            "linkedin": {
                "optimal_count": (3, 5),
                "max_count": 7,
                "style": "professional, industry-specific"
            },
            "instagram": {
                "optimal_count": (8, 15),
                "max_count": 30,
                "style": "diverse mix, community-focused"
            },
            "facebook": {
                "optimal_count": (2, 4),
                "max_count": 5,
                "style": "relevant, not excessive"
            }
        }

    def generate(self, content: str, platform: str) -> Dict:
        """
        Generate strategic hashtag mix

        Args:
            content: Post content to analyze
            platform: Target platform

        Returns:
            {
                "hashtags": [
                    {"tag": "#AI", "category": "trending", "reach": "high"},
                    {"tag": "#TechTips", "category": "niche", "reach": "medium"},
                    ...
                ],
                "strategy": "explanation of hashtag choices",
                "platform": str,
                "count": int
            }
        """

        # Validate platform
        platform = platform.lower()
        if platform not in self.platform_guidelines:
            platform = "twitter"  # Default fallback

        guidelines = self.platform_guidelines[platform]

        # Create hashtag generation prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a social media hashtag strategist.
            Generate optimal hashtag mixes that balance reach, engagement, and relevance.

            IMPORTANT: Return ONLY a valid JSON object (no markdown, no code blocks):
            {{
                "hashtags": [
                    {{"tag": "#Example", "category": "trending", "reach": "high"}},
                    {{"tag": "#Niche", "category": "community", "reach": "medium"}},
                    {{"tag": "#Brand", "category": "branded", "reach": "targeted"}}
                ],
                "strategy": "Brief 1-2 sentence explanation of why these hashtags work"
            }}

            Categories:
            - "trending": Popular, broad-reach hashtags
            - "community": Niche, engaged audience hashtags
            - "branded": Unique to brand/campaign hashtags

            Reach levels:
            - "high": Millions of posts, broad exposure
            - "medium": Thousands to hundreds of thousands, balanced
            - "targeted": Smaller but highly engaged community
            """),
            ("human", """
            Platform: {platform}
            Content: "{content}"
            Optimal hashtag count: {optimal_count}
            Style: {style}

            Generate {optimal_count} strategic hashtags:

            1. 40% trending/popular hashtags (broad reach, discoverable)
            2. 40% niche/topic-specific hashtags (engaged community)
            3. 20% branded/unique hashtags (brand identity)

            Requirements:
            - Highly relevant to the content
            - Mix of reach levels for balanced visibility
            - Actually useful for {platform} audience
            - No overly generic hashtags like #love #instagood
            - Focus on the specific topic and value proposition

            Return the JSON response with hashtags and strategy explanation.
            """)
        ])

        # Create chain
        chain = prompt | self.llm | StrOutputParser()

        try:
            # Invoke LLM
            response = chain.invoke({
                "content": content,
                "platform": platform.title(),
                "optimal_count": f"{guidelines['optimal_count'][0]}-{guidelines['optimal_count'][1]}",
                "style": guidelines["style"]
            })

            # Parse JSON response
            # Remove markdown code blocks if present
            response = response.strip()
            if response.startswith("```"):
                response = response.split("```")[1]
                if response.startswith("json"):
                    response = response[4:]
            response = response.strip()

            result = json.loads(response)

            # Add metadata
            result["platform"] = platform
            result["count"] = len(result.get("hashtags", []))

            # Validate hashtag format
            if "hashtags" in result:
                validated_hashtags = []
                for ht in result["hashtags"]:
                    # Ensure tag starts with #
                    tag = ht.get("tag", "")
                    if not tag.startswith("#"):
                        tag = f"#{tag}"

                    # Remove spaces and special characters
                    tag = tag.replace(" ", "").replace(".", "").replace(",", "")

                    validated_hashtags.append({
                        "tag": tag,
                        "category": ht.get("category", "community"),
                        "reach": ht.get("reach", "medium")
                    })

                result["hashtags"] = validated_hashtags

            # Ensure strategy exists
            if "strategy" not in result or not result["strategy"]:
                result["strategy"] = "Balanced mix of trending and niche hashtags for optimal reach and engagement."

            return result

        except json.JSONDecodeError as e:
            # Fallback hashtags if JSON parsing fails
            print(f"JSON parsing error: {e}")
            print(f"Raw response: {response}")

            # Generate basic hashtags based on content keywords
            fallback_hashtags = self._generate_fallback_hashtags(content, platform)

            return {
                "hashtags": fallback_hashtags,
                "strategy": "Generated hashtags based on content keywords.",
                "platform": platform,
                "count": len(fallback_hashtags)
            }

        except Exception as e:
            # General error fallback
            print(f"Hashtag generation error: {e}")

            fallback_hashtags = self._generate_fallback_hashtags(content, platform)

            return {
                "error": str(e),
                "hashtags": fallback_hashtags,
                "strategy": "Using fallback hashtags. Please try again for optimized results.",
                "platform": platform,
                "count": len(fallback_hashtags)
            }

    def _generate_fallback_hashtags(self, content: str, platform: str) -> List[Dict]:
        """Generate simple fallback hashtags if AI fails"""

        # Generic but relevant hashtags
        fallback_sets = {
            "twitter": [
                {"tag": "#SocialMedia", "category": "trending", "reach": "high"},
                {"tag": "#ContentCreation", "category": "community", "reach": "medium"},
                {"tag": "#DigitalMarketing", "category": "niche", "reach": "medium"}
            ],
            "linkedin": [
                {"tag": "#SocialMediaMarketing", "category": "trending", "reach": "high"},
                {"tag": "#ContentStrategy", "category": "community", "reach": "medium"},
                {"tag": "#BusinessGrowth", "category": "niche", "reach": "medium"},
                {"tag": "#MarketingTips", "category": "community", "reach": "medium"}
            ],
            "instagram": [
                {"tag": "#SocialMedia", "category": "trending", "reach": "high"},
                {"tag": "#ContentCreator", "category": "community", "reach": "medium"},
                {"tag": "#DigitalMarketing", "category": "niche", "reach": "medium"},
                {"tag": "#BusinessTips", "category": "community", "reach": "medium"},
                {"tag": "#MarketingStrategy", "category": "niche", "reach": "medium"}
            ],
            "facebook": [
                {"tag": "#SocialMedia", "category": "trending", "reach": "high"},
                {"tag": "#ContentMarketing", "category": "community", "reach": "medium"},
                {"tag": "#BusinessGrowth", "category": "niche", "reach": "medium"}
            ]
        }

        return fallback_sets.get(platform, fallback_sets["twitter"])


# Test the tool
if __name__ == "__main__":
    print("🧪 Testing Hashtag Generator Tool")
    print("=" * 60)

    generator = HashtagGeneratorTool()

    # Test content
    test_content = "Just launched our AI-powered social media management tool! It helps you optimize content, schedule posts, and track engagement across all platforms. 🚀"
    test_platform = "twitter"

    print(f"\n📝 Content: {test_content}")
    print(f"🎯 Platform: {test_platform}")
    print("\n⏳ Generating hashtags...")

    result = generator.generate(test_content, test_platform)

    print("\n✅ Hashtags Generated!")
    print(f"\n📊 Total: {result['count']} hashtags")
    print(f"💡 Strategy: {result['strategy']}")
    print(f"\n🏷️ Hashtags:")

    for ht in result['hashtags']:
        category_icon = {
            "trending": "🔥",
            "community": "👥",
            "branded": "🏷️"
        }.get(ht['category'], "•")

        reach_icon = {
            "high": "📈",
            "medium": "📊",
            "targeted": "🎯"
        }.get(ht['reach'], "•")

        print(f"  {category_icon} {ht['tag']} - {ht['category']} ({reach_icon} {ht['reach']} reach)")
