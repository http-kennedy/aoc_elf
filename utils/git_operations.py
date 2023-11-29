import subprocess
import platform
from typing import Optional
from utils.aoc_data import get_day_and_year
from utils.environment import setup_environment

_, AOC_ROOT_DIR, _, _ = setup_environment()


def is_git_installed() -> bool:
    """Check if Git is installed on the system

    Returns:
        bool: True if Git is installed, False otherwise.
    """
    try:
        subprocess.run(
            ["git", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def git_install_instructions() -> None:
    """Print instructions for installing Git on the system."""
    os_name = platform.system().lower()
    if "windows" in os_name:
        print(
            "Git is not installed. Please download and install it from https://git-scm.com/download/win."
        )
    elif "linux" in os_name:
        print(
            "Git is not installed. You can typically install it using your package manager. e.g., 'sudo apt install git'."
        )
    elif "darwin" in os_name:
        print(
            "Git is not installed. You can install it using Homebrew with the command 'brew install git'."
        )
    else:
        print("Unsupported operating system. Please install Git manually.")


def run_git_command(command: str) -> None:
    """Run a git command and print its output.

    Args:
        command (str): The Git command to run.
    """
    try:
        result = subprocess.run(
            command,
            check=True,
            shell=True,
            cwd=AOC_ROOT_DIR,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(result.stdout)
        print(result.stderr)
        print("Git command completed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error: Git command failed.")
        print(e.stdout)
        print(e.stderr)


def git_init() -> None:
    """Initialize Git"""
    run_git_command("git init")


def git_add_commit(day: Optional[int] = None, year: Optional[int] = None) -> None:
    """Add and commit changes to the Git repository.

    Args:
        day (Optional[int]): The day of the challenge. If None, it will be determined automatically.
        year (Optional[int]): The year of the challenge. If None, it will be determined automatically.
    """
    if not day or not year:
        day, year = get_day_and_year()
    default_commit_message = f"Add solution for day {day} of year {year}"
    commit_message = input(
        "Enter commit message (default: {}): ".format(default_commit_message)
    ).strip()

    if not commit_message:
        commit_message = default_commit_message

    run_git_command(f"git add {year}/day_{day:02}")
    run_git_command(f"git commit -m '{commit_message}'")


def git_push() -> None:
    """Push to GitHub"""
    run_git_command("git push origin main")


def perform_git_operations() -> None:
    """Perform Git operations based on user input."""
    if not is_git_installed():
        git_install_instructions()
        return

    choice = input(
        "Choose an operation:\n1. Initialize Git\n2. Add and commit\n3. Push to GitHub\nEnter your choice: "
    ).strip()
    if choice == "1":
        git_init()
    elif choice == "2":
        git_add_commit()
    elif choice == "3":
        git_push()
    else:
        print(f"Invalid choice: {choice}")


if __name__ == "__main__":
    perform_git_operations()
