# Vector Store Query CLI

A simple command-line interface for querying vector stores.

## Features

- Query a vector store with natural language
- Interactive mode for multiple queries
- Configurable number of top results to display
- Simple and easy-to-use interface

## Installation

No additional installation is required beyond the project dependencies.

## Usage

```bash
# Basic usage with a query
python chat.py "What is vector embedding?"

# Specify the vector store path
python chat.py -v ./my_vectorstore "How do embeddings work?"

# Get more results (default is 3)
python chat.py -k 5 "Explain similarity search"

# Run in interactive mode
python chat.py -i
```

### Command Line Arguments

- `-v, --vectorstore`: Path to the vector store directory (default: "./vectorstore")
- `-k, --top_k`: Number of top results to return (default: 3)
- `-i, --interactive`: Run in interactive mode
- `query`: The search query (not required when using interactive mode)

## Development

### Running Tests

To run the unit tests:

```bash
python -m unittest test_chat.py
```

## Implementation Notes

This is currently a placeholder implementation with simulated results. To use with a real vector store:

1. Update the `load_vectorstore` function to load your specific vector store type
2. Modify the `query_vectorstore` function to perform actual similarity searches 