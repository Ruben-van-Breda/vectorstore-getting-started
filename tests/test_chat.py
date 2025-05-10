#!/usr/bin/env python3
"""
Unit tests for chat.py
"""

import unittest
import sys
import os
from io import StringIO
from unittest.mock import patch

# Add parent directory to path to import chat module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ContextChat


class TestChat(unittest.TestCase):
    """Test cases for chat.py functions"""
    
    def test_process_query_expected_use(self):
        """Test process_query function with typical input"""
        query = "Hello world"
        expected = "You asked: Hello world"
        self.assertEqual(ContextChat.process_query(query), expected)
    
    def test_process_query_edge_case_empty(self):
        """Test process_query function with empty input"""
        query = ""
        expected = "You asked: "
        self.assertEqual(ContextChat.process_query(query), expected)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_interactive_mode_exit(self, mock_stdout):
        """Test interactive mode with exit command"""
        with patch('builtins.input', side_effect=['test query', 'exit']):
            ContextChat.interactive_mode()
            output = mock_stdout.getvalue()
            self.assertIn("Interactive chat mode", output)
            self.assertIn("You asked: test query", output)
            self.assertIn("Ending chat session", output)


if __name__ == '__main__':
    unittest.main() 