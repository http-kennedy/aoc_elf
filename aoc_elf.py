import os
import platform
from utils.environment import (
    check_env_exists,
    setup_environment,
    unused_env_vars,
    initialize_environment,
)

BASE_DIR, GITHUB_REPO, AOC_SESSION = None, None, None

main_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
aocd_dir = os.path.join(".aocd_cache")
os.environ["AOCD_DIR"] = aocd_dir


def clear_screen() -> None:
    """
    Clears the terminal screen based on the operating system.
    """
    if platform.system().lower() == "windows":
        os.system("cls")
    else:
        os.system("clear")


def display_menu() -> None:
    """
    Displays the main menu options to the user.
    """
    clear_screen()

    print(
        " .----------------. .----------------. .----------------. .----------------. .----------------. .----------------. .----------------."
    )
    print(
        "| .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. |"
    )
    print(
        "| |      __      | | |     ____     | | |     ______   | | |              | | |  _________   | | |   _____      | | |  _________   | |"
    )
    print(
        "| |     /  \     | | |   .'    `.   | | |   .' ___  |  | | |              | | | |_   ___  |  | | |  |_   _|     | | | |_   ___  |  | |"
    )
    print(
        "| |    / /\ \    | | |  /  .--.  \  | | |  / .'   \_|  | | |              | | |   | |_  \_|  | | |    | |       | | |   | |_  \_|  | |"
    )
    print(
        "| |   / ____ \   | | |  | |    | |  | | |  | |         | | |              | | |   |  _|  _   | | |    | |   _   | | |   |  _|      | |"
    )
    print(
        "| | _/ /    \ \_ | | |  \  `--'  /  | | |  \ `.___.'\  | | |              | | |  _| |___/ |  | | |   _| |__/ |  | | |  _| |_       | |"
    )
    print(
        "| ||____|  |____|| | |   `.____.'   | | |   `._____.'  | | |   _______    | | | |_________|  | | |  |________|  | | | |_____|      | |"
    )
    print(
        "| |              | | |              | | |              | | |  |_______|   | | |              | | |              | | |              | |"
    )
    print(
        "| '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' |"
    )
    print(
        "'----------------' '----------------' '----------------' '----------------' '----------------' '----------------' '----------------'"
    )

    print(
        "To provide any contributions to the project visit -> https://github.com/http-kennedy/aoc_elf"
    )
    print(
        "\nNOTE: For any option that requires a 'year' and 'day' during December 01-25 (system date) the defaults will be set to current 'year' and 'day'.\n"
    )
    print("\nChoose an option:")
    print("0. Setup|Modify aoc_elf configurations.")
    print("1. Create AoC solutions environment.")
    print("2. Fetch AoC input and example data.")
    print("3. Submit AoC answer.")
    print("4. Perform Git operations **EXPERIMENTAL && UNTESTED -> DO NOT USE**")
    print("5. Exit")


def main() -> None:
    """
    Main function of the application. Handles the user interface and menu selection.
    """
    from utils.config import setup_config
    from utils.file_operations import setup_aoc_environment
    from utils.aoc_data import fetch_data_for_day
    from utils.answer_submission import submit_answer
    from utils.git_operations import perform_git_operations

    global BASE_DIR, GITHUB_REPO, AOC_SESSION
    BASE_DIR, _, GITHUB_REPO, AOC_SESSION = initialize_environment()
    unused_envs = unused_env_vars(BASE_DIR, GITHUB_REPO, AOC_SESSION)

    try:
        while True:
            display_menu()
            choice = input("\nEnter your choice: ").strip()

            if choice == "0":
                setup_config()
                (
                    BASE_DIR,
                    _,
                    GITHUB_REPO,
                    AOC_SESSION,
                ) = setup_environment()  # Refresh variables after config update
                unused_envs = unused_env_vars(BASE_DIR, GITHUB_REPO, AOC_SESSION)
            elif choice == "1":
                if "BASE_DIR" in unused_envs:
                    print(
                        "\nYour base directory has not been set. Please run option 0 before using this feature."
                    )
                else:
                    setup_aoc_environment()
            elif choice == "2":
                if "BASE_DIR" in unused_envs or "AOC_SESSION" in unused_envs:
                    print(
                        "\nYour base directory and/or AOC session token has not been set. Please run option 0 before using this feature."
                    )
                else:
                    fetch_data_for_day()
            elif choice == "3":
                if "AOC_SESSION" in unused_envs:
                    print(
                        "\nYour AOC session token has not been set. Please run option 0 before using this feature."
                    )
                else:
                    submit_answer()
            elif choice == "4":
                if "GITHUB_REPO" in unused_envs:
                    print(
                        "\nYour GitHub repository has not been set. Please run option 0 before using this feature."
                    )
                else:
                    perform_git_operations()
            elif choice == "5":
                print("Exiting...")
                break
            else:
                print(f"Invalid choice: {choice}")

            input("\nPress Enter to continue...")
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user. Exiting...")


if __name__ == "__main__":
    main()
