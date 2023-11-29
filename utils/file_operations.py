import os
import shutil
from datetime import datetime
from typing import Optional, Dict, List, Tuple
from utils.environment import setup_environment

AOC_DAYS = 25  # Advent of code has 25 challenges per year


def get_aoc_root_dir() -> str:
    """
    Gets the Advent of Code root directory path from the environment variables.

    Returns:
        The path to the AOC root directory.
    """
    _, AOC_ROOT_DIR, _, _ = setup_environment()
    return AOC_ROOT_DIR


def get_day_directory(year: int, day: int, AOC_ROOT_DIR: str) -> str:
    """
    Constructs the path to the directory for a specific day of Advent of Code.

    Args:
        year: The year of the challenge.
        day: The day of the challenge.
        AOC_ROOT_DIR: The root directory for Advent of Code challenges.

    Returns:
        The path to the directory for the specified day.
    """
    return os.path.join(AOC_ROOT_DIR, str(year), f"day_{day:02}")


def get_input() -> int:
    """
    Prompts the user to enter the year for the Advent of Code challenge.

    Returns:
        The entered year or the current year if no input is provided.
    """
    current_year = datetime.now().year
    year = input(f"Enter the AOC year (default: {current_year}): ").strip()

    if not year:
        return current_year

    try:
        return int(year)
    except ValueError:
        print(f"Invalid year: {year}")
        return get_input()


def confirm_overwrite(path: str) -> bool:
    """
    Asks the user for confirmation to overwrite an existing directory.

    Args:
        path: The path of the directory to check for overwriting.

    Returns:
        True if the user confirms overwrite, False otherwise.
    """
    while True:
        response = (
            input(
                f"Directory {path} already exists. Default is no (enter). Overwrite? (y/n): "
            )
            .strip()
            .lower()
        )
        if response == "y":
            return True
        elif response == "n" or response == "":
            return False
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")


def create_year_dir(year: int, AOC_ROOT_DIR: str) -> Optional[str]:
    """
    Creates a directory for the specified year. Asks for confirmation if the directory already exists.

    Args:
        year: The year for which the directory is to be created.
        aoc_root_dir: The root directory that contains the year directories.

    Returns:
        The path to the created directory, or None if not created.
    """

    year_dir = os.path.join(AOC_ROOT_DIR, str(year))

    if os.path.exists(year_dir):
        if not confirm_overwrite(year_dir):
            return None  # Return None if the user chose not to overwrite

    try:
        os.makedirs(year_dir, exist_ok=True)
    except Exception as e:
        print(f"Failed to create directory {year_dir}: {e}")
        return None

    return year_dir


def create_day_dir(year_dir: str) -> Dict[str, List[str]]:
    """
    Creates directories for each day of Advent of Code within the specified year directory.

    Args:
        year_dir: The path to the year directory.

    Returns:
        A dictionary with keys 'created' and 'skipped', each containing a list of directory paths.
    """
    results = {"created": [], "skipped": []}

    for day in range(1, AOC_DAYS + 1):
        day_dir = os.path.join(year_dir, f"day_{day:02}")
        if os.path.exists(day_dir) and not confirm_overwrite(day_dir):
            results["skipped"].append(day_dir)
            continue

        try:
            if os.path.exists(day_dir):
                shutil.rmtree(
                    day_dir
                )  # Remove the existing directory if the user chose to overwrite
            os.makedirs(day_dir, exist_ok=True)  # Create the directory
            if copy_solution_template(day_dir):
                results["created"].append(day_dir)
            else:
                results["skipped"].append(day_dir)
        except Exception as e:
            print(f"Failed to create directory {day_dir}: {e}")
            results["skipped"].append(day_dir)

    return results


def copy_solution_template(day_dir: str) -> bool:
    """
    Copies the solution and helper templates to the specified day's directory.

    Args:
        day_dir: The path to the day's directory where the templates should be copied.

    Returns:
        True if successful, False otherwise.
    """
    solution_template_path = os.path.join("utils", "templates", "solution.py")
    helper_template_path = os.path.join("utils", "templates", "helper.py")

    solution_dest_path = os.path.join(day_dir, "solution.py")
    helper_dest_path = os.path.join(day_dir, "helper.py")

    try:
        shutil.copy(solution_template_path, solution_dest_path)
        shutil.copy(helper_template_path, helper_dest_path)
        return True
    except Exception as e:
        print(f"Failed to copy templates to {day_dir}: {e}")
        return False


def setup_aoc_environment() -> None:
    """
    Sets up the Advent of Code environment for a given year.
    Creates directories for each day and copies solution templates.
    """

    AOC_ROOT_DIR = get_aoc_root_dir()

    print(f"\nYour AoC root directory will be -> {AOC_ROOT_DIR}/'YYYY'/day_'DD' <-\n")
    year = get_input()
    year_dir = create_year_dir(year, AOC_ROOT_DIR)

    if year_dir is None:
        print(f"\nEnvironment setup for year {year} aborted.")
        return

    results = create_day_dir(year_dir)

    print(f"\nEnvironment setup for year {year} completed.")

    if results["created"]:
        print("Created directories:")
        for directory in results["created"]:
            print(f"  - {directory}")

    if results["skipped"]:
        print("\nSkipped directories:")
        for directory in results["skipped"]:
            print(f"  - {directory}")


if __name__ == "__main__":
    setup_aoc_environment()
