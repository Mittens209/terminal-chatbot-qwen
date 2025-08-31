# Simple Terminal Chatbot with OpenRouter API

This is a Python-based terminal chatbot that uses the OpenRouter API to access various AI models from your terminal.

## Features

- Simple, clean terminal interface
- Access to multiple AI models through OpenRouter
- Change models on the fly
- Conversation history maintained during the session

## Requirements

- Python 3.6 or higher
- `requests` library

## Setup

1. **Install dependencies:**

   ```bash
   pip install requests
   ```

2. **Get an OpenRouter API key:**

   - Visit [OpenRouter](https://openrouter.ai/keys) to create an account and get your API key.

3. **Set your API key:**

   - Windows PowerShell:
     ```powershell
     $env:OPENROUTER_API_KEY="your-api-key-here"
     ```

   - Windows CMD:
     ```cmd
     set OPENROUTER_API_KEY=your-api-key-here
     ```

   - macOS/Linux:
     ```bash
     export OPENROUTER_API_KEY="your-api-key-here"
     ```

   Alternatively, you can enter your API key when prompted by the program.

## Usage

1. **Run the script:**

   ```bash
   python simple_chatbot.py
   ```

2. **Chat commands:**

   - Type your message and press Enter to chat
   - Type `exit` to quit the program
   - Type `model:model_name` to change the AI model (e.g., `model:openai/gpt-4o-mini`)

## Available Models

The default model is `openrouter/auto`, which lets OpenRouter select the best available model. Other options include:

- `openai/gpt-4o-mini` - GPT-4o Mini model
- `meta-llama/llama-3.1-8b-instruct` - Llama 3.1 8B model
- `qwen/qwen-2.5-7b-instruct` - Qwen 2.5 7B Instruct model
- `google/gemini-flash-1.5` - Google Gemini Flash 1.5
- Many more available on OpenRouter

## Notes

- Some models may not be available depending on your OpenRouter subscription
- The free tier has certain rate limits and model restrictions
