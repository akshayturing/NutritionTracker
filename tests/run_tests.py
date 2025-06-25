import pytest
import sys

if __name__ == "__main__":
    # Run all tests and display results
    exit_code = pytest.main(['-v'])
    sys.exit(exit_code)