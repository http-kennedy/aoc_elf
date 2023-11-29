import os
import re
from dotenv import load_dotenv

ENV_FILE = ".env"


def is_valid_github_repo(url: str) -> bool:
    """
    Checks if the given URL is a valid GitHub repository URL.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL is a valid GitHub repository URL, False otherwise.
    """
    pattern = r"https://github\.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9._-]+/?"
    return re.match(pattern, url) is not None


def is_valid_base_dir(base_dir: str) -> bool:
    """
    Validates the base directory input, removing trailing slashes and checking existence.

    Args:
        base_dir (str): The base directory to validate.

    Returns:
        bool: True if the directory is valid or the input is empty, False otherwise.
    """

    formatted_dir = base_dir.rstrip("/\\")
    if os.path.isdir(formatted_dir) or not base_dir:
        return formatted_dir
    print(f"\nDirectory '{base_dir}' does not exist.\n")
    return False


def get_input(prompt: str, default: str = None, validator: callable = None) -> str:
    """Get input from the user with an optional default value and validator.

    Args:
        prompt (str): The prompt to display to the user.
        default (str, optional): The default value if the user enters nothing. Defaults to None.
        validator (callable, optional): A function to validate the input. Defaults to None.

    Returns:
        str: The validated and formatted user input, or the default value if the user entered nothing.
    """
    while True:
        value = input(prompt).strip()
        if not value:
            return default if default is not None else "none"
        if validator:
            validated_value = validator(value)
            if validated_value is not False:
                return validated_value
            print(f"Invalid input: '{value}'. Please try again.")
        else:
            return value


def reload_env() -> None:
    """
    Reloads the environment variables from the .env file.
    """
    load_dotenv(override=True)


def modify_config() -> None:
    """
    Modifies the existing configuration in the .env file.
    """
    print("\nFound existing configuration... Modifying existing configuration...\n")

    CURRENT_BASE_DIR = os.getenv("BASE_DIR")
    CURRENT_GITHUB_REPO = os.getenv("GITHUB_REPO")
    CURRENT_AOC_SESSION = os.getenv("AOC_SESSION")

    BASE_DIR = get_input(
        f"Current base directory is '{CURRENT_BASE_DIR}'. Enter new base directory (leave blank to keep current): ",
        os.getenv("BASE_DIR"),
        validator=is_valid_base_dir,
    )
    GITHUB_REPO = get_input(
        f"\nCurrent GitHub repository url is '{CURRENT_GITHUB_REPO}'. Enter new url (leave blank to keep current): ",
        os.getenv("GITHUB_REPO"),
        is_valid_github_repo,
    )

    print(f"\nCurrent AOC_SESSION token is '{CURRENT_AOC_SESSION}'.")
    print("To get your AOC_SESSION token:")
    print("1. Log in to Advent of Code.")
    print("2. Open the developer tools (F12 or Ctrl+Shift+I).")
    print("3. Go to the Application tab.")
    print("4. Under 'Cookies', select 'https://adventofcode.com'.")
    print("5. Find the 'session' cookie and copy its value.\n")
    AOC_SESSION = get_input(
        "Enter your AOC_SESSION token (leave blank to keep current): ",
        default=os.getenv("AOC_SESSION"),
    )

    with open(ENV_FILE, "w") as f:
        f.write(f"BASE_DIR={BASE_DIR}\n")
        f.write(f"GITHUB_REPO={GITHUB_REPO}\n")
        f.write(f"AOC_SESSION={AOC_SESSION}\n")
        f.write("SETUP_RAN=1\n")

    reload_env()

    print("\nConfiguration modified successfully!")


def setup_config() -> None:
    """
    Sets up the initial configuration and writes it to the .env file.
    """
    load_dotenv()

    if os.getenv("SETUP_RAN") == "1":
        modify_config()
        return

    print("\nWelcome to py_aoc setup!")
    print("Let's setup your configuration.\n")

    BASE_DIR = get_input(
        "Enter base directory (your AoC solutions environment will be made in this directory): \n",
        default=os.getenv("BASE_DIR"),
        validator=is_valid_base_dir,
    )
    GITHUB_REPO = get_input(
        # FIX ME AFTER TESTING git_operations.py
        "Enter the GitHub repository url: \n",
        default=os.getenv("GITHUB_REPO"),
        validator=is_valid_github_repo,
    )

    print("To get your AOC_SESSION token using Chrome:")
    print("1. Log in to Advent of Code.")
    print("2. Open the developer tools (F12 or Ctrl+Shift+I).")
    print("3. Go to the Application tab.")
    print("4. Under 'Cookies', select 'https://adventofcode.com'.")
    print("5. Find the 'session' cookie and copy its value.\n")
    AOC_SESSION = get_input(
        "Enter your AOC_SESSION token (used for fetching puzzle inputs|examples, and submitting answers): ",
        default=os.getenv("AOC_SESSION"),
    )

    with open(ENV_FILE, "w") as f:
        f.write(f"BASE_DIR={BASE_DIR}\n")
        f.write(f"GITHUB_REPO={GITHUB_REPO}\n")
        f.write(f"AOC_SESSION={AOC_SESSION}\n")
        f.write("SETUP_RAN=1\n")

    reload_env()

    print("Configuration set up successfully!")


if __name__ == "__main__":
    setup_config()
