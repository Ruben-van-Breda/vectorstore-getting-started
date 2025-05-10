#!/bin/bash

OUTPUT_DIR=./vectorestore
INPUT_DIR=./input/

# Vectorize Data
echo "Vectorize Data"
python3 ../../chroma_vectorize_data.py "$INPUT_DIR" -o "$OUTPUT_DIR"

echo "Query Data"
python3 ../../chroma_context_agent.py --query "what is Sip Dialogs about" --directory "$OUTPUT_DIR" 