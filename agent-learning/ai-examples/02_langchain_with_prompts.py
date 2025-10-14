"""
🎯 LESSON 2: LangChain with Prompt Templates

This example teaches you about prompt templates:
- Why templates are better than string formatting
- How to create reusable prompts
- How to handle different input variables
- Best practices for prompt engineering

Key Concepts:
- PromptTemplate: Reusable prompt structures
- Variables: Dynamic parts of your prompts
- Chains: Connecting prompts with LLMs
- Output parsing: Structuring AI responses
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda
import os
from dotenv import load_dotenv

# Load environment variables from PostProber .env file
load_dotenv(dotenv_path="../../.env")

def setup_ai_model():
    """Set up the AI model (same as lesson 1)"""
    return ChatOpenAI(
        model="gpt-4.1",
        temperature=0.9,
        max_tokens=500
    )

# 📖 LESSON: Creating your first prompt template
def basic_prompt_template():
    """Learn how to create and use prompt templates"""

    llm = setup_ai_model()

    # Instead of manually formatting strings, use PromptTemplate
    template = """
    You are a social media expert helping with content creation.

    Task: Create a {platform} post about {topic}
    Tone: {tone}
    Target audience: {audience}

    Requirements:
    - Keep it under {char_limit} characters
    - Include relevant hashtags
    - Make it engaging and actionable

    Post:
    """

    # Create the prompt template
    prompt = PromptTemplate(
        input_variables=["platform", "topic", "tone", "audience", "char_limit"],
        template=template
    )

    # Example inputs
    inputs = {
        "platform": "LinkedIn",
        "topic": "remote work productivity",
        "tone": "professional but friendly",
        "audience": "working professionals",
        "char_limit": "300"
    }

    # Format the prompt with your inputs
    formatted_prompt = prompt.format(**inputs)
    print("📝 Formatted Prompt:")
    print(formatted_prompt)
    print("\n" + "="*50 + "\n")

    # Get AI response
    response = llm.invoke(formatted_prompt)
    print("🤖 AI Response:")
    print(response.content)

# 📖 LESSON: Chat templates (better for conversations)
def chat_prompt_template():
    """Learn about chat templates for more natural conversations"""

    llm = setup_ai_model()

    # Chat templates support system/user/assistant messages
    chat_template = ChatPromptTemplate.from_messages([
        ("system", "You are PostProber AI, an expert social media assistant. You help users create engaging content for {platform}."),
        ("human", "I want to create a post about {topic}. My brand voice is {brand_voice}. Please suggest a post and explain why it would work well."),
    ])

    # Create inputs
    inputs = {
        "platform": "Twitter",
        "topic": "sustainable fashion",
        "brand_voice": "eco-conscious and inspiring"
    }

    # Create the chain: template -> llm -> output parser
    chain = chat_template | llm | StrOutputParser()

    # Run the chain
    response = chain.invoke(inputs)

    print("🎯 Chat Template Result:")
    print(response)

# 📖 LESSON: Multiple prompt templates for different tasks
def postprober_prompt_library():
    """Create a library of prompt templates for different PostProber features"""

    llm = setup_ai_model()

    # Template 1: Content Creation
    content_creation_template = ChatPromptTemplate.from_messages([
        ("system", "You are a content creation expert. Create engaging social media posts."),
        ("human", """
        Create a {platform} post about: {topic}
        Brand voice: {brand_voice}
        Call-to-action: {cta}
        Include: {special_requirements}
        """),
    ])

    # Template 2: Hashtag Generation
    hashtag_template = ChatPromptTemplate.from_messages([
        ("system", "You are a hashtag expert. Generate relevant, trending hashtags."),
        ("human", """
        Generate 5-8 hashtags for this {platform} post:
        "{post_content}"

        Target audience: {audience}
        Industry: {industry}

        Mix of:
        - 2-3 popular hashtags (high volume)
        - 3-4 niche hashtags (targeted)
        - 1-2 branded hashtags
        """),
    ])

    # Template 3: Post Optimization
    optimization_template = ChatPromptTemplate.from_messages([
        ("system", "You are a social media optimization expert. Improve posts for better engagement."),
        ("human", """
        Original post: "{original_post}"
        Platform: {platform}
        Issues: {issues}

        Please provide:
        1. Improved version
        2. Explanation of changes
        3. Expected engagement improvement
        """),
    ])

    # Example usage of each template
    print("📚 PostProber Prompt Library Examples:")
    print("="*50)

    # Example 1: Content Creation
    content_chain = content_creation_template | llm | StrOutputParser()
    content_result = content_chain.invoke({
        "platform": "Instagram",
        "topic": "morning coffee routine",
        "brand_voice": "cozy and authentic",
        "cta": "share your routine in comments",
        "special_requirements": "mention our new coffee blend"
    })

    print("\n📝 Content Creation Example:")
    print(content_result)

    # Example 2: Hashtag Generation
    hashtag_chain = hashtag_template | llm | StrOutputParser()
    hashtag_result = hashtag_chain.invoke({
        "platform": "Instagram",
        "post_content": "Starting my day with the perfect cup of coffee ☕ Our new Morning Blend is everything I needed!",
        "audience": "coffee enthusiasts and lifestyle bloggers",
        "industry": "coffee/beverage"
    })

    print("\n🏷️ Hashtag Generation Example:")
    print(hashtag_result)

# 📖 LESSON: Advanced prompt techniques
def advanced_prompt_techniques():
    """Learn advanced prompting techniques for better results"""

    llm = setup_ai_model()

    # Technique 1: Few-shot prompting (giving examples)
    few_shot_template = ChatPromptTemplate.from_messages([
        ("system", "You are a social media expert. Create posts in the style of the examples."),
        ("human", """
        Here are examples of our brand voice:

        Example 1: "Just dropped our latest feature! 🚀 It's like having a personal assistant for your social media. Who's ready to save 2 hours a day? #ProductivityHack"

        Example 2: "Plot twist: The best social media strategy isn't posting more, it's posting smarter 🧠 Quality > Quantity, always. #SocialMediaTips"

        Now create a similar post about: {topic}
        """),
    ])

    # Technique 2: Chain of thought prompting
    chain_of_thought_template = ChatPromptTemplate.from_messages([
        ("system", "You are a strategic social media planner. Think step by step."),
        ("human", """
        I need to create a {platform} post about {topic}.

        Please think through this step by step:
        1. What's the main goal of this post?
        2. Who is the target audience?
        3. What emotions should it evoke?
        4. What action should readers take?
        5. How can we make it platform-specific?

        Then create the post based on your analysis.
        """),
    ])

    # Test the techniques
    print("🧠 Advanced Prompt Techniques:")
    print("="*50)

    # Few-shot example
    few_shot_chain = few_shot_template | llm | StrOutputParser()
    few_shot_result = few_shot_chain.invoke({
        "topic": "time management for entrepreneurs"
    })

    print("\n🎯 Few-shot Learning Example:")
    print(few_shot_result)

    # Chain of thought example
    cot_chain = chain_of_thought_template | llm | StrOutputParser()
    cot_result = cot_chain.invoke({
        "platform": "LinkedIn",
        "topic": "the importance of work-life balance"
    })

    print("\n🧠 Chain of Thought Example:")
    print(cot_result)

if __name__ == "__main__":
    print("🚀 Welcome to LangChain Prompt Templates!")
    print("=" * 50)

    # Uncomment these examples one by one to learn:

    # Example 1: Basic prompt template
    print("\n📖 Example 1: Basic Prompt Template")
    try:
        basic_prompt_template()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Tip: API key is loaded from PostProber .env file automatically")

    # Example 2: Chat templates
    print("\n📖 Example 2: Chat Prompt Template")
    chat_prompt_template()

    # Example 3: PostProber prompt library
    print("\n📖 Example 3: PostProber Prompt Library")
    postprober_prompt_library()

    # Example 4: Advanced techniques
    print("\n📖 Example 4: Advanced Prompt Techniques")
    advanced_prompt_techniques()

    print("\n🎉 Excellent! You now understand prompt templates!")
    print("📚 Next: Check out 03_langchain_with_tools.py to learn about function calling")