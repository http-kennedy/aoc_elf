import time
import argparse
import colorama
from functools import wraps
from colorama import Fore, Style
from typing import Callable, List, Optional, Tuple

colorama.init(autoreset=True)

# Global variables
debug_mode = False
debug_helper_mode = False
debug_solution_mode = False


# Common functions
def read_input(source: str, is_file: bool = True) -> List[str]:
    """
    Reads input data from a file or a string.

    Args:
    source (str): Path to the input file or a string containing the input.
    is_file (bool): Flag to indicate whether the source is a file path or a string.

    Returns:
    List[str]: A list of lines from the input source.
    """
    if is_file:
        with open(source, "r") as file:
            return [line.strip() for line in file]
    else:
        return [line.strip() for line in source.splitlines()]


def profile(func: Callable) -> Callable:
    """
    A decorator to profile the execution time of a function.

    Args:
    func (Callable): The function to be profiled.

    Returns:
    Callable: The wrapped function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        exec_time = end_time - start_time
        return result, exec_time

    return wrapper


def execute_solutions(
    solution_p1: Callable,
    solution_p2: Callable,
    data: List[str],
    args: argparse.Namespace,
    answer_a: Optional[str] = None,
    answer_b: Optional[str] = None,
    is_example: bool = False,
) -> Tuple[bool, bool]:
    """
    Executes the provided solution functions and checks their results.

    Args:
    solution_p1 (Callable): Function for solution part 1.
    solution_p2 (Callable): Function for solution part 2.
    data (List[str]): Input data for the puzzle.
    args (argparse.Namespace): Parsed command line arguments.
    answer_a (Optional[str]): Expected answer for part 1 in example mode.
    answer_b (Optional[str]): Expected answer for part 2 in example mode.
    is_example (bool): Flag to indicate example mode.

    Returns:
    Tuple[bool, bool]: Tuple indicating whether each solution part returned None.
    """
    no_solution_p1 = False
    no_solution_p2 = False

    # Execute and check result for Part 1
    if args.p1 or not (args.p1 or args.p2):
        no_solution_p1 |= execute_and_print_solution(
            solution_p1, data, answer_a, part=1, is_example=is_example
        )

    # Execute and check result for Part 2
    if args.p2 or not (args.p1 or args.p2):
        no_solution_p2 |= execute_and_print_solution(
            solution_p2, data, answer_b, part=2, is_example=is_example
        )

    return no_solution_p1, no_solution_p2


def execute_and_print_solution(
    solution_func: Callable,
    data: List[str],
    expected_answer: Optional[str],
    part: int,
    is_example: bool = False,
) -> bool:
    """
    Executes a solution function, prints the result, and checks if the result is None.

    Args:
    solution_func (Callable): The solution function to execute.
    data (List[str]): Input data for the puzzle.
    expected_answer (Optional[str]): The expected answer for comparison.
    part (int): The part number of the puzzle (1 or 2).
    is_example (bool): Flag to indicate if it's an example run.

    Returns:
    bool: True if the solution returned None, False otherwise.
    """
    result, exec_time = solution_func(data)

    if is_example and expected_answer is None:
        print(f"Solution Part {part}: No answer provided in example.txt")
        return False

    if result is None:
        print_separator()
        print(f"Solution Part {part}: returns {red_text('None')}.")
        return True  # Return True if result is None
    else:
        if is_example:
            print_example_result(result, expected_answer, exec_time, part)
        else:
            print_solution_result(result, exec_time, part)
        return False  # Return False if result is not None


def parse_arguments() -> argparse.Namespace:
    """
    Parses and returns command line arguments for the puzzle solver.

    Returns:
    argparse.Namespace: Parsed command line arguments.
    """
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
    debug_helper_mode = args.debug_helper or args.debug_all
    debug_solution_mode = args.debug_solution or args.debug_all
    return args


def print_running_mode(args: argparse.Namespace, mode: str = "real input") -> None:
    """
    Prints the current running mode of the puzzle solver.

    Args:
    args (argparse.Namespace): Parsed command line arguments.
    mode (str): The mode of operation, either 'real input' or 'example'.
    """
    if args.p1 and not args.p2:
        print(yellow_text(f"Running {mode} data against solution_p1."))
    elif args.p2 and not args.p1:
        print(yellow_text(f"Running {mode} data against solution_p2."))
    else:
        print(
            yellow_text(f"Running {mode} data against both solution_p1 && solution_p2.")
        )


def determine_and_print_solution_message(
    no_solution_p1: bool, no_solution_p2: bool
) -> None:
    """
    Determines and prints a message based on whether solution parts returned None.

    Args:
    no_solution_p1 (bool): Indicates if solution part 1 returned None.
    no_solution_p2 (bool): Indicates if solution part 2 returned None.
    """
    if no_solution_p1 and no_solution_p2:
        print_no_solution_message("Both solutions")
    elif no_solution_p1:
        print_no_solution_message("Solution Part 1:")
    elif no_solution_p2:
        print_no_solution_message("Solution Part 2:")


def print_no_solution_message(solution_name):
    if solution_name == "Both solutions":
        message = "Both solutions seem to be enjoying a coffee break! ☕"
    else:
        message = f"{solution_name} seems to be enjoying a coffee break! ☕"

    print_separator()
    print("\n" + purple_text(message))
    print(green_text("Need help? Try running: python solution.py --help"))


def print_separator() -> None:
    """
    Prints a separator line.
    """
    print(purple_text("-" * 50))


def green_text(text: str) -> str:
    """
    Formats the given text with a green color.

    Args:
    text (str): The text to format.

    Returns:
    str: The formatted text.
    """
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}"


def yellow_text(text: str) -> str:
    """
    Formats the given text with a yellow color.

    Args:
    text (str): The text to format.

    Returns:
    str: The formatted text.
    """
    return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"


def red_text(text: str) -> str:
    """
    Formats the given text with a red color.

    Args:
    text (str): The text to format.

    Returns:
    str: The formatted text.
    """
    return f"{Fore.RED}{text}{Style.RESET_ALL}"


def purple_text(text: str) -> str:
    """
    Formats the given text with a purple color.

    Args:
    text (str): The text to format.

    Returns:
    str: The formatted text.
    """
    return f"{Fore.MAGENTA}{text}{Style.RESET_ALL}"


# Example-specific functions
def parse_example_data(
    file_path: str = "example.txt",
) -> List[Tuple[str, Optional[str], Optional[str]]]:
    """
    Parses example data and expected answers from a given file.

    Args:
    file_path (str): Path to the file containing the example data.

    Returns:
    List[Tuple[str, Optional[str], Optional[str]]]: A list containing tuples of example data and expected answers for part 1 and 2.
    """
    examples = []
    with open(file_path, "r") as file:
        content = file.read()

    example_sections = content.split(
        "--------------------------------------------------------------------------------"
    )

    extended_sections = []
    for i in range(0, len(example_sections) - 1, 2):
        extended_section = example_sections[i] + example_sections[i + 1]
        extended_sections.append(extended_section)

    for section in extended_sections:
        if "Example data" in section:
            lines = section.splitlines()

            if debug_helper_mode:
                print(f"{green_text('Section:')} \n{section}")

            try:
                start_idx = (
                    next(i for i, line in enumerate(lines) if "Example data" in line)
                    + 1
                )

                end_idx = next(
                    (i for i, line in enumerate(lines) if line.startswith("answer_a:")),
                    len(lines),
                )

                example_data = "\n".join(lines[start_idx:end_idx]).strip()
                answer_a = (
                    lines[end_idx].split(": ")[1] if end_idx < len(lines) else None
                )
                answer_b = (
                    lines[end_idx + 1].split(": ")[1]
                    if end_idx + 1 < len(lines)
                    else None
                )

                if debug_helper_mode:
                    print(f"{green_text('Example data:')} \n{example_data}")
                    print(
                        f"\n{green_text('Extracted answers:')} \np1: {answer_a}, p2: {answer_b}\n"
                    )

                examples.append((example_data, answer_a, answer_b))
            except (IndexError, ValueError) as e:
                if debug_helper_mode:
                    print(f"{red_text('Error parsing section:')} {str(e)}")
                    print(f"{red_text('Lines in section:')} {str(lines)}")

    return examples


def run_example_solutions(
    solution_p1: Callable, solution_p2: Callable, args: argparse.Namespace
) -> None:
    """
    Runs the provided solution functions against example data.

    Args:
    solution_p1 (Callable): Function for solution part 1.
    solution_p2 (Callable): Function for solution part 2.
    args (argparse.Namespace): Parsed command line arguments.
    """
    print_running_mode(args, mode="example")
    examples = parse_example_data()

    overall_no_solution_p1 = False
    overall_no_solution_p2 = False

    for i, (example_data, answer_a, answer_b) in enumerate(examples, start=1):
        print_separator()
        print(f"{green_text(f'Using example data {i}')}:")
        data = read_input(example_data, is_file=False)

        no_solution_p1, no_solution_p2 = execute_solutions(
            solution_p1, solution_p2, data, args, answer_a, answer_b, is_example=True
        )

        overall_no_solution_p1 |= no_solution_p1
        overall_no_solution_p2 |= no_solution_p2

    determine_and_print_solution_message(overall_no_solution_p1, overall_no_solution_p2)


def print_example_result(
    result: Optional[str], expected_answer: str, exec_time: float, part: int
) -> None:
    """
    Prints the result of an example solution, comparing it with the expected answer and displaying the execution time.

    Args:
    result (Optional[str]): The result obtained from the solution function.
    expected_answer (str): The expected answer for the example.
    exec_time (float): The execution time of the solution function.
    part (int): The part number of the puzzle (1 or 2).

    """
    if result is None:
        print(f"Solution Part {part} returns {red_text('None')}")
    else:
        result_text = (
            green_text(result) if str(result) == expected_answer else red_text(result)
        )
        print(
            f"Example Part {part}: Expected Result: '{expected_answer}' | Actual Result: '{result_text}' -> Execution Time: '{exec_time:.6f}' seconds."
        )
        print_separator()


# Real-input specific functions
def run_solutions(
    file_path: str,
    solution_p1: Callable,
    solution_p2: Callable,
    args: argparse.Namespace,
) -> None:
    """
    Runs the provided solution functions against real input data.

    Args:
    file_path (str): Path to the file containing the real input data.
    solution_p1 (Callable): Function for solution part 1.
    solution_p2 (Callable): Function for solution part 2.
    args (argparse.Namespace): Parsed command line arguments.
    """
    print_running_mode(args)
    data = read_input(file_path)

    no_solution_p1, no_solution_p2 = execute_solutions(
        solution_p1, solution_p2, data, args
    )

    determine_and_print_solution_message(no_solution_p1, no_solution_p2)


def print_solution_result(result: Optional[str], exec_time: float, part: int) -> None:
    """
    Prints the result of a solution along with its execution time.

    Args:
    result (Optional[str]): The result of the solution function.
    exec_time (float): The execution time of the solution.
    part (int): The part number of the puzzle (1 or 2).
    """
    if result is None:
        print_separator()
        print(f"Solution Part {part}: returns {red_text('None')}.")
    else:
        print_separator()
        print(
            f"Solution Part {part}: '{green_text(result)}' -> Execution Time: '{green_text(f'{exec_time:.6f}')}' seconds."
        )
        print_separator()
