# chat_agent.py

import os
import argparse
from openai import OpenAI

client = OpenAI()
# Setup the OpenAI client
def SetupAgent():
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError("❌ OPENAI_API_KEY not found in environment variables.")
    # print("✅ OpenAI Agent setup complete.")
# Send a prompt to ChatGPT
def Query(prompt, model="gpt-4"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"


# Example usage
if __name__ == "__main__":

    # Check aruments if -q "" is in the command 
    # run this else do while True
    parser = argparse.ArgumentParser(description="Simple ChatGPT CLI")
    parser.add_argument("-q", "--query", help="Prompt to ask ChatGPT")
    args = parser.parse_args()


    SetupAgent()

    if args.query:
        answer = Query(args.query)
        print(answer)
    else:
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            answer = Query(user_input)
            print("ChatGPT:", answer)