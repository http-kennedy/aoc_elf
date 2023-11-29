import os
import json
import re
import time
import glob
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from dateutil.parser import parse
from dateutil.tz import tzlocal
from aocd.models import Puzzle, User
from aocd import submit
from utils.environment import setup_environment
from utils.aoc_data import (
    get_day_and_year,
    check_and_update_example_input,
    get_day_directory,
    AOC_ROOT_DIR,
)
from aoc_elf import aocd_dir


def setup_user_session() -> str:
    """
    Sets up the user session for Advent of Code.

    Returns:
        The session token as a string.
    """
    _, _, _, AOC_SESSION = setup_environment()
    return AOC_SESSION


def prompt_for_part_and_answer() -> tuple[str, str]:
    """
    Prompts the user to enter the part of the challenge and the answer.

    Returns:
        A tuple containing the part of the challenge ('a' or 'b') and the answer as strings.
    """
    while True:
        part = input("Enter the part (a or b): ").strip().lower()
        if part in ["a", "b"]:
            break
        else:
            print("Invalid input. Please enter 'a' or 'b'.")

    answer = input("Enter the answer: ").strip()
    return part, answer


def parse_wait_time(message: str) -> timedelta:
    """
    Parses the wait time from a given message string.

    Args:
        message: The message containing the wait time information.

    Returns:
        A timedelta object representing the wait time.
    """
    wait_time_match = re.search(
        r"You have (\d+)m (\d+)s left to wait.", message, re.IGNORECASE
    )
    if wait_time_match:
        minutes, seconds = map(int, wait_time_match.groups())
        return timedelta(minutes=minutes, seconds=seconds)

    if "one minute" in message:
        return timedelta(minutes=1)

    minutes_wait_match = re.search(
        r"please wait (\d+) minutes before trying again", message, re.IGNORECASE
    )
    if minutes_wait_match:
        minutes = int(minutes_wait_match.group(1))
        return timedelta(minutes=minutes)

    return timedelta()


def read_last_submission_feedback() -> dict:
    """
    Reads the last submission feedback from stored JSON files.

    Returns:
        A dictionary containing the feedback of the last submission.
    """
    if not os.path.exists(aocd_dir):
        return None

    post_files = glob.glob(os.path.join(aocd_dir, "**/*_post.json"), recursive=True)

    latest_valid_feedback = None
    latest_submission_time = None

    for feedback_file in post_files:
        with open(feedback_file, "r") as file:
            data = json.load(file)
            if data:
                latest_feedback = data[-1]
                submission_time = parse(latest_feedback["when"])

                if "wait" in latest_feedback.get("message", ""):
                    if (
                        latest_submission_time is None
                        or submission_time > latest_submission_time
                    ):
                        latest_valid_feedback = latest_feedback
                        latest_submission_time = submission_time

    return latest_valid_feedback


def display_countdown_timer(remaining_time: timedelta) -> None:
    """
    Displays a countdown timer for the given remaining time.

    Args:
        remaining_time: The remaining time as a timedelta object.
    """
    while remaining_time.total_seconds() > 0:
        mins, secs = divmod(int(remaining_time.total_seconds()), 60)
        timer = f"{mins:02d}:{secs:02d}"
        print(f"Rate limit in effect. Please wait: {timer}", end="\r")
        time.sleep(1)
        remaining_time -= timedelta(seconds=1)
    print("\nYou may now submit your answer.")


def calculate_remaining_wait_time() -> timedelta:
    """
    Calculates the remaining wait time based on the last submission feedback.

    Returns:
        A timedelta object representing the remaining wait time.
    """
    feedback = read_last_submission_feedback()
    if feedback and "wait" in feedback.get("message", ""):
        wait_time = parse_wait_time(feedback["message"])
        submission_time = parse(feedback["when"])
        current_time = datetime.now(tz=tzlocal())
        elapsed_time = current_time - submission_time
        remaining_time = wait_time - elapsed_time
        return max(remaining_time, timedelta(0))

    return timedelta()


def submit_answer_attempt(
    year: int, day: int, part: str, answer: str, session: str
) -> None:
    """
    Attempts to submit an answer to the Advent of Code website.

    Args:
        year: The year of the challenge.
        day: The day of the challenge.
        part: The part of the challenge ('a' or 'b').
        answer: The answer to submit.
        session: The session token for authentication.
    """
    user = User(token=session)
    puzzle = Puzzle(year=year, day=day, user=user)
    response = puzzle.answered(part)
    if response:
        print(
            f"Answer for part {part} of day {day} of year {year} has already been submitted."
        )
        return

    remaining_wait_time = calculate_remaining_wait_time()
    if remaining_wait_time.total_seconds() > 0:
        display_countdown_timer(remaining_wait_time)
    else:
        try:
            submission_result = submit(
                answer, part=part, year=year, day=day, session=session, quiet=True
            )

            submission_result_data = submission_result.data.decode("utf-8")
            soup = BeautifulSoup(submission_result_data, "html.parser")
            article = soup.find("article")

            if article:
                paragraphs = article.find_all("p")
                for paragraph in paragraphs:
                    text = paragraph.get_text(" ", strip=True)
                    if "You have completed Day" in text:
                        completion_message = text.split("You have completed Day")[0]
                        print("\n" + completion_message)
                        break
                    elif "[Continue to Part Two]" in text:
                        day_dir = get_day_directory(year, day, AOC_ROOT_DIR)
                        check_and_update_example_input(day, year, day_dir)
            else:
                print("\nFailed to submit answer.")
        except Exception as e:
            print("\n" + str(e))


def submit_answer() -> None:
    """
    Handles the entire process of submitting an answer, including user prompts and submission.
    """
    session = setup_user_session()
    if not session:
        print(
            "Session token not found. Please run 'python aoc.py' and choose option 0 to set up your session token."
        )
        return

    print("\nSubmit an answer for a specific 'year', 'day', and 'part'.")
    day, year = get_day_and_year()
    part, answer = prompt_for_part_and_answer()
    submit_answer_attempt(year, day, part, answer, session)


if __name__ == "__main__":
    submit_answer()
