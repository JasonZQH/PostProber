"""
🎯 LESSON 5: Advanced LangGraph - Multi-Agent Workflows

This example shows advanced LangGraph concepts:
- Multiple specialized agents working together
- Complex decision making and routing
- Agent collaboration and handoffs
- Error handling and recovery
- Real-world PostProber scenarios

Key Concepts:
- Agent roles: Specialized AI agents for different tasks
- Collaboration: Agents working together on complex problems
- State sharing: How agents pass information between each other
- Supervisor patterns: Coordinating multiple agents
- Parallel processing: Running agents simultaneously
"""

from typing import TypedDict, List, Optional, Literal
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.tools import tool
import json
import random
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables from PostProber .env file
load_dotenv(dotenv_path="../../.env")

# 📖 LESSON: Advanced state management for multi-agent workflows
class AdvancedPostState(TypedDict):
    """Enhanced state for multi-agent post creation and optimization"""
    # User inputs
    topic: str
    platform: str
    target_audience: str
    brand_voice: str
    business_goals: List[str]

    # Content creation
    content_variations: Optional[List[str]]
    selected_content: Optional[str]
    optimized_content: Optional[str]

    # Analysis and optimization
    sentiment_analysis: Optional[dict]
    engagement_prediction: Optional[dict]
    competitor_analysis: Optional[dict]
    seo_analysis: Optional[dict]

    # Scheduling and strategy
    optimal_timing: Optional[dict]
    hashtag_strategy: Optional[dict]
    cross_platform_adaptations: Optional[dict]

    # Final outputs
    final_post: Optional[str]
    posting_strategy: Optional[dict]
    performance_predictions: Optional[dict]

    # Workflow control
    current_agent: Optional[str]
    completed_tasks: Optional[List[str]]
    next_tasks: Optional[List[str]]
    errors: Optional[List[str]]
    requires_human_review: Optional[bool]

def setup_ai_model():
    """Set up the AI model"""
    return ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=800
    )

# 📖 LESSON: Specialized agent nodes - each with specific expertise

def content_creator_agent(state: AdvancedPostState) -> AdvancedPostState:
    """Agent 1: Content Creator - Generates multiple content variations"""
    print("👨‍🎨 Content Creator Agent: Generating content variations...")

    llm = setup_ai_model()

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a creative content creator specialist. Your job is to generate multiple engaging variations of social media content.

        You excel at:
        - Understanding brand voice and audience
        - Creating engaging, platform-specific content
        - Generating diverse content styles
        - Crafting compelling hooks and CTAs
        """),
        ("human", """
        Create 3 different content variations for {platform} about: {topic}

        Brand voice: {brand_voice}
        Target audience: {target_audience}
        Business goals: {business_goals}

        For each variation, create a different approach:
        1. Educational/Informative approach
        2. Emotional/Story-driven approach
        3. Direct/Action-oriented approach

        Format each variation clearly and make them distinct.
        """)
    ])

    chain = prompt | llm | StrOutputParser()

    try:
        variations_text = chain.invoke({
            "platform": state["platform"],
            "topic": state["topic"],
            "brand_voice": state["brand_voice"],
            "target_audience": state["target_audience"],
            "business_goals": ", ".join(state["business_goals"])
        })

        # Parse variations (simplified parsing)
        variations = [v.strip() for v in variations_text.split('\n\n') if v.strip()]
        state["content_variations"] = variations[:3]  # Take first 3

        state["completed_tasks"] = state.get("completed_tasks", []) + ["content_creation"]
        print(f"✅ Generated {len(state['content_variations'])} content variations")

    except Exception as e:
        state["errors"] = state.get("errors", []) + [f"Content creation error: {str(e)}"]
        print(f"❌ Content creation error: {e}")

    return state

def strategy_analyst_agent(state: AdvancedPostState) -> AdvancedPostState:
    """Agent 2: Strategy Analyst - Analyzes and selects best content"""
    print("📊 Strategy Analyst Agent: Analyzing content performance potential...")

    llm = setup_ai_model()

    variations = state.get("content_variations", [])
    if not variations:
        state["errors"] = state.get("errors", []) + ["No content variations to analyze"]
        return state

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a social media strategy analyst. You analyze content for engagement potential, brand alignment, and goal achievement.

        You excel at:
        - Predicting content performance
        - Analyzing sentiment and tone
        - Evaluating brand voice consistency
        - Measuring goal alignment
        """),
        ("human", """
        Analyze these {platform} content variations and select the best one:

        Variations:
        {variations}

        Evaluation criteria:
        - Platform: {platform}
        - Target audience: {target_audience}
        - Brand voice: {brand_voice}
        - Business goals: {business_goals}

        For each variation, provide:
        1. Engagement prediction score (1-10)
        2. Brand voice alignment (1-10)
        3. Goal achievement potential (1-10)
        4. Overall recommendation

        Then select the best variation and explain why.
        """)
    ])

    chain = prompt | llm | StrOutputParser()

    try:
        analysis_text = chain.invoke({
            "platform": state["platform"],
            "variations": "\n\n".join([f"Variation {i+1}: {v}" for i, v in enumerate(variations)]),
            "target_audience": state["target_audience"],
            "brand_voice": state["brand_voice"],
            "business_goals": ", ".join(state["business_goals"])
        })

        # Simplified: select first variation for demo
        # In real implementation, would parse the analysis to select best
        state["selected_content"] = variations[0] if variations else ""

        # Mock engagement prediction
        state["engagement_prediction"] = {
            "score": random.uniform(6.5, 9.2),
            "estimated_reach": random.randint(500, 5000),
            "estimated_engagement": random.randint(50, 500),
            "confidence": random.uniform(0.7, 0.95)
        }

        state["completed_tasks"] = state.get("completed_tasks", []) + ["strategy_analysis"]
        print(f"✅ Selected best content variation (predicted score: {state['engagement_prediction']['score']:.1f}/10)")

    except Exception as e:
        state["errors"] = state.get("errors", []) + [f"Strategy analysis error: {str(e)}"]
        print(f"❌ Strategy analysis error: {e}")

    return state

def optimization_agent(state: AdvancedPostState) -> AdvancedPostState:
    """Agent 3: Optimization Specialist - Optimizes content for platform and goals"""
    print("⚡ Optimization Agent: Optimizing content for maximum impact...")

    llm = setup_ai_model()

    selected_content = state.get("selected_content", "")
    if not selected_content:
        state["errors"] = state.get("errors", []) + ["No selected content to optimize"]
        return state

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a social media optimization specialist. You refine content to maximize engagement while maintaining brand voice and achieving business goals.

        You excel at:
        - Platform-specific optimization
        - Character limit management
        - Hook and CTA optimization
        - Engagement-driving techniques
        """),
        ("human", """
        Optimize this {platform} content for maximum engagement:

        Original content:
        {content}

        Optimization requirements:
        - Platform: {platform}
        - Brand voice: {brand_voice}
        - Target audience: {target_audience}
        - Business goals: {business_goals}

        Improve:
        1. Hook/opening (make it irresistible)
        2. Body content (clear, engaging, valuable)
        3. Call-to-action (compelling and specific)
        4. Platform-specific formatting

        Keep the core message but make it more engaging.
        """)
    ])

    chain = prompt | llm | StrOutputParser()

    try:
        optimized_content = chain.invoke({
            "platform": state["platform"],
            "content": selected_content,
            "brand_voice": state["brand_voice"],
            "target_audience": state["target_audience"],
            "business_goals": ", ".join(state["business_goals"])
        })

        state["optimized_content"] = optimized_content.strip()

        state["completed_tasks"] = state.get("completed_tasks", []) + ["optimization"]
        print(f"✅ Content optimized for {state['platform']}")

    except Exception as e:
        state["errors"] = state.get("errors", []) + [f"Optimization error: {str(e)}"]
        print(f"❌ Optimization error: {e}")

    return state

def hashtag_specialist_agent(state: AdvancedPostState) -> AdvancedPostState:
    """Agent 4: Hashtag Specialist - Creates strategic hashtag mix"""
    print("🏷️ Hashtag Specialist Agent: Developing hashtag strategy...")

    llm = setup_ai_model()

    content = state.get("optimized_content") or state.get("selected_content", "")
    if not content:
        state["errors"] = state.get("errors", []) + ["No content available for hashtag analysis"]
        return state

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a hashtag strategy specialist. You create optimal hashtag mixes that balance reach, engagement, and discoverability.

        You excel at:
        - Trending hashtag identification
        - Niche community hashtag selection
        - Hashtag mix optimization
        - Platform-specific hashtag strategies
        """),
        ("human", """
        Create a strategic hashtag mix for this {platform} content:

        Content: {content}
        Topic: {topic}
        Target audience: {target_audience}
        Business goals: {business_goals}

        Create a hashtag strategy with:
        1. 2-3 trending/popular hashtags (high reach)
        2. 3-4 niche/community hashtags (engaged audience)
        3. 1-2 branded hashtags (brand building)

        For each hashtag, explain:
        - Why it's relevant
        - Expected reach/engagement level
        - How it supports business goals

        Return the hashtags and strategy explanation.
        """)
    ])

    chain = prompt | llm | StrOutputParser()

    try:
        hashtag_strategy_text = chain.invoke({
            "platform": state["platform"],
            "content": content,
            "topic": state["topic"],
            "target_audience": state["target_audience"],
            "business_goals": ", ".join(state["business_goals"])
        })

        # Mock hashtag strategy (in real app, would parse the response)
        state["hashtag_strategy"] = {
            "hashtags": ["#SocialMedia", "#ContentCreation", "#MarketingTips", "#BusinessGrowth", "#PostProber"],
            "strategy_explanation": hashtag_strategy_text,
            "reach_potential": "Medium-High",
            "engagement_potential": "High"
        }

        state["completed_tasks"] = state.get("completed_tasks", []) + ["hashtag_strategy"]
        print(f"✅ Hashtag strategy created with {len(state['hashtag_strategy']['hashtags'])} hashtags")

    except Exception as e:
        state["errors"] = state.get("errors", []) + [f"Hashtag strategy error: {str(e)}"]
        print(f"❌ Hashtag strategy error: {e}")

    return state

def timing_specialist_agent(state: AdvancedPostState) -> AdvancedPostState:
    """Agent 5: Timing Specialist - Determines optimal posting schedule"""
    print("⏰ Timing Specialist Agent: Analyzing optimal posting times...")

    llm = setup_ai_model()

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a social media timing specialist. You analyze audience behavior patterns to determine optimal posting times for maximum engagement.

        You excel at:
        - Audience behavior analysis
        - Platform-specific timing optimization
        - Time zone considerations
        - Content type timing strategies
        """),
        ("human", """
        Determine optimal posting times for this {platform} content:

        Content topic: {topic}
        Target audience: {target_audience}
        Business goals: {business_goals}

        Consider:
        1. Platform-specific peak engagement times
        2. Target audience demographics and behavior
        3. Content type and topic relevance
        4. Competition and noise levels

        Provide:
        - Best posting time today
        - Best posting day this week
        - Alternative timing options
        - Reasoning for recommendations
        """)
    ])

    chain = prompt | llm | StrOutputParser()

    try:
        timing_analysis = chain.invoke({
            "platform": state["platform"],
            "topic": state["topic"],
            "target_audience": state["target_audience"],
            "business_goals": ", ".join(state["business_goals"])
        })

        # Mock optimal timing (in real app, would use actual analytics)
        current_time = datetime.now()
        optimal_time = current_time + timedelta(hours=random.randint(1, 8))

        state["optimal_timing"] = {
            "recommended_time": optimal_time.strftime("%Y-%m-%d %H:%M:%S"),
            "reasoning": timing_analysis,
            "confidence_score": random.uniform(0.8, 0.95),
            "alternative_times": [
                (optimal_time + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
                (optimal_time + timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S")
            ]
        }

        state["completed_tasks"] = state.get("completed_tasks", []) + ["timing_analysis"]
        print(f"✅ Optimal posting time determined: {state['optimal_timing']['recommended_time']}")

    except Exception as e:
        state["errors"] = state.get("errors", []) + [f"Timing analysis error: {str(e)}"]
        print(f"❌ Timing analysis error: {e}")

    return state

def final_assembly_agent(state: AdvancedPostState) -> AdvancedPostState:
    """Agent 6: Final Assembly - Combines everything into final post and strategy"""
    print("🎯 Final Assembly Agent: Creating final post and strategy...")

    # Combine optimized content with hashtags
    content = state.get("optimized_content") or state.get("selected_content", "")
    hashtags = state.get("hashtag_strategy", {}).get("hashtags", [])

    if content:
        final_post = content
        if hashtags:
            final_post += "\n\n" + " ".join(hashtags)

        state["final_post"] = final_post

        # Create comprehensive posting strategy
        state["posting_strategy"] = {
            "content": content,
            "hashtags": hashtags,
            "optimal_posting_time": state.get("optimal_timing", {}).get("recommended_time"),
            "predicted_engagement": state.get("engagement_prediction", {}),
            "strategy_notes": "Complete multi-agent optimization applied"
        }

        # Final performance predictions
        state["performance_predictions"] = {
            "engagement_score": state.get("engagement_prediction", {}).get("score", 7.0),
            "reach_estimate": state.get("engagement_prediction", {}).get("estimated_reach", 1000),
            "confidence": state.get("optimal_timing", {}).get("confidence_score", 0.8)
        }

        state["completed_tasks"] = state.get("completed_tasks", []) + ["final_assembly"]
        print(f"✅ Final post assembled ({len(final_post)} characters)")
    else:
        state["errors"] = state.get("errors", []) + ["No content available for final assembly"]
        print("❌ No content available for final assembly")

    return state

# 📖 LESSON: Workflow orchestration and routing
def should_proceed_to_optimization(state: AdvancedPostState) -> str:
    """Conditional routing: proceed only if content analysis was successful"""
    if state.get("selected_content") and not state.get("errors"):
        return "optimize"
    else:
        return "error_handling"

def error_handling_node(state: AdvancedPostState) -> AdvancedPostState:
    """Handle errors and determine recovery strategy"""
    print("🚨 Error Handler: Processing workflow errors...")

    errors = state.get("errors", [])
    if errors:
        print(f"⚠️ Found {len(errors)} errors:")
        for error in errors:
            print(f"  - {error}")

        # Mark for human review if critical errors
        state["requires_human_review"] = True
        print("👤 Marked for human review due to errors")

    return state

# 📖 LESSON: Building complex multi-agent workflows
def create_advanced_postprober_workflow():
    """Create advanced multi-agent PostProber workflow"""

    workflow = StateGraph(AdvancedPostState)

    # Add all specialized agents
    workflow.add_node("content_creator", content_creator_agent)
    workflow.add_node("strategy_analyst", strategy_analyst_agent)
    workflow.add_node("optimization_agent", optimization_agent)
    workflow.add_node("hashtag_specialist", hashtag_specialist_agent)
    workflow.add_node("timing_specialist", timing_specialist_agent)
    workflow.add_node("final_assembly", final_assembly_agent)
    workflow.add_node("error_handler", error_handling_node)

    # Define workflow entry point
    workflow.set_entry_point("content_creator")

    # Linear workflow with conditional branching
    workflow.add_edge("content_creator", "strategy_analyst")

    # Conditional routing after strategy analysis
    workflow.add_conditional_edges(
        "strategy_analyst",
        should_proceed_to_optimization,
        {
            "optimize": "optimization_agent",
            "error_handling": "error_handler"
        }
    )

    # Parallel processing: optimization and hashtag work can happen together
    # For simplicity, we'll do them sequentially
    workflow.add_edge("optimization_agent", "hashtag_specialist")
    workflow.add_edge("hashtag_specialist", "timing_specialist")
    workflow.add_edge("timing_specialist", "final_assembly")

    # End nodes
    workflow.add_edge("final_assembly", END)
    workflow.add_edge("error_handler", END)

    return workflow.compile()

# 📖 LESSON: Running advanced workflows
def run_advanced_workflow():
    """Run the complete multi-agent PostProber workflow"""

    print("🚀 PostProber Advanced Multi-Agent Workflow")
    print("=" * 60)

    app = create_advanced_postprober_workflow()

    # Comprehensive input state
    initial_state = AdvancedPostState(
        topic="AI automation tools for small businesses",
        platform="LinkedIn",
        target_audience="small business owners and entrepreneurs",
        brand_voice="professional yet approachable, expert but not intimidating",
        business_goals=["increase brand awareness", "generate leads", "establish thought leadership"],

        # Initialize all other fields
        content_variations=None, selected_content=None, optimized_content=None,
        sentiment_analysis=None, engagement_prediction=None, competitor_analysis=None, seo_analysis=None,
        optimal_timing=None, hashtag_strategy=None, cross_platform_adaptations=None,
        final_post=None, posting_strategy=None, performance_predictions=None,
        current_agent=None, completed_tasks=None, next_tasks=None, errors=None, requires_human_review=None
    )

    print("📥 Input Configuration:")
    print(f"  Topic: {initial_state['topic']}")
    print(f"  Platform: {initial_state['platform']}")
    print(f"  Audience: {initial_state['target_audience']}")
    print(f"  Brand Voice: {initial_state['brand_voice']}")
    print(f"  Goals: {', '.join(initial_state['business_goals'])}")

    print("\n🔄 Multi-Agent Workflow Execution:")
    print("-" * 40)

    try:
        # Execute the workflow
        final_state = app.invoke(initial_state)

        print("\n🎉 Multi-Agent Workflow Complete!")
        print("=" * 60)

        # Display results
        print("📊 Workflow Results:")
        completed_tasks = final_state.get("completed_tasks", [])
        print(f"  ✅ Completed tasks: {', '.join(completed_tasks)}")

        if final_state.get("errors"):
            print(f"  ⚠️ Errors encountered: {len(final_state['errors'])}")
            for error in final_state['errors']:
                print(f"    - {error}")

        if final_state.get("requires_human_review"):
            print("  👤 Requires human review")

        # Performance predictions
        if final_state.get("performance_predictions"):
            predictions = final_state["performance_predictions"]
            print(f"\n📈 Performance Predictions:")
            print(f"  Engagement Score: {predictions.get('engagement_score', 0):.1f}/10")
            print(f"  Estimated Reach: {predictions.get('reach_estimate', 0):,}")
            print(f"  Confidence: {predictions.get('confidence', 0):.1%}")

        # Posting strategy
        if final_state.get("posting_strategy"):
            strategy = final_state["posting_strategy"]
            print(f"\n⏰ Posting Strategy:")
            print(f"  Optimal Time: {strategy.get('optimal_posting_time', 'Not determined')}")
            print(f"  Hashtags: {len(strategy.get('hashtags', []))} strategic hashtags")

        # Final post
        if final_state.get("final_post"):
            print(f"\n📱 Final Optimized Post:")
            print("-" * 50)
            print(final_state["final_post"])
            print("-" * 50)
            print(f"Character count: {len(final_state['final_post'])}")

    except Exception as e:
        print(f"❌ Workflow execution error: {e}")

if __name__ == "__main__":
    print("🤖 Welcome to Advanced Multi-Agent LangGraph!")
    print("=" * 60)

    # Run the advanced workflow
    print("\n📖 Advanced Multi-Agent PostProber Workflow")
    try:
        run_advanced_workflow()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Tip: Make sure to set your OPENAI_API_KEY environment variable")

    print("\n🎉 Incredible! You've built a sophisticated multi-agent system!")
    print("🚀 This is enterprise-level AI orchestration!")
    print("📚 Next: Check out 06_postprober_example.py for a complete PostProber integration example")