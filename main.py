import argparse
import asyncio
from aiopath import AsyncPath
import logging
import sys

from src.logger_config import setup_logging
from src.sorter import read_folder

def main() -> None:
    """
    The main function to parse arguments and run the file sorting process.
    """
    parser = argparse.ArgumentParser(description="Recursively sorts files in a source folder.")
    
    # Define command-line arguments
    parser.add_argument("src_path", help="Path to the source folder.")
    parser.add_argument("dest_path", help="Path to the destination folder.")
    
    args = parser.parse_args()

    async def run_process() -> None:
        """
        An async wrapper to handle path normalization and execution.
        """
        try:
            # Asynchronously resolve paths
            normalized_src: AsyncPath = await AsyncPath(args.src_path).resolve()
            normalized_dest: AsyncPath = await AsyncPath(args.dest_path).resolve()
            
            # Start the main sorting process
            await read_folder(normalized_src, normalized_dest)
        except Exception as e:
            logging.error(f"An unknown error occurred during execution: {e}")

    # Set up logging before running the process
    setup_logging()

    # Run the async main function
    asyncio.run(run_process())

if __name__ == "__main__":
    main()