#!/usr/bin/env python3
"""
Simple Terminal Chatbot using OpenRouter API

This script creates a simple terminal-based chat interface that connects to
various AI models through the OpenRouter API.

Requirements:
- Python 3.6+
- requests library (install with: pip install requests)
- python-dotenv library (install with: pip install python-dotenv)

Usage:
1. Create a .env file in the same directory with your OpenRouter API key:
   OPENROUTER_API_KEY=your-api-key-here
   DEFAULT_MODEL=openrouter/auto (optional)
2. Run the script: python simple_chatbot.py

Features:
- Simple terminal interface
- Chat history within the session
- Type 'exit' to quit
- Loads API key from .env file
"""

import os
from dotenv import load_dotenv
import requests
import json
import sys
from pathlib import Path

# ANSI color codes for terminal output
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Load environment variables from .env file
def load_env_file():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        return True
    return False

# Configuration
API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "openrouter/auto"  # Default can be overridden in .env file

def get_api_key():
    """Get API key from environment or .env file"""
    # Try to load from .env file first
    load_env_file()
    
    # Get API key from environment (which now includes variables from .env)
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    # If still no API key, check if .env exists but key is not set or has placeholder
    env_path = Path(__file__).parent / '.env'
    
    # Check if API key is missing or still has placeholder text
    if not api_key and env_path.exists():
        print(f"{Colors.YELLOW}Found .env file but OPENROUTER_API_KEY is not set properly.{Colors.END}")
        print(f"Please edit the {env_path} file and set your API key.")
        sys.exit(1)
    elif not api_key:
        print(f"{Colors.YELLOW}No .env file or environment variable found for API key.{Colors.END}")
        print(f"Please create a .env file in {Path(__file__).parent} with your API key:")
        print("OPENROUTER_API_KEY=your_api_key_here")
        sys.exit(1)
    elif api_key in ["your_api_key_here", "sk-or-v1-abcdefg123456789"]:
        print(f"{Colors.YELLOW}You're using a placeholder API key in your .env file.{Colors.END}")
        print(f"Please edit the {env_path} file and set your actual OpenRouter API key.")
        sys.exit(1)
        
    return api_key

def create_headers(api_key):
    """Create HTTP headers for OpenRouter API"""
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://simple-terminal-chatbot.local",  # Replace with your site if deployed
        "X-Title": "Simple Terminal Chatbot",  # Identify your application to OpenRouter
    }

def chat_with_ai(messages, model=DEFAULT_MODEL, temperature=0.7):
    """Send messages to the AI and get a response"""
    api_key = get_api_key()
    headers = create_headers(api_key)
    
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 1000  # Adjust as needed
    }
    
    try:
        print(f"{Colors.YELLOW}AI is thinking...{Colors.END}")
        response = requests.post(API_URL, headers=headers, json=data, timeout=60)
        
        if response.status_code == 401:
            print(f"\n{Colors.RED}Authentication Error (401): Your API key was rejected by OpenRouter.{Colors.END}")
            print(f"{Colors.YELLOW}Please check that:{Colors.END}")
            print(f"1. Your API key is correct in the .env file")
            print(f"2. Your account is active at https://openrouter.ai/keys")
            print(f"3. You've properly formatted the key (should start with 'sk-or-')")
            sys.exit(1)
        
        response.raise_for_status()  # Raise exception for other HTTP errors
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        error_message = f"HTTP Error: {e.response.status_code}"
        try:
            error_data = e.response.json()
            if "error" in error_data and "message" in error_data["error"]:
                error_message += f" - {error_data['error']['message']}"
        except:
            pass
        return f"{Colors.RED}Error: {error_message}{Colors.END}"
    except Exception as e:
        return f"{Colors.RED}Error: {str(e)}{Colors.END}"

def print_welcome(model=DEFAULT_MODEL):
    """Print welcome message and instructions"""
    print(f"\n{Colors.BOLD}╔══════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.BOLD}║  Simple Terminal Chatbot with OpenRouter  ║{Colors.END}")
    print(f"{Colors.BOLD}╚══════════════════════════════════════════╝{Colors.END}")
    print(f"\n{Colors.GREEN}Welcome! Start chatting with AI.{Colors.END}")
    print(f"{Colors.BLUE}Type 'exit' to quit the program.{Colors.END}")
    print(f"{Colors.BLUE}Type 'model:model_name' to change the AI model.{Colors.END}")
    print(f"{Colors.BLUE}API Key: {Colors.GREEN}✓ Loaded from .env file{Colors.END}")
    print(f"{Colors.BLUE}Current model: {Colors.GREEN}{model}{Colors.END}\n")

def main():
    # Load environment variables
    load_env_file()
    
    # Check for custom model in environment variables
    current_model = os.environ.get("DEFAULT_MODEL", DEFAULT_MODEL)
    
    print_welcome(model=current_model)
    
    # Initialize conversation with system prompt
    conversation = [
        {"role": "system", "content": "You are a helpful, concise assistant. Respond in a clear, direct manner."}
    ]
    
    # Main chat loop
    while True:
        # Get user input
        user_input = input(f"{Colors.BOLD}You: {Colors.END}")
        
        # Check for exit command
        if user_input.lower() in ["exit", "quit", "bye"]:
            print(f"\n{Colors.GREEN}Goodbye! Have a nice day!{Colors.END}\n")
            break
            
        # Check for model change command
        if user_input.lower().startswith("model:"):
            try:
                new_model = user_input.split(":", 1)[1].strip()
                if new_model:
                    current_model = new_model
                    print(f"{Colors.BLUE}Model changed to: {current_model}{Colors.END}")
                    continue
            except:
                print(f"{Colors.RED}Invalid model format. Try again.{Colors.END}")
                continue
        
        # Add user message to conversation
        conversation.append({"role": "user", "content": user_input})
        
        # Get AI response
        ai_response = chat_with_ai(conversation, model=current_model)
        
        # Add AI response to conversation history
        conversation.append({"role": "assistant", "content": ai_response})
        
        # Display AI response
        print(f"{Colors.BOLD}AI: {Colors.END}{ai_response}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.GREEN}Program interrupted. Goodbye!{Colors.END}\n")
        sys.exit(0)
