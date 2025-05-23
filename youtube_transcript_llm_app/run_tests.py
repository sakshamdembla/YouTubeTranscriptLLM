#!/usr/bin/env python3
"""
Test runner for YouTube Transcript LLM App.
Discovers and runs all tests in the tests directory.
"""
import unittest
import os
import sys

def run_tests():
    """Discover and run all tests"""
    # Get the directory containing this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Set up the test discovery
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(
        start_dir=os.path.join(current_dir, 'tests'),
        pattern='test_*.py'
    )
    
    # Create a test runner and run the tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Return appropriate exit code based on test results
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests()) 