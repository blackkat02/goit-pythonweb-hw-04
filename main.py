import argparse
import asyncio
from aiopath import AsyncPath

from src.logger_config import setup_logging
from src.sorter import read_folder


def main() -> None:
    """
    The main function to parse arguments and run the file sorting process.
    """
    parser = argparse.ArgumentParser(description="Recursively sorts files in a source folder.")
    parser.add_argument("src_path", help="Path to the source folder.")
    parser.add_argument("dest_path", help="Path to the destination folder.")
    args = parser.parse_args()

    setup_logging()

    asyncio.run(
        read_folder(
            AsyncPath(args.src_path),
            AsyncPath(args.dest_path)
        )
    )


if __name__ == "__main__":
    main()
