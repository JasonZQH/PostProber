"""
🎯 LESSON 1: Basic LangChain - Your First AI Call

This example shows the absolute basics of LangChain:
- How to set up an LLM (Large Language Model)
- How to make a simple AI call
- How to get a response

Key Concepts:
- LLM: The AI model that generates text
- Invoke: The method to call the AI
- Response: What the AI sends back
"""

from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path="../../.env")

# 📖 LESSON: Setting up your AI model
# ChatOpenAI is the interface to GPT models
def setup_ai_model():
    """Set up the AI model with your API key"""

    # API key is automatically loaded from .env file
    # PostProber .env file already contains: OPENAI_API_KEY=sk-proj-...
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found! Make sure OPENAI_API_KEY is set in your .env file")

    llm = ChatOpenAI(
        model="gpt-4.1",  # The AI model to use
        temperature=0.9,        # How creative (0 = precise, 1 = creative)
        max_tokens=500         # Maximum response length
    )

    return llm

# 📖 LESSON: Making your first AI call
def basic_ai_call():
    """Make a simple call to the AI"""

    # Set up the model
    llm = setup_ai_model()

    # Your question/prompt
    prompt = "Write a fun tweet about coffee in under 280 characters"

    # Call the AI and get response
    response = llm.invoke(prompt)

    print("🤖 AI Response:")
    print(response.content)
    print(f"\n📊 Response length: {len(response.content)} characters")

# 📖 LESSON: Understanding different types of prompts
def different_prompt_examples():
    """Try different types of prompts to see how AI responds"""

    llm = setup_ai_model()

    prompts = [
        "Write a professional LinkedIn post about social media strategy",
        "Create 3 hashtags for a post about healthy eating",
        "Rewrite this tweet to be more engaging: 'We launched a new feature'",
        "What's the best time to post on Instagram for maximum engagement?"
    ]

    for i, prompt in enumerate(prompts, 1):
        print(f"\n--- Example {i} ---")
        print(f"📝 Prompt: {prompt}")

        response = llm.invoke(prompt)
        print(f"🤖 Response: {response.content}")
        print("-" * 50)

# 📖 LESSON: PostProber context
def postprober_content_helper():
    """Example of how this could help with PostProber content creation"""

    llm = setup_ai_model()

    # Simulating a PostProber user request
    user_topic = "launching a new mobile app"
    user_target_platform = "Twitter"

    prompt = f"""
    Help me create social media content for {user_target_platform}.

    Topic: {user_topic}
    Platform: {user_target_platform}

    Please provide:
    1. A engaging post text (under 280 characters)
    2. 3-5 relevant hashtags
    3. Best posting time suggestion
    """

    response = llm.invoke(prompt)

    print("🎯 PostProber AI Assistant Result:")
    print(response.content)

if __name__ == "__main__":
    print("🚀 Welcome to LangChain Basics!")
    print("=" * 50)

    # Uncomment these lines one by one to try different examples:

    # Example 1: Basic AI call
    print("\n📖 Example 1: Basic AI Call")
    try:
        basic_ai_call()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Tip: API key is loaded from PostProber .env file automatically")

    # Example 2: Different prompt types
    print("\n📖 Example 2: Different Prompt Types")
    different_prompt_examples()

    # Example 3: PostProber context
    print("\n📖 Example 3: PostProber Content Helper")
    postprober_content_helper()

    print("\n🎉 Great job! You've made your first AI calls!")
    print("📚 Next: Check out 02_langchain_with_prompts.py to learn about prompt templates")