import time
from functools import wraps


def infer_type(value):
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def detect_file_input_format(file_path="input.txt"):
    try:
        with open(file_path, "r") as file:
            first_line = file.readline()
            if "," in first_line:
                return "comma"
            else:
                return "line"
    except FileNotFoundError:
        return "unknown"


def format_example_data(example_data, format_type):
    return example_data.replace(", ", "\n") if format_type == "line" else example_data


def parse_number_of_examples(lines):
    example_line = next((line for line in lines if "Example data" in line), "")
    num_examples = int(example_line.split("/")[-1].split()[0]) if example_line else 0
    return num_examples


def extract_example_data_and_answers():
    input_format = detect_file_input_format("example.txt")

    try:
        with open("example.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Error: 'example.txt' not found.")
        return []

    num_of_examples = parse_number_of_examples(lines)
    example_data_and_answers = []

    for example_num in range(1, num_of_examples + 1):
        example_data, data_end_index = parse_example_data(lines, example_num)
        formatted_data = format_example_data(example_data, input_format)
        answer_a, answer_b = parse_example_answers(lines, data_end_index)
        example_data_and_answers.append((formatted_data, answer_a, answer_b))

    return example_data_and_answers


def parse_example_data(lines, example_num):
    example_start_line = f"Example data {example_num}"
    example_start_index = next(
        (i for i, line in enumerate(lines) if example_start_line in line), -1
    )

    if example_start_index == -1:
        return "", -1

    data_start = example_start_index + 1
    data_end = next(
        (i for i, line in enumerate(lines, data_start) if "------" in line), -1
    )

    example_data = "".join(lines[data_start : data_end - 1]).strip()
    return example_data, data_end


def parse_example_answers(lines, data_end_index):
    answers_start = data_end_index
    answers = lines[answers_start : answers_start + 2]

    answer_a = answers[0].split(":")[1].strip() if "answer_a:" in answers[0] else None
    answer_b = answers[1].split(":")[1].strip() if "answer_b:" in answers[1] else None

    return answer_a, answer_b


def profile(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        exec_time = end_time - start_time
        return result, exec_time

    return wrapper


def print_and_check_results(
    part: str, result: str, expected_answer: str, exec_time: float
) -> None:
    """
    Prints the result in a structured format and checks it against the expected answer.

    Args:
        part: A string indicating the part of the solution (e.g., 'part a').
        result: The result to be printed and checked.
        expected_answer: The expected answer to check against.
        exec_time: Execution time of the solution function.
    """
    print(f"{part.capitalize()}:")

    if expected_answer == "-":
        print("    - Status: Answer not available.")
    elif result != "not implemented":
        print(f"    - Result: {result}")
        print(f"    - Expected: {expected_answer}")
        print(
            f"    - Status: {'Correct!' if str(result) == expected_answer else 'Incorrect.'}"
        )
        print(f"    - Execution Time: {exec_time:.4f} seconds")
    else:
        print("    - Status: Not implemented yet.")


def print_result(part: str, result_tuple) -> None:
    """
    Prints the result for a given part of the solution.

    Args:
        part: A string indicating the part of the solution (e.g., 'part a').
        result_tuple: The tuple containing the result and execution time.
    """
    result, exec_time = result_tuple
    if result != "not implemented":
        print(f"Result for {part}: {result} (Executed in {exec_time:.4f} seconds)\n")
    else:
        print(f"{part}: Not implemented yet.")


def run_example(
    example_data_and_answers, read_data, solution_part_a, solution_part_b
) -> None:
    for example_num, (example_data, answer_a, answer_b) in enumerate(
        example_data_and_answers, start=1
    ):
        print(f"\nRunning Example {example_num}:\n{'-' * 20}")

        data = read_data(example_data)

        if answer_a != "-":
            result_a, exec_time_a = solution_part_a(data)
            print_and_check_results("part a", result_a, answer_a, exec_time_a)
        else:
            print_and_check_results("part a", "-", "-", 0)

        if answer_b != "-":
            result_b, exec_time_b = solution_part_b(data)
            print_and_check_results("part b", result_b, answer_b, exec_time_b)
        else:
            print_and_check_results("part b", "-", "-", 0)


def run_real_data(read_data, solution_part_a, solution_part_b) -> None:
    """
    Runs the real data case using the provided solution functions.

    Args:
        read_data: Function to read the input data.
        solution_part_a: Function for solving part A of the problem.
        solution_part_b: Function for solving part B of the problem.
    """


def run_real_data(read_data, solution_part_a, solution_part_b):
    try:
        with open("input.txt", "r") as file:
            file_contents = file.read()
    except FileNotFoundError:
        print("Error: 'input.txt' not found.")
        return

    data = read_data(file_contents)

    result_a = solution_part_a(data)
    print_result("part a", result_a)

    result_b = solution_part_b(data)
    print_result("part b", result_b)
