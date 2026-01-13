# Execution Scripts

This directory contains deterministic Python scripts that perform the actual work.

## Principles

1. **Deterministic**: Given the same inputs, scripts should produce the same outputs
2. **Single Responsibility**: Each script does one thing well
3. **Error Handling**: Proper try/catch blocks and meaningful error messages
4. **Logging**: Use Python's logging module to track execution
5. **Environment Variables**: Use `.env` for all secrets and configuration

## Script Template

```python
#!/usr/bin/env python3
"""
Brief description of what this script does.
"""

import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def main():
    """Main execution function."""
    try:
        logger.info("Starting script execution")
        
        # Your code here
        
        logger.info("Script completed successfully")
        return True
    except Exception as e:
        logger.error(f"Script failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
```

## Guidelines

- **Use environment variables** for API keys and configuration
- **Add docstrings** to all functions
- **Handle errors gracefully** with try/except blocks
- **Log execution progress** so issues can be debugged
- **Return meaningful data** that the AI can use for decisions
- **Keep scripts focused** - one clear purpose per script
