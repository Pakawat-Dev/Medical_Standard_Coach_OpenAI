# Medical_Standard_Coach_OpenAI
A multi-agent AI system that provides expert guidance on medical device standards compliance. This tool helps medical device professionals navigate complex ISO standards and regulatory requirements.
## What This Tool Does

ZenTH ISO Standards Coach is an intelligent assistant that specializes in:
- **ISO 13485:2016** - Quality Management Systems for medical devices
- **IEC 62304:2006+A1:2015** - Medical device software lifecycle processes  
- **IEC 82304-1:2016** - Health software standards
- **ISO 14971:2019** - Risk management for medical devices

The system uses multiple AI agents working together to provide comprehensive, accurate compliance guidance.

## Prerequisites

Before you can run this application, you need:

1. **Python 3.8 or higher** installed on your computer
2. **OpenAI API key** (you'll need to sign up at https://openai.com)
3. Basic familiarity with command line/terminal

## Step-by-Step Setup Guide

### Step 1: Clone or Download the Project
If you received this as a zip file, extract it to a folder on your computer.

### Step 2: Set Up Python Environment
Open your terminal/command prompt and navigate to the project folder:

```bash
# Navigate to the project directory
cd path/to/zenth-iso-coach

# Create a virtual environment (recommended)
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate
```

### Step 3: Install Required Packages
Install all the necessary Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- `autogen` - The core multi-agent framework
- `autogen-agentchat` - Chat functionality for agents
- `autogen-ext[openai]` - OpenAI integration
- `python-dotenv` - Environment variable management

### Step 4: Set Up Your OpenAI API Key
1. Create a file named `.env` in the project folder (if it doesn't exist)
2. Add your OpenAI API key to the file:

```
OPENAI_API_KEY=your_api_key_here
```

**Important**: Replace `your_api_key_here` with your actual OpenAI API key.

### Step 5: Run the Application
Start the ZenTH ISO Standards Coach:

```bash
python main.py
```

## How to Use the Application

### Interactive Mode (Default)
When you run the application, it starts in interactive mode where you can ask multiple questions:

1. The application will display a welcome message
2. Type your question about medical device standards
3. Press Enter and wait for the AI agents to provide guidance
4. Ask follow-up questions or new questions
5. Type `quit`, `exit`, `q`, or `bye` to exit

### Single Query Mode
You can also run a single question by setting an environment variable:

```bash
# Windows
set SINGLE_QUERY="How do I classify software according to IEC 62304?"
python main.py

# Mac/Linux
SINGLE_QUERY="How do I classify software according to IEC 62304?" python main.py
```

## Example Questions You Can Ask

Here are some examples of questions the system can help with:

- "What are the requirements for software safety classification in IEC 62304?"
- "How do I implement risk management according to ISO 14971?"
- "What documentation is required for ISO 13485 compliance?"
- "How should I handle SOUP (Software of Unknown Provenance) in my medical device?"
- "What are the key differences between Class A, B, and C software?"
- "How do I perform a gap analysis for EU MDR compliance?"

## How the Multi-Agent System Works

The application uses three specialized AI agents:

1. **ZenTH ISO Standards Coach** - The main expert that provides initial guidance
2. **Compliance Reviewer** - Reviews the guidance for accuracy and completeness
3. **Documentation Formatter** - Formats the final response in a professional, audit-ready format

These agents work together to ensure you get comprehensive, accurate, and well-formatted compliance guidance.

## Important Safety Notes

⚠️ **This tool is for compliance guidance only**
- It does NOT provide medical advice or clinical guidance
- It does NOT provide device operation instructions
- Always consult qualified medical professionals for clinical matters
- Verify all guidance with your organization's approved procedures

## Troubleshooting

### Common Issues and Solutions

**Error: "OPENAI_API_KEY environment variable not set"**
- Make sure you created the `.env` file with your API key
- Check that the API key is correct and active

**Error: "Module not found"**
- Make sure you activated your virtual environment
- Run `pip install -r requirements.txt` again

**Application runs but gives poor responses**
- Check your internet connection
- Verify your OpenAI API key has sufficient credits
- Try rephrasing your question more specifically

**Application seems slow**
- This is normal - the multi-agent system takes time to provide thorough analysis
- Complex questions may take 30-60 seconds to process

## Project Structure

```
zenth-iso-coach/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── .env                # Your API key (create this)
├── .venv/              # Virtual environment (created by you)
└── README.md           # This file
```

## Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Ensure all prerequisites are met
3. Verify your `.env` file is set up correctly
4. Make sure your virtual environment is activated

## License and Disclaimer

This tool is designed to assist with medical device compliance but should not replace professional regulatory consulting or legal advice. Always verify guidance with qualified regulatory professionals and your organization's approved procedures.
