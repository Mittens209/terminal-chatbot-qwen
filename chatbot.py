import requests
import time
import sys
import threading

# 🔑 Replace with your real OpenRouter API key
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def ask_bot(prompt):
    data = {
        "model": "mistralai/mistral-7b-instruct:free",  # free model option
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(API_URL, headers=headers, json=data)
    result = response.json()
    try:
        return result["choices"][0]["message"]["content"]
    except:
        return "⚠️ Error: " + str(result)

def type_out(text, delay=0.03):
    """Print text like typing effect"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # new line after finished

def typing_animation(stop_event):
    """Shows 'Bot is typing...' animation until stop_event is set"""
    dots = ""
    while not stop_event.is_set():
        sys.stdout.write("\rBot is typing" + dots)
        sys.stdout.flush()
        dots += "."
        if len(dots) > 3:
            dots = ""
        time.sleep(0.5)
    sys.stdout.write("\r" + " " * 20 + "\r")  # clear line

print("🤖Chatbot ready! Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Bot: Goodbye!")
        break

    # Start typing animation in background
    stop_event = threading.Event()
    t = threading.Thread(target=typing_animation, args=(stop_event,))
    t.start()

    # Get bot reply
    reply = ask_bot(user_input)

    # Stop animation
    stop_event.set()
    t.join()

    # Show reply with typing effect
    print("Bot:", end=" ", flush=True)
    type_out(reply)
