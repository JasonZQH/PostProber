"""
🎯 LESSON 3: LangChain with Tools and Function Calling

This example teaches you about tools:
- What are tools and why they're powerful
- How to create custom tools
- How to give AI access to external functions
- Real-world integration examples for PostProber

Key Concepts:
- Tools: Functions that AI can call
- Function calling: AI deciding when to use tools
- Tool schemas: Describing tools to AI
- Agent executor: Managing tool usage
"""

from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.agents import AgentExecutor, create_openai_functions_agent
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict
import os
from dotenv import load_dotenv

# Load environment variables from PostProber .env file
load_dotenv(dotenv_path="../../.env")

def setup_ai_model():
    """Set up the AI model (same as previous lessons)"""
    return ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=1000
    )

# 📖 LESSON: Creating your first tool
@tool
def get_current_time() -> str:
    """Get the current date and time. Useful for scheduling posts or time-sensitive content."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def count_characters(text: str) -> int:
    """Count the number of characters in a text. Useful for platform character limits."""
    return len(text)

@tool
def generate_hashtags(topic: str, count: int = 5) -> List[str]:
    """Generate hashtags for a given topic. Returns a list of relevant hashtags."""
    # This is a simple example - in real PostProber, this would use trending data
    base_hashtags = {
        "coffee": ["#Coffee", "#MorningBrew", "#CoffeeLovers", "#Barista", "#CoffeeTime"],
        "technology": ["#Tech", "#Innovation", "#Digital", "#Future", "#TechTrends"],
        "fitness": ["#Fitness", "#Workout", "#HealthyLifestyle", "#GymLife", "#FitnessTips"],
        "food": ["#Food", "#Foodie", "#Delicious", "#Cooking", "#Recipe"]
    }

    # Simple matching logic (in real app, this would be much more sophisticated)
    for key, tags in base_hashtags.items():
        if key.lower() in topic.lower():
            return tags[:count]

    # Generic hashtags if no match
    return [f"#{topic.title()}", "#SocialMedia", "#Content", "#Engagement", "#PostProber"]

# 📖 LESSON: More sophisticated PostProber tools
@tool
def check_posting_schedule(platform: str, datetime_str: str) -> Dict:
    """Check if a posting time is optimal for a given platform."""
    try:
        post_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        hour = post_time.hour
        day_of_week = post_time.weekday()  # 0 = Monday, 6 = Sunday

        # Optimal posting times (simplified examples)
        optimal_times = {
            "twitter": {
                "weekday_hours": [9, 12, 17],  # 9am, 12pm, 5pm
                "weekend_hours": [10, 14]      # 10am, 2pm
            },
            "linkedin": {
                "weekday_hours": [8, 12, 17],  # 8am, 12pm, 5pm
                "weekend_hours": []             # Not recommended
            },
            "instagram": {
                "weekday_hours": [11, 14, 17], # 11am, 2pm, 5pm
                "weekend_hours": [10, 13]      # 10am, 1pm
            }
        }

        platform_times = optimal_times.get(platform.lower(), {"weekday_hours": [12], "weekend_hours": [12]})

        is_weekend = day_of_week >= 5
        optimal_hours = platform_times["weekend_hours"] if is_weekend else platform_times["weekday_hours"]

        is_optimal = hour in optimal_hours

        return {
            "is_optimal": is_optimal,
            "current_hour": hour,
            "optimal_hours": optimal_hours,
            "day_type": "weekend" if is_weekend else "weekday",
            "platform": platform,
            "recommendation": f"{'Good' if is_optimal else 'Consider'} time for {platform}"
        }

    except ValueError:
        return {"error": "Invalid datetime format. Use YYYY-MM-DD HH:MM:SS"}

@tool
def analyze_content_sentiment(text: str) -> Dict:
    """Analyze the sentiment and tone of content."""
    # Simplified sentiment analysis (in real app, use proper NLP libraries)
    positive_words = ["great", "awesome", "love", "amazing", "excellent", "fantastic", "wonderful"]
    negative_words = ["bad", "terrible", "hate", "awful", "horrible", "worst"]
    professional_words = ["strategy", "growth", "optimization", "efficiency", "professional"]

    text_lower = text.lower()

    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    professional_count = sum(1 for word in professional_words if word in text_lower)

    if positive_count > negative_count:
        sentiment = "positive"
    elif negative_count > positive_count:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    tone = "professional" if professional_count > 2 else "casual"

    return {
        "sentiment": sentiment,
        "tone": tone,
        "word_count": len(text.split()),
        "character_count": len(text),
        "positive_indicators": positive_count,
        "professional_indicators": professional_count
    }

# 📖 LESSON: Using tools with AI agents
def basic_tool_usage():
    """Learn how to use tools with AI"""

    llm = setup_ai_model()

    # Create a list of tools
    tools = [get_current_time, count_characters, generate_hashtags]

    # Create a prompt that knows about tools
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are PostProber AI, a helpful social media assistant.
        You have access to several tools to help users with their social media content.
        Use these tools when they would be helpful to answer the user's question.

        Available tools:
        - get_current_time: Get the current date and time
        - count_characters: Count characters in text
        - generate_hashtags: Generate relevant hashtags for topics
        """),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    # Create an agent that can use tools
    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # Test with different queries
    queries = [
        "What time is it right now?",
        "How many characters are in this tweet: 'Just launched our new social media tool! 🚀 #SocialMedia #Launch'",
        "Generate 5 hashtags for a post about healthy breakfast recipes",
        "I want to post about coffee at the best time. What time is it now and give me some hashtags?"
    ]

    for i, query in enumerate(queries, 1):
        print(f"\n--- Query {i} ---")
        print(f"🤔 User: {query}")

        try:
            result = agent_executor.invoke({"input": query})
            print(f"🤖 AI: {result['output']}")
        except Exception as e:
            print(f"❌ Error: {e}")

        print("-" * 50)

# 📖 LESSON: Advanced PostProber tool integration
def postprober_agent_example():
    """A more realistic PostProber agent with multiple tools"""

    llm = setup_ai_model()

    # All PostProber tools
    tools = [
        get_current_time,
        count_characters,
        generate_hashtags,
        check_posting_schedule,
        analyze_content_sentiment
    ]

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are PostProber AI, an expert social media management assistant.

        Your mission: Help users create, optimize, and schedule amazing social media content.

        You have access to these powerful tools:
        - get_current_time: Check current date/time for scheduling
        - count_characters: Verify content fits platform limits
        - generate_hashtags: Create relevant hashtags
        - check_posting_schedule: Analyze if posting time is optimal
        - analyze_content_sentiment: Understand content tone and sentiment

        Always be helpful, professional, and provide actionable advice.
        When suggesting improvements, explain why they would work better.
        """),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # Realistic PostProber scenarios
    scenarios = [
        "I want to post 'Just launched our new app! Download now and boost your productivity!' on Twitter. Is this good to post now?",

        "Analyze this LinkedIn post for me: 'Excited to share our new strategy for remote team collaboration. We've seen 40% improvement in productivity using these methods.' Then suggest hashtags.",

        "I'm planning to post about coffee recipes on Instagram at 2024-12-25 15:30:00. Is that a good time? Also generate hashtags for coffee content."
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🎯 Scenario {i}")
        print(f"👤 User: {scenario}")
        print("🤖 PostProber AI is thinking...")

        try:
            result = agent_executor.invoke({"input": scenario})
            print(f"✨ Result:\n{result['output']}")
        except Exception as e:
            print(f"❌ Error: {e}")

        print("=" * 60)

# 📖 LESSON: Creating custom tools for your app
def create_custom_postprober_tools():
    """Learn how to create tools specific to your application"""

    @tool
    def get_user_analytics(user_id: str, days: int = 7) -> Dict:
        """Get user's posting analytics for the last N days."""
        # In real PostProber, this would query your database
        return {
            "user_id": user_id,
            "period_days": days,
            "total_posts": random.randint(5, 20),
            "total_engagement": random.randint(100, 1000),
            "avg_engagement_rate": round(random.uniform(2.0, 8.5), 2),
            "best_performing_platform": random.choice(["Twitter", "LinkedIn", "Instagram"]),
            "suggestion": "Your engagement rate is above average! Consider posting more frequently on your best-performing platform."
        }

    @tool
    def schedule_post(content: str, platform: str, schedule_time: str) -> Dict:
        """Schedule a post for future publishing."""
        # In real PostProber, this would save to your scheduling system
        return {
            "status": "scheduled",
            "post_id": f"post_{random.randint(1000, 9999)}",
            "content": content,
            "platform": platform,
            "scheduled_for": schedule_time,
            "message": f"✅ Post scheduled for {platform} at {schedule_time}"
        }

    @tool
    def get_trending_topics(platform: str, category: str = "general") -> List[str]:
        """Get trending topics for a specific platform and category."""
        # In real PostProber, this would use platform APIs
        trending_topics = {
            "twitter": ["#AI", "#Tech", "#Productivity", "#Remote Work", "#Startup"],
            "linkedin": ["#Leadership", "#Career", "#Professional Development", "#Industry Insights", "#Networking"],
            "instagram": ["#Lifestyle", "#Motivation", "#BehindTheScenes", "#Community", "#Inspiration"]
        }
        return trending_topics.get(platform.lower(), ["#Trending", "#Popular", "#Now"])

    # Test the custom tools
    llm = setup_ai_model()
    tools = [get_user_analytics, schedule_post, get_trending_topics]

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are PostProber's advanced AI assistant with access to user data and scheduling capabilities.

        You can:
        - Check user analytics and performance
        - Schedule posts for future publishing
        - Get trending topics for any platform

        Always provide helpful, data-driven recommendations.
        """),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # Test custom tools
    test_query = "Check my analytics for the last 7 days (user ID: user123), then suggest what content I should post next based on trends, and schedule it for tomorrow at 2pm on my best platform."

    print("🔧 Testing Custom PostProber Tools:")
    print("="*50)
    print(f"👤 User: {test_query}")

    try:
        result = agent_executor.invoke({"input": test_query})
        print(f"🚀 PostProber AI:\n{result['output']}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🛠️ Welcome to LangChain Tools and Function Calling!")
    print("=" * 60)

    # Uncomment these examples one by one to learn:

    # Example 1: Basic tool usage
    print("\n📖 Example 1: Basic Tool Usage")
    try:
        basic_tool_usage()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Tip: API key is loaded from PostProber .env file automatically")

    # Example 2: Advanced PostProber agent
    print("\n📖 Example 2: PostProber Agent with Tools")
    # postprober_agent_example()

    # Example 3: Custom tools
    print("\n📖 Example 3: Custom PostProber Tools")
    # create_custom_postprober_tools()

    print("\n🎉 Amazing! You now understand tools and function calling!")
    print("🚀 This is where AI becomes truly powerful - it can interact with your app!")
    print("📚 Next: Check out 04_basic_langgraph.py to learn about state machines and workflows")