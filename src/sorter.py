import asyncio
from aiopath import AsyncPath
import logging
from typing import Union


async def copy_file(source_path: AsyncPath, output_path: AsyncPath) -> None:
    """
    Asynchronously copies a file to a destination folder, creating a subfolder
    based on the file's extension.

    Args:
        source_path (AsyncPath): The full path to the source file.
        output_path (AsyncPath): The full path to the destination directory.
    """
    try:
        source = source_path
        
        # Check if the source path is a file and exists
        if not await source.exists() or await source.is_dir():
            logging.error(f"Error: The source path '{source}' is not a file or does not exist.")
            return

        # Determine file extension and create a subfolder name
        extension: str = source.suffix.lstrip('.').lower()
        if not extension:
            extension = "other"

        # Create the path to the subfolder based on the extension
        target_dir: AsyncPath = output_path / extension

        # Create the destination subfolder if it doesn't exist
        await target_dir.mkdir(parents=True, exist_ok=True)

        # Create the path for the new file
        target_file: AsyncPath = target_dir / source.name

        # Asynchronously read and write file content
        content: bytes = await source.read_bytes()
        await target_file.write_bytes(content)
        
        print(f"Copied: {source.name} -> {target_file}")
        
    except Exception as e:
        logging.error(f"Error copying file '{source_path}': {e}")


async def read_folder(src_dir: Union[str, AsyncPath], dest_dir: Union[str, AsyncPath]) -> None:
    """
    Recursively and asynchronously traverses a source folder and copies files.

    Args:
        src_dir (Union[str, AsyncPath]): The path to the source directory.
        dest_dir (Union[str, AsyncPath]): The path to the destination directory.
    """
    source_path: AsyncPath = AsyncPath(src_dir)
    dest_path: AsyncPath = AsyncPath(dest_dir)

    # Check if the source path exists and is a directory
    if not await source_path.is_dir():
        logging.error(f"Error: The path '{source_path}' does not exist or is not a folder.")
        return

    print(f"Starting to process folder: {source_path}")

    tasks = []
    # Asynchronously iterate over the directory content
    async for item in source_path.iterdir():
        # Check if the item is a directory
        if await item.is_dir():
            # Create a recursive task for the subdirectory
            tasks.append(asyncio.create_task(read_folder(item, dest_path)))
        else:
            # Create a task for copying the file
            tasks.append(asyncio.create_task(copy_file(item, dest_path)))

    # Run all tasks concurrently
    if tasks:
        await asyncio.gather(*tasks)