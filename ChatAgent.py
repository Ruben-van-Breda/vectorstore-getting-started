# chat_agent.py

import os
import argparse
from openai import OpenAI

client = OpenAI()

def SetupAgent():
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError("❌ OPENAI_API_KEY not found in environment variables.")

def Query(prompt, model="gpt-4", system_message="You are a helpful assistant."):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple ChatGPT CLI")
    parser.add_argument("-q", "--query", help="Prompt to ask ChatGPT")
    parser.add_argument("-sys", "--system", help="System message to guide the assistant", default="You are an expert assistant.")
    args = parser.parse_args()

    SetupAgent()

    print(f"🧠 System Message: {args.system}")

    if args.query:
        answer = Query(args.query, system_message=args.system)
        print(answer)
    else:
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("👋 Goodbye!")
                break
            answer = Query(user_input, system_message=args.system)
            print("ChatGPT:", answer)