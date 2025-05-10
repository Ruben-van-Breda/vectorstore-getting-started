#!/usr/bin/env python3

import unittest
from unittest.mock import patch, MagicMock
import io
import sys
from contextlib import redirect_stdout

# Import the module to test
from ContextChat import (
    setup_cli,
    load_vectorstore,
    query_vectorstore,
    display_results,
    interactive_mode
)

class TestChat(unittest.TestCase):
    """Test cases for the chat.py module."""
    
    def test_load_vectorstore_success(self):
        """Test loading vector store successfully."""
        result = load_vectorstore("./test_path")
        self.assertEqual(result, {"path": "./test_path", "loaded": True})
    
    @patch('sys.exit')
    def test_load_vectorstore_error(self, mock_exit):
        """Test handling error when loading vector store."""
        # This test depends on implementation details. If load_vectorstore
        # is modified to handle errors differently, this test will need updating.
        with patch('builtins.print') as mock_print:
            # Force an exception by passing an invalid path type
            load_vectorstore(123)  # Assuming this causes an exception
            mock_exit.assert_called_once()
            # Check that an error message was printed
            mock_print.assert_called()
    
    def test_query_vectorstore(self):
        """Test querying the vector store."""
        mock_store = {"path": "./test", "loaded": True}
        results = query_vectorstore(mock_store, "test query", 2)
        
        # Check that we got the expected number of results
        self.assertEqual(len(results), 2)
        # Check the content of results
        self.assertEqual(results[0]["content"], "Result 1 for query: test query")
        self.assertEqual(results[1]["content"], "Result 2 for query: test query")
        # Check the scores
        self.assertAlmostEqual(results[0]["score"], 0.9)
        self.assertAlmostEqual(results[1]["score"], 0.8)
    
    def test_display_results(self):
        """Test displaying results."""
        results = [
            {"content": "Test result 1", "score": 0.95},
            {"content": "Test result 2", "score": 0.85}
        ]
        
        # Capture stdout to check output
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            display_results(results)
        
        output = captured_output.getvalue()
        self.assertIn("1. Test result 1 (Score: 0.95)", output)
        self.assertIn("2. Test result 2 (Score: 0.85)", output)
    
    def test_display_results_empty(self):
        """Test displaying empty results."""
        # Capture stdout to check output
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            display_results([])
        
        output = captured_output.getvalue()
        self.assertIn("No results found", output)
    
    @patch('builtins.input', side_effect=["test query", "exit"])
    def test_interactive_mode(self, mock_input):
        """Test interactive mode with a query and then exit."""
        mock_store = {"path": "./test", "loaded": True}
        
        # Capture stdout to check output
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            interactive_mode(mock_store, 2)
        
        output = captured_output.getvalue()
        self.assertIn("Interactive Mode", output)
        self.assertIn("Searching for: test query", output)
        self.assertIn("Goodbye!", output)

if __name__ == "__main__":
    unittest.main() 