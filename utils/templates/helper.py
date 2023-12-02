import time
import argparse
import colorama
from functools import wraps
from colorama import Fore, Style

colorama.init(autoreset=True)


debug_mode = False
debug_helper_mode = False
debug_solution_mode = False


def read_input(source, is_file=True):
    if is_file:
        with open(source, "r") as file:
            return [line.strip() for line in file]
    else:
        return [line.strip() for line in source.splitlines()]


def profile(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        exec_time = end_time - start_time
        return result, exec_time

    return wrapper


def run_solutions(file_path, solution_p1, solution_p2, args):
    data = read_input(file_path)

    if args.p1 or not (args.p1 or args.p2):
        result_p1, time_p1 = solution_p1(data, debug_mode)
        print(
            f"Solution Part 1: '{green_text(result_p1)}' -> Execution Time: '{green_text(f'{time_p1:.6f}')}' seconds.\n"
        )

    if args.p2 or not (args.p1 or args.p2):
        result_p2, time_p2 = solution_p2(data, debug_mode)
        print(
            f"Solution Part 2: '{green_text(result_p2)}' -> Execution Time: '{green_text(f'{time_p2:.6f}')}' seconds."
        )


def run_examples(solution_p1, solution_p2):
    examples = parse_example_data()
    for i, (example_data, answer_a, answer_b) in enumerate(examples, start=1):
        print(f"\nRunning Example {i}:")

        data = read_input(example_data, is_file=False)

        result_p1, exec_time_p1 = solution_p1(data)
        result_color_p1 = Fore.GREEN if str(result_p1) == answer_a else Fore.RED
        print(
            f"Example Part 1: Expected Result: '{answer_a}' | Actual Result: '{result_color_p1}{result_p1}{Style.RESET_ALL}' -> Execution Time: '{exec_time_p1:.6f}' seconds."
        )

        result_p2, exec_time_p2 = solution_p2(data)
        result_color_p2 = Fore.GREEN if str(result_p2) == answer_b else Fore.RED
        print(
            f"Example Part 2: Expected Result: '{answer_b}' | Actual Result: '{result_color_p2}{result_p2}{Style.RESET_ALL}' -> Execution Time: '{exec_time_p2:.6f}' seconds."
        )


def parse_example_data(file_path="example.txt"):
    examples = []
    with open(file_path, "r") as file:
        content = file.read()

    example_sections = content.split(
        "--------------------------------------------------------------------------------"
    )

    # Extend each section to include the next set of hyphens
    extended_sections = []
    for i in range(0, len(example_sections) - 1, 2):
        extended_section = example_sections[i] + example_sections[i + 1]
        extended_sections.append(extended_section)

    for section in extended_sections:
        if "Example data" in section:
            lines = section.splitlines()
            debug_print("Section: \n", variable=section, helper_debug=True)

            try:
                # Find the start index of the example data
                start_idx = (
                    next(i for i, line in enumerate(lines) if "Example data" in line)
                    + 1
                )

                # Find the index of the line containing 'answer_a'
                end_idx = next(
                    (i for i, line in enumerate(lines) if line.startswith("answer_a:")),
                    len(lines),
                )

                # Extract example data and answers
                example_data = "\n".join(lines[start_idx:end_idx]).strip()
                answer_a = (
                    lines[end_idx].split(": ")[1] if end_idx < len(lines) else None
                )
                answer_b = (
                    lines[end_idx + 1].split(": ")[1]
                    if end_idx + 1 < len(lines)
                    else None
                )

                debug_print(
                    "Example data: \n", variable=example_data, helper_debug=True
                )
                debug_print(
                    "\nExtracted answers: \n",
                    variable=f"p1: {answer_a}, p2: {answer_b}\n",
                    helper_debug=True,
                )

                examples.append((example_data, answer_a, answer_b))
            except (IndexError, ValueError) as e:
                debug_print(
                    "Error parsing section: ", variable=str(e), helper_debug=True
                )
                debug_print(
                    "Lines in section: ", variable=str(lines), helper_debug=True
                )

    return examples


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run Advent of Code solutions.")
    parser.add_argument("--input", default="input.txt", help="Input file path")
    parser.add_argument("--example", action="store_true", help="Run examples")
    parser.add_argument("--p1", action="store_true", help="Run only Part 1")
    parser.add_argument("--p2", action="store_true", help="Run only Part 2")
    parser.add_argument(
        "--debug-all", action="store_true", help="Enable all debug messages"
    )
    parser.add_argument(
        "--debug-helper",
        action="store_true",
        help="Enable debug messages in helper.py only",
    )
    parser.add_argument(
        "--debug-solution",
        action="store_true",
        help="Enable debug messages in solution.py only",
    )
    args = parser.parse_args()
    global debug_mode, debug_helper_mode, debug_solution_mode
    debug_mode = args.debug_all
    debug_helper_mode = (
        args.debug_helper or args.debug_all
    )  # Enable helper debug if either flag is set
    debug_solution_mode = (
        args.debug_solution or args.debug_all
    )  # Enable solution debug if either flag is set
    return args


def green_text(text):
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}"


def red_text(text):
    return f"{Fore.RED}{text}{Style.RESET_ALL}"


def debug_print(message, variable="", helper_debug=False):
    if (debug_mode and not helper_debug) or (debug_helper_mode and helper_debug):
        colored_variable = green_text(variable) if variable else ""
        print(message + colored_variable)
