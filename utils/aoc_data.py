import os
import subprocess
import json
import glob
from typing import Tuple, Optional
from aocd import get_data
from datetime import datetime
from dateutil.parser import parse
from utils.environment import setup_environment
from utils.file_operations import AOC_DAYS, get_aoc_root_dir, get_day_directory
from utils.config import is_valid_base_dir
from aoc_elf import aocd_dir


AOC_ROOT_DIR = get_aoc_root_dir()


def get_day_and_year() -> Tuple[int, int]:
    """
    Prompts the user to input the day and year for the Advent of Code challenge.

    Returns:
        A tuple containing the day and year as integers.
    """
    now = datetime.now()
    default_year = now.year if now.month == 12 and 1 <= now.day <= 25 else None
    default_day = now.day if now.month == 12 and 1 <= now.day <= 25 else None

    while True:
        try:
            year_input = input(f"Enter the year (default: {default_year}): ").strip()
            year = int(year_input) if year_input else default_year
            if year and (2015 <= year <= now.year):
                break
            else:
                print(
                    f"Invalid year: {year}. Please enter a year between 2015 and {now.year}."
                )
        except ValueError:
            print(
                f"Invalid input. Please enter a valid year between 2015 and {now.year}."
            )

    while True:
        try:
            day_input = input(f"Enter the day (default: {default_day}): ").strip()
            day = int(day_input) if day_input else default_day
            if day and (1 <= day <= AOC_DAYS):
                break
            else:
                print(
                    f"Invalid day: {day}. Please enter a day between 1 and {AOC_DAYS}."
                )
        except ValueError:
            print(f"Invalid input. Please enter a valid day between 1 and {AOC_DAYS}.")

    return day, year


def fetch_data_for_day() -> None:
    """
    Fetches data for the specified day of Advent of Code challenge.
    It includes puzzle input and example input.
    """
    print("\nFetching puzzle and example input for the specific 'year' and 'day'...")
    day, year = get_day_and_year()
    day_dir = get_day_directory(year, day, AOC_ROOT_DIR)

    if not is_valid_base_dir(day_dir, False):
        day_dir = input(
            f"\nDirectory '{day_dir}' does not exist. Enter new directory to save input.txt and example.txt: \n"
        )

    get_puzzle_input(day, year, day_dir)
    example_fetched = get_example_input(day, year, day_dir)

    part_a_completed = check_for_part_a_completion(day, year, aocd_dir)
    example_file = os.path.join(day_dir, "example.txt")
    example_exists = os.path.exists(example_file)

    if (part_a_completed or example_exists) and not example_fetched:
        check_and_update_example_input(day, year, day_dir)


def get_puzzle_input(day: int, year: int, day_dir: str) -> bool:
    """
    Retrieves puzzle input for a given day and year, and saves it to a file.

    Args:
        day: The day of the puzzle.
        year: The year of the puzzle.
        day_dir: The directory path where the puzzle input should be saved.

    Returns:
        True if the data was successfully fetched and saved, False otherwise.
    """
    input_file = os.path.join(day_dir, "input.txt")

    if not os.path.exists(day_dir):
        os.makedirs(day_dir, exist_ok=True)

    if not os.path.exists(input_file):
        try:
            data = get_data(day=day, year=year)
            with open(input_file, "w") as f:
                f.write(data)
                print(
                    f"Fetched puzzle input for day '{day}' of year '{year}'! Located at {input_file}."
                )
            return True
        except Exception as e:
            print(f"Failed to fetch puzzle input for day '{day}' of year '{year}'!")
            print(f"Error: {e}")
            return False


def get_example_input(day: int, year: int, day_dir: str) -> bool:
    """
    Retrieves example input for a given day and year, and saves it to a file.

    Args:
        day: The day of the puzzle.
        year: The year of the puzzle.
        day_dir: The directory path where the example input should be saved.

    Returns:
        True if the data was successfully fetched and saved, False otherwise.
    """

    if not is_valid_base_dir(day_dir, False):
        day_dir = input(
            f"\nDirectory '{day_dir}' does not exist. Enter new directory to save new example.txt: \n"
        )

    example_file = os.path.join(day_dir, "example.txt")

    if not os.path.exists(day_dir):
        os.makedirs(day_dir, exist_ok=True)

    if not os.path.exists(example_file):
        try:
            result = subprocess.run(
                ["aocd", str(day), str(year), "--example"],
                capture_output=True,
                text=True,
                check=True,
            )
            with open(example_file, "w") as f:
                f.write(result.stdout)
                print(
                    f"Fetched example input for day '{day}' of year '{year}'! Located at {example_file}."
                )
            return True
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.strip().split("\n")[-1]
            print(f"Failed to fetch example input for day '{day}' of year '{year}'!")
            # print(f"Error: {error_message}") #TODO: Make this cleaner? Seems redundant as the error message /should always match get_puzzle_input()
            return False
    return False


def check_for_part_a_completion(day: int, year: int, aocd_dir: str) -> bool:
    """
    Checks if part A of the puzzle for a given day and year has been completed.

    Args:
        day: The day of the puzzle.
        year: The year of the puzzle.
        aocd_dir: The directory path where submission data is stored.

    Returns:
        True if part A has been completed, False otherwise.
    """
    post_file_path = os.path.join(aocd_dir, f"{year}/day_{day:02}_post.json")

    if not os.path.exists(post_file_path):
        return False

    with open(post_file_path, "r") as file:
        submissions = json.load(file)

    for submission in submissions:
        if submission.get(
            "part"
        ) == "a" and "That's the right answer" in submission.get("message", ""):
            return True

    return False


def check_and_update_example_input(day: int, year: int, day_dir: str) -> bool:
    """
    Checks if the example input needs to be updated and updates it if available.

    Args:
        day: The day of the puzzle.
        year: The year of the puzzle.
        day_dir: The directory path where the example input is stored.

    Returns:
        True if the example input was successfully updated or fetched, False otherwise.
    """
    example_file = os.path.join(day_dir, "example.txt")

    if os.path.exists(example_file):
        with open(example_file, "r") as file:
            example_input = file.read()

        if "answer_b: -" in example_input:
            try:
                result = subprocess.run(
                    ["aocd", str(day), str(year), "--example"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                with open(example_file, "w") as f:
                    f.write(result.stdout)

                with open(example_file, "r") as file:
                    updated_example_input = file.read()

                if "answer_b: -" not in updated_example_input:
                    print(
                        f"Updated example input for Part B for day '{day}' of year '{year}' in {example_file}."
                    )
                return True
            except subprocess.CalledProcessError as e:
                error_message = e.stderr.strip().split("\n")[-1]
                print(
                    f"Failed to update example input for Part B for day '{day}' of year '{year}' in {example_file}."
                )
                # print(f"Error: {error_message}")
                return False
    else:
        return get_example_input(day, year)

    print(
        f"\nPuzzle input and example input already exists for day '{day}' of year '{year}' at {day_dir}."
    )
    return False


if __name__ == "__main__":
    fetch_data_for_day()
