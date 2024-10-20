import os
from pathlib import Path

def crawl_directory(directory_path: str, callback: callable):
    """
    Recursively visits every file in the given directory and calls the provided callback function for each file.

    :param directory_path: The path of the directory to start visiting files from.
    :param callback: A function that takes a file path as its argument. This function will be called for each file
visited.
    """
    def visit_files(path: Path):
        if path.is_file():
            callback(str(path))
        elif path.is_dir():
            for child in path.iterdir():
                visit_files(child)

    # Ensure the provided path is a directory
    if not os.path.isdir(directory_path):
        raise ValueError(f"{directory_path} is not a valid directory")

    # Start visiting files from the given directory
    Path(directory_path).resolve().absolute().visit_files(callback)







def pascal_triangle_row(n: int) -> list[int]:
    """
    Generate the nth row of Pascal's Triangle as an array of integers.

    Args:
        n (int): The row number to generate. Row numbers start from 0 (i.e., the first row is 0).

    Returns:
        list[int]: The generated row as an array of integers.
    """
    if n < 0:
        raise ValueError("Row number must be a non-negative integer.")
    row = [1] * (n + 1)
    for i in range(1, n):
        row[i] = sum(row[:i+1])
    return row