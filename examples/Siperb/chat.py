#!/usr/bin/env python3
"""
A simple command line chat program that can run in interactive mode.

Usage:
  python chat.py -i      # Run in interactive mode
  python chat.py "query" # Process a single query
"""

import argparse
import sys
import subprocess


def process_query(query):
    """
    Process a user query and return a response.
    
    @param query - The user's input query
    @returns A response to the query
    """
    response = run_bash(f"./vector_query.sh \"{query}\"")
    context_query = f"""You are an expert assistant. Use the provided context to answer the user query accurately and concisely.

[CONTEXT]
{response}

[USER QUESTION]
{query}
"""
    chat_response = run_bash(f"./chat.sh \"{context_query}\"")

    return f"{chat_response}"


def interactive_mode():
    """
    Run the program in interactive mode, continuously prompting for input.
    """
    print("Interactive chat mode. Type 'exit' or 'quit' to end the session.")
    
    while True:
        try:
            query = input("> ")
            if query.lower() in ['exit', 'quit']:
                print("Ending chat session. Goodbye!")
                break
                
            response = process_query(query)
            print(response)
            
        except KeyboardInterrupt:
            print("\nSession terminated by user. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

# Run bash script function

def run_bash(command):
    """
    Runs a bash command and returns the output.
    
    @param command - The bash command to run (as a string)
    @returns The output from the command
    """
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if result.returncode != 0:
            raise Exception(result.stderr.strip())
        return result.stdout.strip()
    except Exception as e:
        return f"Error running bash command: {e}"

def main():
    """
    Main entry point of the program.
    """
    parser = argparse.ArgumentParser(description="Simple command line chat program")
    parser.add_argument("-i", "--interactive", action="store_true", 
                        help="Run in interactive mode")
    parser.add_argument("query", nargs="?", type=str,
                        help="Query to process (if not in interactive mode)")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
    elif args.query:
        response = process_query(args.query)
        print(response)
    else:
        print("No query provided. Run with -h for help.")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main() 