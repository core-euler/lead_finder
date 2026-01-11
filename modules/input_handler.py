import logging
import re
from typing import List

logger = logging.getLogger(__name__)

def process_sources(source_args: List[str], file_path: str) -> List[str]:
    """
    Processes input sources from both command-line arguments and a file.
    Returns a unique, clean list of source identifiers.
    """
    raw_sources = []

    # 1. Read from file if provided
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        raw_sources.append(line)
            logger.info(f"Loaded {len(raw_sources)} sources from file: {file_path}")
        except FileNotFoundError:
            logger.error(f"Source file not found: {file_path}")
        except Exception as e:
            logger.error(f"Error reading source file {file_path}: {e}")

    # 2. Add from command-line arguments
    if source_args:
        raw_sources.extend(source_args)

    # 3. Deduplicate and validate
    unique_sources = set()
    valid_pattern = re.compile(r'^(@[a-zA-Z0-9_]{5,32}|t\.me\/[a-zA-Z0-9_]{5,32}|t\.me\/\+[a-zA-Z0-9_-]+)$')
    
    for source in raw_sources:
        source = source.strip()
        if valid_pattern.match(source):
            unique_sources.add(source)
        else:
            logger.warning(f"Skipping invalid source format: '{source}'")

    final_sources = list(unique_sources)
    logger.info(f"Processed a total of {len(final_sources)} unique and valid sources.")
    
    return final_sources

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    mock_args = ["@chat1", "t.me/chat2", "invalid-source"]
    mock_file_content = """
# This is a comment
@chat2
@chat3
t.me/+ABC123XYZ
    """
    mock_file_path = "test_sources.txt"
    with open(mock_file_path, "w") as f:
        f.write(mock_file_content)

    print("--- Testing with args and file ---")
    processed = process_sources(mock_args, mock_file_path)
    print(f"Processed sources: {processed}")
    
    print("\n--- Testing with file only ---")
    processed = process_sources([], mock_file_path)
    print(f"Processed sources: {processed}")

    print("\n--- Testing with args only ---")
    processed = process_sources(mock_args, None)
    print(f"Processed sources: {processed}")

    import os
    os.remove(mock_file_path)
