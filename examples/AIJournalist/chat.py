#!/usr/bin/env python3
"""
A simple command line chat program that can run in interactive mode.

Usage:
  python chat.py -i                # Run in interactive mode
  python chat.py "query"          # Process a single query
  python chat.py -i --no-history  # Interactive without query history
"""

import argparse
import sys
import subprocess

system_message = "Your name is Simone"

def process_query(query, system_message=None):
    """
    Process a user query and return a response.
    """
    system_msg = system_message or "You are an expert assistant. Use the provided context to answer the user query accurately and concisely."

    response = run_bash(f"./vector_query.sh \"{query}\"")
    context_query = f"""{system_msg}

[CONTEXT]
{response}

[USER QUESTION]
{query}
"""
    chat_response = run_bash(f"./chat.sh \"{context_query}\"")
    return f"{chat_response}"


def interactive_mode(include_history=True):
    """
    Run the program in interactive mode, continuously prompting for input.
    """
    print("🗨️  Interactive chat mode. Type 'exit' or 'quit' to end the session.")
    history = []



    while True:
        try:
            query = input("> ")
            if query.lower() in ['exit', 'quit']:
                print("👋 Ending chat session. Goodbye!")
                break

            if include_history:
                full_history = "\n".join(history + [query])
                response = process_query(full_history, system_message=system_message)
            else:
                response = process_query(query)

            history.append(query)
            history.append(response)
            print(response)

        except KeyboardInterrupt:
            print("\n⛔ Session terminated by user. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def run_bash(command):
    """
    Runs a bash command and returns the output.
    """
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if result.returncode != 0:
            raise Exception(result.stderr.strip())
        return result.stdout.strip()
    except Exception as e:
        return f"Error running bash command: {e}"


def main():
    parser = argparse.ArgumentParser(description="Simple command line chat program")
    parser.add_argument("-i", "--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--no-history", action="store_true", help="Do not include history in interactive mode")
    parser.add_argument("query", nargs="?", type=str, help="Query to process (if not in interactive mode)")

    args = parser.parse_args()

    if args.interactive:
        interactive_mode(include_history=not args.no_history)
    elif args.query:
        response = process_query(args.query)
        print(response)
    else:
        print("⚠️  No query provided. Run with -h for help.")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()