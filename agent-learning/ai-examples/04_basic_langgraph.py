"""
🎯 LESSON 4: Basic LangGraph - State Machines and Workflows

This example introduces LangGraph:
- What is LangGraph and why it's powerful
- Understanding state and state machines
- Creating your first workflow graph
- How nodes and edges work

Key Concepts:
- State: Information that flows through your workflow
- Nodes: Steps in your workflow (functions)
- Edges: Connections between steps
- Graph: The complete workflow structure
- Conditional routing: Making decisions in workflows
"""

from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
import json
import os
from dotenv import load_dotenv

# Load environment variables from PostProber .env file
load_dotenv(dotenv_path="../../.env")

# 📖 LESSON: Defining State - The information that flows through your workflow
class PostCreationState(TypedDict):
    """State for our post creation workflow"""
    # Input from user
    topic: str
    platform: str
    target_audience: str

    # Generated during workflow
    raw_content: Optional[str]
    optimized_content: Optional[str]
    hashtags: Optional[List[str]]
    character_count: Optional[int]
    final_post: Optional[str]

    # Workflow control
    needs_optimization: Optional[bool]
    errors: Optional[List[str]]

def setup_ai_model():
    """Set up the AI model"""
    return ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=500
    )

# 📖 LESSON: Creating workflow nodes (functions that process state)

def generate_content_node(state: PostCreationState) -> PostCreationState:
    """Node 1: Generate initial content based on user input"""
    print(f"📝 Generating content for {state['platform']} about {state['topic']}...")

    llm = setup_ai_model()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a social media content creator. Create engaging posts."),
        ("human", """
        Create a {platform} post about: {topic}
        Target audience: {target_audience}

        Make it engaging and appropriate for the platform.
        Don't include hashtags yet - just the main content.
        """)
    ])

    chain = prompt | llm | StrOutputParser()

    try:
        raw_content = chain.invoke({
            "platform": state["platform"],
            "topic": state["topic"],
            "target_audience": state["target_audience"]
        })

        # Update state with generated content
        state["raw_content"] = raw_content.strip()
        state["character_count"] = len(state["raw_content"])

        print(f"✅ Generated content: {state['raw_content'][:50]}...")

    except Exception as e:
        state["errors"] = state.get("errors", []) + [f"Content generation error: {str(e)}"]
        print(f"❌ Error generating content: {e}")

    return state

def check_optimization_needed_node(state: PostCreationState) -> PostCreationState:
    """Node 2: Check if content needs optimization"""
    print("🔍 Checking if optimization is needed...")

    # Platform character limits
    platform_limits = {
        "twitter": 280,
        "linkedin": 3000,
        "instagram": 2200,
        "facebook": 63206
    }

    limit = platform_limits.get(state["platform"].lower(), 280)
    character_count = state.get("character_count", 0)

    # Determine if optimization is needed
    needs_optimization = character_count > limit

    state["needs_optimization"] = needs_optimization

    if needs_optimization:
        print(f"⚠️ Content too long ({character_count} > {limit} chars) - needs optimization")
    else:
        print(f"✅ Content length OK ({character_count} <= {limit} chars)")

    return state

def optimize_content_node(state: PostCreationState) -> PostCreationState:
    """Node 3: Optimize content if needed"""
    print("⚡ Optimizing content...")

    llm = setup_ai_model()

    platform_limits = {
        "twitter": 280,
        "linkedin": 3000,
        "instagram": 2200,
        "facebook": 63206
    }

    limit = platform_limits.get(state["platform"].lower(), 280)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a social media optimization expert. Make content better and shorter."),
        ("human", """
        Optimize this {platform} post to be under {char_limit} characters while keeping it engaging:

        Original content:
        {original_content}

        Make it:
        - Under {char_limit} characters
        - More engaging and punchy
        - Platform-appropriate
        - Maintain the key message
        """)
    ])

    chain = prompt | llm | StrOutputParser()

    try:
        optimized_content = chain.invoke({
            "platform": state["platform"],
            "char_limit": limit,
            "original_content": state["raw_content"]
        })

        state["optimized_content"] = optimized_content.strip()
        state["character_count"] = len(state["optimized_content"])

        print(f"✅ Optimized content: {state['optimized_content'][:50]}...")

    except Exception as e:
        state["errors"] = state.get("errors", []) + [f"Optimization error: {str(e)}"]
        print(f"❌ Error optimizing content: {e}")

    return state

def generate_hashtags_node(state: PostCreationState) -> PostCreationState:
    """Node 4: Generate hashtags"""
    print("🏷️ Generating hashtags...")

    llm = setup_ai_model()

    # Use optimized content if available, otherwise raw content
    content = state.get("optimized_content") or state.get("raw_content", "")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a hashtag expert. Generate relevant, trending hashtags."),
        ("human", """
        Generate 5-8 relevant hashtags for this {platform} post:
        "{content}"

        Topic: {topic}
        Target audience: {target_audience}

        Return only the hashtags, separated by spaces.
        Mix popular and niche hashtags.
        """)
    ])

    chain = prompt | llm | StrOutputParser()

    try:
        hashtag_text = chain.invoke({
            "platform": state["platform"],
            "content": content,
            "topic": state["topic"],
            "target_audience": state["target_audience"]
        })

        # Parse hashtags
        hashtags = [tag.strip() for tag in hashtag_text.split() if tag.startswith("#")]
        state["hashtags"] = hashtags

        print(f"✅ Generated hashtags: {' '.join(hashtags)}")

    except Exception as e:
        state["errors"] = state.get("errors", []) + [f"Hashtag generation error: {str(e)}"]
        print(f"❌ Error generating hashtags: {e}")

    return state

def finalize_post_node(state: PostCreationState) -> PostCreationState:
    """Node 5: Combine everything into final post"""
    print("🎯 Finalizing post...")

    # Use optimized content if available, otherwise raw content
    content = state.get("optimized_content") or state.get("raw_content", "")
    hashtags = state.get("hashtags", [])

    # Combine content and hashtags
    final_post = content
    if hashtags:
        final_post += "\n\n" + " ".join(hashtags)

    state["final_post"] = final_post
    state["character_count"] = len(final_post)

    print(f"✅ Final post ready ({state['character_count']} characters)")

    return state

# 📖 LESSON: Conditional routing - making decisions in workflows
def should_optimize(state: PostCreationState) -> str:
    """Conditional edge: decide if content needs optimization"""
    if state.get("needs_optimization", False):
        return "optimize"
    else:
        return "skip_optimization"

# 📖 LESSON: Building your first LangGraph workflow
def create_post_creation_workflow():
    """Create a complete post creation workflow using LangGraph"""

    # Create the state graph
    workflow = StateGraph(PostCreationState)

    # Add all nodes to the graph
    workflow.add_node("generate_content", generate_content_node)
    workflow.add_node("check_optimization", check_optimization_needed_node)
    workflow.add_node("optimize_content", optimize_content_node)
    workflow.add_node("generate_hashtags", generate_hashtags_node)
    workflow.add_node("finalize_post", finalize_post_node)

    # Define the workflow edges (flow between nodes)
    workflow.set_entry_point("generate_content")

    # Linear flow: generate -> check -> conditional -> hashtags -> finalize
    workflow.add_edge("generate_content", "check_optimization")

    # Conditional edge: check if optimization is needed
    workflow.add_conditional_edges(
        "check_optimization",
        should_optimize,
        {
            "optimize": "optimize_content",
            "skip_optimization": "generate_hashtags"
        }
    )

    # Continue flow
    workflow.add_edge("optimize_content", "generate_hashtags")
    workflow.add_edge("generate_hashtags", "finalize_post")
    workflow.add_edge("finalize_post", END)

    # Compile the graph
    app = workflow.compile()

    return app

# 📖 LESSON: Running your workflow
def run_workflow_example():
    """Run the post creation workflow with example data"""

    print("🚀 Running PostProber Content Creation Workflow")
    print("=" * 60)

    # Create the workflow
    app = create_post_creation_workflow()

    # Initial state (user input)
    initial_state = PostCreationState(
        topic="productivity tips for remote workers",
        platform="Twitter",
        target_audience="remote professionals and entrepreneurs",
        raw_content=None,
        optimized_content=None,
        hashtags=None,
        character_count=None,
        final_post=None,
        needs_optimization=None,
        errors=None
    )

    print("📥 Input:")
    print(f"  Topic: {initial_state['topic']}")
    print(f"  Platform: {initial_state['platform']}")
    print(f"  Audience: {initial_state['target_audience']}")
    print("\n🔄 Workflow Execution:")

    try:
        # Run the workflow
        final_state = app.invoke(initial_state)

        print("\n🎉 Workflow Complete!")
        print("=" * 60)
        print("📊 Final Results:")
        print(f"  Character count: {final_state.get('character_count', 0)}")
        print(f"  Needed optimization: {final_state.get('needs_optimization', False)}")
        print(f"  Hashtags: {final_state.get('hashtags', [])}")

        if final_state.get('errors'):
            print(f"  ⚠️ Errors: {final_state['errors']}")

        print(f"\n📱 Final Post:")
        print("-" * 40)
        print(final_state.get('final_post', 'No post generated'))
        print("-" * 40)

    except Exception as e:
        print(f"❌ Workflow error: {e}")

# 📖 LESSON: Multiple workflow examples
def run_multiple_examples():
    """Run the workflow with different inputs to see how it adapts"""

    app = create_post_creation_workflow()

    test_cases = [
        {
            "name": "Short Twitter post",
            "state": PostCreationState(
                topic="coffee",
                platform="Twitter",
                target_audience="coffee lovers",
                raw_content=None, optimized_content=None, hashtags=None,
                character_count=None, final_post=None, needs_optimization=None, errors=None
            )
        },
        {
            "name": "Long LinkedIn article",
            "state": PostCreationState(
                topic="leadership strategies for startup founders in 2024 with detailed case studies and actionable insights",
                platform="LinkedIn",
                target_audience="startup founders and business leaders",
                raw_content=None, optimized_content=None, hashtags=None,
                character_count=None, final_post=None, needs_optimization=None, errors=None
            )
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test Case {i}: {test_case['name']}")
        print("=" * 50)

        try:
            result = app.invoke(test_case["state"])
            print(f"✅ Result: {len(result.get('final_post', ''))} characters")
            print(f"📱 Preview: {result.get('final_post', '')[:100]}...")

        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("📊 Welcome to LangGraph - Building AI Workflows!")
    print("=" * 60)

    # Uncomment these examples one by one to learn:

    # Example 1: Single workflow run
    print("\n📖 Example 1: Post Creation Workflow")
    try:
        run_workflow_example()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Tip: Make sure to set your OPENAI_API_KEY environment variable")

    # Example 2: Multiple examples
    print("\n📖 Example 2: Multiple Workflow Examples")
    # run_multiple_examples()

    print("\n🎉 Fantastic! You now understand LangGraph workflows!")
    print("🔄 You've seen how to create complex, multi-step AI processes!")
    print("📚 Next: Check out 05_langgraph_workflow.py for advanced multi-agent workflows")