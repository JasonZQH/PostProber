"""
Content Optimization Tool

AI-powered tool that optimizes social media content for maximum engagement.
Uses LangChain + OpenAI to analyze and improve post quality.
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from typing import Dict
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="../../../.env")


class ContentOptimizerTool:
    """
    Tool for optimizing social media content

    Analyzes content and provides:
    - Optimized version with better engagement potential
    - Quality score (0-100)
    - Specific improvements made
    """

    def __init__(self):
        """Initialize the content optimizer with OpenAI LLM"""
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,  # Balanced creativity
            max_tokens=800,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # Platform-specific character limits and best practices
        self.platform_limits = {
            "twitter": {
                "max_chars": 280,
                "optimal_range": (150, 200),
                "best_practices": "Use clear hooks, hashtags, and engagement drivers"
            },
            "linkedin": {
                "max_chars": 3000,
                "optimal_range": (150, 300),
                "best_practices": "Professional tone, value-driven, thought leadership"
            },
            "instagram": {
                "max_chars": 2200,
                "optimal_range": (125, 250),
                "best_practices": "Visual-first, storytelling, authentic voice"
            },
            "facebook": {
                "max_chars": 63206,
                "optimal_range": (100, 250),
                "best_practices": "Conversational, community-focused, engaging"
            }
        }

    def optimize(self, content: str, platform: str) -> Dict:
        """
        Optimize content for specific platform

        Args:
            content: Original post content
            platform: Target platform (twitter, linkedin, instagram, facebook)

        Returns:
            {
                "optimized_content": str,
                "score": int (0-100),
                "improvements": List[str],
                "original_length": int,
                "optimized_length": int,
                "platform": str
            }
        """

        # Validate platform
        platform = platform.lower()
        if platform not in self.platform_limits:
            platform = "twitter"  # Default fallback

        platform_info = self.platform_limits[platform]

        # Create optimization prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a social media optimization expert specializing in {platform}.
            Your goal is to make content more engaging while maintaining the core message.

            IMPORTANT: Return ONLY a valid JSON object with this EXACT structure (no markdown, no code blocks):
            {{
                "optimized_content": "the improved content here",
                "score": 85,
                "improvements": [
                    "Added stronger hook",
                    "Improved call-to-action",
                    "Optimized for platform"
                ]
            }}

            The score should be realistic (60-95 range) based on actual quality.
            """),
            ("human", """
            Platform: {platform}
            Character limit: {max_chars}
            Optimal length: {optimal_range}
            Best practices: {best_practices}

            Original content: "{content}"

            Optimize this content by:
            1. Creating an irresistible hook (first line grabs attention)
            2. Ensuring message clarity and focus
            3. Adding appropriate emotional appeal
            4. Including a compelling call-to-action
            5. Following {platform} best practices
            6. Keeping it within optimal length range

            Improve the content but keep the core message intact.
            Make it feel natural, not over-optimized or salesy.
            """)
        ])

        # Create chain
        chain = prompt | self.llm | StrOutputParser()

        try:
            # Invoke LLM
            response = chain.invoke({
                "content": content,
                "platform": platform.title(),
                "max_chars": platform_info["max_chars"],
                "optimal_range": f"{platform_info['optimal_range'][0]}-{platform_info['optimal_range'][1]} characters",
                "best_practices": platform_info["best_practices"]
            })

            # Parse JSON response
            # Remove markdown code blocks if present
            response = response.strip()
            if response.startswith("```"):
                # Remove ```json and ``` markers
                response = response.split("```")[1]
                if response.startswith("json"):
                    response = response[4:]
            response = response.strip()

            result = json.loads(response)

            # Add metadata
            result["original_length"] = len(content)
            result["optimized_length"] = len(result.get("optimized_content", content))
            result["platform"] = platform

            # Ensure score is in valid range
            if "score" in result:
                result["score"] = max(50, min(100, result["score"]))
            else:
                result["score"] = 75  # Default score

            # Ensure improvements is a list
            if "improvements" not in result or not isinstance(result["improvements"], list):
                result["improvements"] = ["Content optimized for better engagement"]

            return result

        except json.JSONDecodeError as e:
            # Fallback if JSON parsing fails
            print(f"JSON parsing error: {e}")
            print(f"Raw response: {response}")

            return {
                "optimized_content": content,
                "score": 65,
                "improvements": [
                    "Consider adding a stronger hook",
                    "Add a clear call-to-action",
                    f"Optimize for {platform} best practices"
                ],
                "original_length": len(content),
                "optimized_length": len(content),
                "platform": platform,
                "error": "Could not fully optimize, showing original"
            }

        except Exception as e:
            # General error fallback
            print(f"Optimization error: {e}")

            return {
                "error": str(e),
                "optimized_content": content,
                "score": 50,
                "improvements": ["Unable to optimize at this time. Please try again."],
                "original_length": len(content),
                "optimized_length": len(content),
                "platform": platform
            }


# Test the tool
if __name__ == "__main__":
    print("🧪 Testing Content Optimizer Tool")
    print("=" * 60)

    optimizer = ContentOptimizerTool()

    # Test content
    test_content = "Check out our new AI tool for social media management"
    test_platform = "twitter"

    print(f"\n📝 Original Content: {test_content}")
    print(f"🎯 Platform: {test_platform}")
    print("\n⏳ Optimizing...")

    result = optimizer.optimize(test_content, test_platform)

    print("\n✅ Optimization Complete!")
    print(f"📊 Score: {result['score']}/100")
    print(f"✨ Optimized Content: {result['optimized_content']}")
    print(f"\n🔧 Improvements:")
    for improvement in result['improvements']:
        print(f"  • {improvement}")
    print(f"\n📏 Length: {result['original_length']} → {result['optimized_length']} characters")
