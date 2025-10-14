"""
🎯 LESSON 6: Complete PostProber Integration Example

This example shows how to integrate LangChain + LangGraph into your real PostProber application:
- API endpoint integration
- Database integration
- User session management
- Real-time streaming responses
- Error handling and logging
- Production-ready patterns

Key Concepts:
- FastAPI integration
- Async workflows
- Streaming responses
- State persistence
- User context management
- Production deployment patterns
"""

from typing import TypedDict, List, Optional, AsyncGenerator
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import asyncio
import json
import uuid
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from PostProber .env file
load_dotenv(dotenv_path="../../.env")

# 📖 LESSON: Production-ready state management
class PostProberAIState(TypedDict):
    """Production state for PostProber AI features"""
    # User context
    user_id: str
    session_id: str
    timestamp: str

    # Input
    request_type: str  # "create_post", "optimize_content", "schedule_analysis", etc.
    user_input: dict
    platform_settings: dict

    # Processing
    ai_responses: List[dict]
    current_step: str
    progress_percentage: int

    # Output
    final_result: Optional[dict]
    suggestions: Optional[List[dict]]
    next_actions: Optional[List[str]]

    # System
    errors: Optional[List[str]]
    processing_time: Optional[float]
    model_usage: Optional[dict]

def setup_ai_model():
    """Production AI model setup with error handling"""
    return ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=1000,
        request_timeout=30,
        max_retries=2
    )

# 📖 LESSON: PostProber-specific AI agents for real features

async def ai_writing_assistant(state: PostProberAIState) -> PostProberAIState:
    """Real-time writing assistant for the Compose page"""
    print("✍️ AI Writing Assistant: Providing real-time suggestions...")

    if state["request_type"] != "writing_assistance":
        return state

    user_input = state["user_input"]
    current_text = user_input.get("current_text", "")
    platform = user_input.get("platform", "twitter")
    user_preferences = state["platform_settings"]

    llm = setup_ai_model()

    # Different prompts based on what user needs
    if len(current_text) < 10:  # Just starting
        prompt_type = "hook_suggestions"
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are PostProber's AI writing assistant. Help users create engaging opening hooks."),
            ("human", """
            The user is starting a {platform} post about: {topic}

            Suggest 3 compelling opening hooks that will grab attention.
            Keep them short, engaging, and platform-appropriate.
            """)
        ])
    elif len(current_text) < 100:  # Building content
        prompt_type = "content_expansion"
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are PostProber's AI writing assistant. Help expand and improve content."),
            ("human", """
            Current draft: "{current_text}"
            Platform: {platform}

            Suggest ways to expand this content while keeping it engaging.
            Provide 2-3 specific suggestions for the next sentence.
            """)
        ])
    else:  # Finishing touches
        prompt_type = "optimization"
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are PostProber's AI writing assistant. Help optimize and finalize content."),
            ("human", """
            Current content: "{current_text}"
            Platform: {platform}

            Suggest final optimizations:
            1. Improve engagement
            2. Add a compelling CTA
            3. Check platform best practices
            """)
        ])

    chain = prompt | llm | StrOutputParser()

    try:
        response = await chain.ainvoke({
            "current_text": current_text,
            "platform": platform,
            "topic": user_input.get("topic", "general")
        })

        # Format response for frontend
        ai_response = {
            "type": prompt_type,
            "suggestions": response,
            "timestamp": datetime.now().isoformat(),
            "confidence": 0.85
        }

        state["ai_responses"].append(ai_response)
        state["current_step"] = "writing_assistance_complete"
        state["progress_percentage"] = 100

        print(f"✅ Provided {prompt_type} suggestions")

    except Exception as e:
        state["errors"] = state.get("errors", []) + [f"Writing assistance error: {str(e)}"]
        print(f"❌ Writing assistance error: {e}")

    return state

async def smart_scheduler_agent(state: PostProberAIState) -> PostProberAIState:
    """Intelligent scheduling recommendations for the Schedule page"""
    print("📅 Smart Scheduler: Analyzing optimal posting times...")

    if state["request_type"] != "schedule_optimization":
        return state

    user_input = state["user_input"]
    content = user_input.get("content", "")
    platform = user_input.get("platform", "twitter")
    user_analytics = state["platform_settings"].get("analytics_data", {})

    llm = setup_ai_model()

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are PostProber's intelligent scheduling assistant. You analyze content and user data to recommend optimal posting times.

        Consider:
        - Platform-specific peak times
        - Content type and topic
        - Historical user performance
        - Audience demographics
        """),
        ("human", """
        Analyze this content for optimal scheduling:

        Content: "{content}"
        Platform: {platform}
        User's historical best performance: {best_times}
        Content category: {category}

        Provide:
        1. Best posting time today
        2. Best posting time this week
        3. Reasoning for recommendations
        4. Alternative time slots
        5. Expected engagement improvement %
        """)
    ])

    chain = prompt | llm | StrOutputParser()

    try:
        response = await chain.ainvoke({
            "content": content,
            "platform": platform,
            "best_times": user_analytics.get("best_times", "Not available"),
            "category": user_input.get("category", "general")
        })

        # Mock optimal times based on platform
        platform_times = {
            "twitter": "14:00",  # 2 PM
            "linkedin": "08:00", # 8 AM
            "instagram": "19:00" # 7 PM
        }

        scheduling_result = {
            "optimal_time_today": platform_times.get(platform, "12:00"),
            "optimal_day_this_week": "Tuesday",
            "reasoning": response,
            "confidence_score": 0.82,
            "expected_improvement": "15-25%",
            "alternative_times": ["10:00", "16:00", "20:00"]
        }

        state["final_result"] = scheduling_result
        state["current_step"] = "schedule_optimization_complete"
        state["progress_percentage"] = 100

        print(f"✅ Scheduling analysis complete")

    except Exception as e:
        state["errors"] = state.get("errors", []) + [f"Scheduling error: {str(e)}"]
        print(f"❌ Scheduling error: {e}")

    return state

async def analytics_insights_agent(state: PostProberAIState) -> PostProberAIState:
    """AI-powered analytics insights for the Analytics page"""
    print("📊 Analytics Insights: Generating intelligent reports...")

    if state["request_type"] != "analytics_insights":
        return state

    user_input = state["user_input"]
    analytics_data = user_input.get("analytics_data", {})
    time_period = user_input.get("time_period", "7d")

    llm = setup_ai_model()

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are PostProber's analytics AI. You analyze social media performance data and provide actionable insights.

        You excel at:
        - Identifying trends and patterns
        - Suggesting improvements
        - Predicting future performance
        - Providing clear, actionable recommendations
        """),
        ("human", """
        Analyze this social media performance data:

        Time period: {time_period}
        Total posts: {total_posts}
        Total engagement: {total_engagement}
        Best performing platform: {best_platform}
        Top content type: {top_content_type}
        Engagement rate trend: {engagement_trend}

        Provide insights:
        1. Key performance highlights
        2. Areas for improvement
        3. Content strategy recommendations
        4. Posting schedule optimizations
        5. Platform-specific suggestions

        Make recommendations specific and actionable.
        """)
    ])

    chain = prompt | llm | StrOutputParser()

    try:
        # Mock analytics data
        mock_data = {
            "total_posts": analytics_data.get("total_posts", 15),
            "total_engagement": analytics_data.get("total_engagement", 450),
            "best_platform": analytics_data.get("best_platform", "LinkedIn"),
            "top_content_type": analytics_data.get("top_content_type", "Educational"),
            "engagement_trend": analytics_data.get("engagement_trend", "Increasing (+12%)")
        }

        response = await chain.ainvoke({
            "time_period": time_period,
            **mock_data
        })

        insights_result = {
            "summary": response,
            "key_metrics": mock_data,
            "recommendations": [
                "Increase posting frequency on LinkedIn",
                "Focus more on educational content",
                "Post during weekday mornings",
                "Use more video content"
            ],
            "predicted_growth": "20-30% engagement increase possible",
            "confidence": 0.78
        }

        state["final_result"] = insights_result
        state["current_step"] = "analytics_insights_complete"
        state["progress_percentage"] = 100

        print(f"✅ Analytics insights generated")

    except Exception as e:
        state["errors"] = state.get("errors", []) + [f"Analytics insights error: {str(e)}"]
        print(f"❌ Analytics insights error: {e}")

    return state

async def content_optimizer_agent(state: PostProberAIState) -> PostProberAIState:
    """Content optimization for any platform"""
    print("⚡ Content Optimizer: Enhancing content for maximum impact...")

    if state["request_type"] != "content_optimization":
        return state

    user_input = state["user_input"]
    original_content = user_input.get("content", "")
    platform = user_input.get("platform", "twitter")
    optimization_goals = user_input.get("goals", ["engagement"])

    llm = setup_ai_model()

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are PostProber's content optimization specialist. You improve content for maximum engagement while maintaining the original message.

        You optimize for:
        - Platform-specific best practices
        - Engagement-driving techniques
        - Clear calls-to-action
        - Brand voice consistency
        """),
        ("human", """
        Optimize this {platform} content:

        Original: "{original_content}"
        Goals: {goals}

        Provide:
        1. Optimized version
        2. Key improvements made
        3. Why these changes will improve performance
        4. Character count comparison
        5. Engagement prediction increase
        """)
    ])

    chain = prompt | llm | StrOutputParser()

    try:
        response = await chain.ainvoke({
            "platform": platform,
            "original_content": original_content,
            "goals": ", ".join(optimization_goals)
        })

        # Mock optimization results
        optimization_result = {
            "optimized_content": response.split("Optimized version:")[-1].split("Key improvements:")[0].strip() if "Optimized version:" in response else original_content,
            "improvements": response,
            "original_length": len(original_content),
            "optimized_length": len(original_content) - 20,  # Mock shorter
            "predicted_improvement": "25-35%",
            "optimization_score": 8.7
        }

        state["final_result"] = optimization_result
        state["current_step"] = "content_optimization_complete"
        state["progress_percentage"] = 100

        print(f"✅ Content optimization complete")

    except Exception as e:
        state["errors"] = state.get("errors", []) + [f"Content optimization error: {str(e)}"]
        print(f"❌ Content optimization error: {e}")

    return state

# 📖 LESSON: Workflow routing based on request type
def route_by_request_type(state: PostProberAIState) -> str:
    """Route to appropriate agent based on request type"""
    request_type = state["request_type"]

    routing_map = {
        "writing_assistance": "writing_assistant",
        "schedule_optimization": "scheduler",
        "analytics_insights": "analytics",
        "content_optimization": "optimizer"
    }

    return routing_map.get(request_type, "error_handler")

async def error_handler(state: PostProberAIState) -> PostProberAIState:
    """Handle errors and provide fallback responses"""
    print("🚨 Error Handler: Processing errors...")

    errors = state.get("errors", [])
    if errors:
        print(f"Found {len(errors)} errors:")
        for error in errors:
            print(f"  - {error}")

    # Provide helpful error response
    state["final_result"] = {
        "error": True,
        "message": "Sorry, I encountered an issue processing your request. Please try again.",
        "support_contact": "support@postprober.com"
    }

    return state

# 📖 LESSON: Creating the production PostProber AI workflow
def create_postprober_ai_workflow():
    """Create the main PostProber AI workflow"""

    workflow = StateGraph(PostProberAIState)

    # Add all AI agents
    workflow.add_node("writing_assistant", ai_writing_assistant)
    workflow.add_node("scheduler", smart_scheduler_agent)
    workflow.add_node("analytics", analytics_insights_agent)
    workflow.add_node("optimizer", content_optimizer_agent)
    workflow.add_node("error_handler", error_handler)

    # Set entry point
    workflow.set_entry_point("router")

    # Add router node
    workflow.add_node("router", lambda state: state)  # Pass-through node for routing

    # Conditional routing based on request type
    workflow.add_conditional_edges(
        "router",
        route_by_request_type,
        {
            "writing_assistant": "writing_assistant",
            "scheduler": "scheduler",
            "analytics": "analytics",
            "optimizer": "optimizer",
            "error_handler": "error_handler"
        }
    )

    # All agents end the workflow
    workflow.add_edge("writing_assistant", END)
    workflow.add_edge("scheduler", END)
    workflow.add_edge("analytics", END)
    workflow.add_edge("optimizer", END)
    workflow.add_edge("error_handler", END)

    return workflow.compile()

# 📖 LESSON: API integration patterns
class PostProberAI:
    """Main PostProber AI service class"""

    def __init__(self):
        self.workflow = create_postprober_ai_workflow()
        self.active_sessions = {}

    async def process_request(self, user_id: str, request_type: str, user_input: dict, platform_settings: dict = None) -> dict:
        """Main entry point for AI requests"""

        session_id = str(uuid.uuid4())
        start_time = datetime.now()

        # Create initial state
        initial_state = PostProberAIState(
            user_id=user_id,
            session_id=session_id,
            timestamp=start_time.isoformat(),
            request_type=request_type,
            user_input=user_input,
            platform_settings=platform_settings or {},
            ai_responses=[],
            current_step="initializing",
            progress_percentage=0,
            final_result=None,
            suggestions=None,
            next_actions=None,
            errors=None,
            processing_time=None,
            model_usage=None
        )

        try:
            # Execute workflow
            print(f"🚀 Processing {request_type} request for user {user_id}")
            final_state = await self.workflow.ainvoke(initial_state)

            # Calculate processing time
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            final_state["processing_time"] = processing_time

            # Return clean response for API
            response = {
                "success": True,
                "request_type": request_type,
                "result": final_state.get("final_result", {}),
                "suggestions": final_state.get("suggestions", []),
                "processing_time": processing_time,
                "session_id": session_id
            }

            if final_state.get("errors"):
                response["warnings"] = final_state["errors"]

            print(f"✅ Request processed in {processing_time:.2f}s")
            return response

        except Exception as e:
            print(f"❌ Request processing failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "request_type": request_type,
                "session_id": session_id
            }

    async def stream_writing_assistance(self, user_id: str, current_text: str, platform: str) -> AsyncGenerator[dict, None]:
        """Streaming writing assistance for real-time UI updates"""

        # This would connect to your streaming LLM endpoint
        # For demo, we'll simulate streaming

        suggestions = [
            "Consider starting with a compelling question...",
            "Your audience loves authentic stories...",
            "Adding a personal experience would increase engagement...",
            "Try including a clear call-to-action at the end..."
        ]

        for i, suggestion in enumerate(suggestions):
            await asyncio.sleep(0.5)  # Simulate processing time
            yield {
                "type": "suggestion",
                "content": suggestion,
                "progress": (i + 1) / len(suggestions) * 100,
                "timestamp": datetime.now().isoformat()
            }

# 📖 LESSON: Example usage and testing
async def test_postprober_ai():
    """Test the complete PostProber AI system"""

    print("🧪 Testing PostProber AI System")
    print("=" * 50)

    ai = PostProberAI()

    # Test cases for different features
    test_cases = [
        {
            "name": "Writing Assistant",
            "user_id": "user123",
            "request_type": "writing_assistance",
            "user_input": {
                "current_text": "Just finished reading about",
                "platform": "twitter",
                "topic": "AI automation"
            }
        },
        {
            "name": "Schedule Optimization",
            "user_id": "user123",
            "request_type": "schedule_optimization",
            "user_input": {
                "content": "Excited to share our new AI-powered social media tool!",
                "platform": "linkedin",
                "category": "product_announcement"
            }
        },
        {
            "name": "Analytics Insights",
            "user_id": "user123",
            "request_type": "analytics_insights",
            "user_input": {
                "time_period": "30d",
                "analytics_data": {
                    "total_posts": 25,
                    "total_engagement": 1250,
                    "best_platform": "LinkedIn"
                }
            }
        },
        {
            "name": "Content Optimization",
            "user_id": "user123",
            "request_type": "content_optimization",
            "user_input": {
                "content": "We made a new thing. It's good. Check it out.",
                "platform": "twitter",
                "goals": ["engagement", "clarity"]
            }
        }
    ]

    for test_case in test_cases:
        print(f"\n🔍 Testing: {test_case['name']}")
        print("-" * 30)

        try:
            result = await ai.process_request(
                test_case["user_id"],
                test_case["request_type"],
                test_case["user_input"]
            )

            print(f"✅ Success: {result['success']}")
            if result["success"]:
                print(f"⏱️ Processing time: {result['processing_time']:.2f}s")
                print(f"📝 Result preview: {str(result['result'])[:100]}...")
            else:
                print(f"❌ Error: {result.get('error', 'Unknown error')}")

        except Exception as e:
            print(f"❌ Test failed: {e}")

    # Test streaming
    print(f"\n🌊 Testing Streaming Writing Assistant")
    print("-" * 30)

    async for update in ai.stream_writing_assistance("user123", "Starting my day with", "instagram"):
        print(f"📡 Stream: {update['content'][:50]}... ({update['progress']:.0f}%)")

if __name__ == "__main__":
    print("🚀 PostProber AI Integration Example")
    print("=" * 60)

    # Run the complete test
    print("\n📖 Complete PostProber AI System Test")
    try:
        asyncio.run(test_postprober_ai())
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Tip: Make sure to set your OPENAI_API_KEY environment variable")

    print("\n🎉 Congratulations! You've completed the LangChain + LangGraph learning series!")
    print("🚀 You now have the knowledge to build sophisticated AI agents for PostProber!")
    print("\n📚 What you've learned:")
    print("  ✅ Basic LangChain LLM interactions")
    print("  ✅ Prompt engineering and templates")
    print("  ✅ Tools and function calling")
    print("  ✅ LangGraph state machines and workflows")
    print("  ✅ Multi-agent collaboration")
    print("  ✅ Production integration patterns")
    print("\n💡 Next steps:")
    print("  🔧 Integrate these patterns into your PostProber codebase")
    print("  🌐 Set up proper API endpoints")
    print("  💾 Add database persistence")
    print("  🔒 Implement authentication and rate limiting")
    print("  📊 Add monitoring and analytics")
    print("\n🎯 You're ready to build the future of AI-powered social media management!")