# Terminal Chatbot with OpenRouter API

A simple terminal-based chatbot that connects to various AI models through OpenRouter's API.

## Setup Instructions

1. **Install required packages**:
   ```
   pip install requests python-dotenv
   ```

2. **Set up your API key**:
   - Copy the `.env.example` file to `.env`:
     ```
     copy .env.example .env
     ```
   - Edit the `.env` file and add your OpenRouter API key:
     ```
     OPENROUTER_API_KEY=your_api_key_here
     ```
   - You can get an API key from [OpenRouter](https://openrouter.ai/keys)

3. **Run the chatbot**:
   ```
   python simple_chatbot.py
   ```

## Features

- 💬 Chat with various AI models from your terminal
- 🔄 Switch between models during chat with `model:model_name` command
- 🔑 Securely store your API key in a .env file
- 🎨 Colorful terminal interface

## Available Commands

- Type messages and press Enter to chat with the AI
- Type `exit`, `quit`, or `bye` to exit the program
- Type `model:model_name` to change the AI model on the fly
  - Example: `model:openai/gpt-4o-mini` or `model:meta-llama/llama-3.1-8b-instruct`

## Available Models

The default model is `openrouter/auto` (OpenRouter will select the best model). 
Other popular options include:

- `openai/gpt-4o-mini` - GPT-4o Mini model
- `meta-llama/llama-3.1-8b-instruct` - Llama 3.1 8B model
- `qwen/qwen-2.5-7b-instruct` - Qwen 2.5 7B Instruct model
- `google/gemini-flash-1.5` - Google Gemini Flash 1.5
- Many more available on OpenRouter

## Notes

- Some models may require paid access through OpenRouter
- Free tier has rate limits
