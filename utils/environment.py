import os
from dotenv import load_dotenv
from utils.config import setup_config, ENV_FILE


def check_env_exists() -> bool:
    """
    Checks if the .env file exists and contains all required environment variables.

    Returns:
        True if the .env file exists and all required environment variables are set,
        otherwise False.
    """
    required_env_vars = ["BASE_DIR", "GITHUB_REPO", "AOC_SESSION"]
    env_exists = True

    if not os.path.exists(ENV_FILE):
        env_exists = False
    else:
        load_dotenv()
        for var in required_env_vars:
            if not os.getenv(var):
                env_exists = False
                break

    if not env_exists:
        setup_config()
        return False

    return True


def setup_environment() -> tuple[str, str, str, str]:
    """
    Loads environment variables from the .env file.

    Returns:
        A tuple containing the BASE_DIR, AOC_ROOT_DIR, GITHUB_REPO, and AOC_SESSION.
    """
    load_dotenv()

    BASE_DIR = os.getenv("BASE_DIR")
    AOC_ROOT_DIR = os.path.join(BASE_DIR, "aoc_solutions")
    GITHUB_REPO = os.getenv("GITHUB_REPO")
    AOC_SESSION = os.getenv("AOC_SESSION")

    return BASE_DIR, AOC_ROOT_DIR, GITHUB_REPO, AOC_SESSION


def unused_env_vars(BASE_DIR: str, GITHUB_REPO: str, AOC_SESSION: str) -> list[str]:
    """
    Identifies any unused environment variables.

    Args:
        BASE_DIR: The base directory path.
        GITHUB_REPO: The GitHub repository URL.
        AOC_SESSION: The AOC session token.

    Returns:
        A list of strings representing the names of unused environment variables.
    """
    unused_envs = []

    if not BASE_DIR or BASE_DIR.lower() == "none":
        unused_envs.append("BASE_DIR")
    if not GITHUB_REPO or GITHUB_REPO.lower() == "none":
        unused_envs.append("GITHUB_REPO")
    if not AOC_SESSION or AOC_SESSION.lower() == "none":
        unused_envs.append("AOC_SESSION")

    return unused_envs
