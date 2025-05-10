#!/bin/bash

# Get the first argument
QUERY="$1"
VECTORE_STORE=./vectorestore


python3 ../../chroma_context_agent.py --query "${QUERY}" --directory "$VECTORE_STORE" > answer.txt
cat answer.txt
