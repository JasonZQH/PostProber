# 🚀 Quick Setup Guide for LangChain + LangGraph Learning

## 📋 Prerequisites

1. **Python 3.8+** installed on your system
2. **OpenAI API key** (get one at https://platform.openai.com/)

## ⚡ Quick Start

### 1. Install Dependencies

```bash
cd src/shared/ai-examples
pip install -r requirements.txt
```

### 2. Set Your API Key

**Option A: Environment Variable (Recommended)**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

**Option B: Create .env file**
```bash
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

### 3. Run Your First Example

```bash
python 01_basic_langchain.py
```

## 📚 Learning Path

Run the examples in order:

```bash
# Level 1: LangChain Basics
python 01_basic_langchain.py
python 02_langchain_with_prompts.py
python 03_langchain_with_tools.py

# Level 2: LangGraph Workflows
python 04_basic_langgraph.py
python 05_langgraph_workflow.py

# Level 3: Real Application
python 06_postprober_example.py
```

## 🔧 Troubleshooting

### Common Issues:

**"Module not found" error:**
```bash
pip install --upgrade langchain langchain-openai langgraph
```

**"API key not found" error:**
- Make sure your OPENAI_API_KEY is set correctly
- Check that you have sufficient API credits

**Rate limit errors:**
- Add delays between requests
- Use a paid OpenAI plan for higher limits

### Getting Help:

1. Check the error messages in each example
2. Read the comments in the code for explanations
3. Start with simpler examples if you're stuck

## 🎯 What's Next?

After completing the learning examples:

1. **Experiment**: Modify the examples with your own prompts
2. **Integrate**: Add AI features to your PostProber app
3. **Scale**: Build production-ready AI workflows
4. **Monitor**: Add logging and error handling

## 💡 Pro Tips

- Start with simple examples before moving to complex workflows
- Always handle errors gracefully in production
- Monitor your API usage and costs
- Test with different prompts to see how AI responds
- Keep your API keys secure and never commit them to git

Happy learning! 🚀