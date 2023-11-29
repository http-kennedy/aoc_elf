import time


def split_example_file() -> None:
    """
    Reads the content from 'example.txt', splits it into example input data
    and answers, and then writes them to 'example_input.txt' and
    'example_answers.txt' respectively.
    """
    with open("example.txt", "r") as file:
        lines = file.readlines()

    data_start = (
        lines.index(
            "------------------------------- Example data 1/1 -------------------------------\n"
        )
        + 1
    )
    data_end = lines.index(
        "--------------------------------------------------------------------------------\n",
        data_start,
    )

    example_data = lines[data_start:data_end]
    answers = [line for line in lines[data_end:] if "answer_" in line]

    with open("example_input.txt", "w") as file:
        file.writelines(example_data)

    with open("example_answers.txt", "w") as file:
        file.writelines(answers)


def read_example_answers() -> tuple[str, str]:
    """
    Reads answers from 'example_answers.txt' and returns them.

    Returns:
        A tuple containing two strings: answer_a and answer_b.
    """
    with open("example_answers.txt", "r") as ans_file:
        answers = ans_file.readlines()
        answer_a = answers[0].split(":")[1].strip()
        answer_b = answers[1].split(":")[1].strip() if "-" not in answers[1] else None
        return answer_a, answer_b


def print_and_check_results(part: str, result: str, expected_answer: str) -> None:
    """
    Prints the result and checks it against the expected answer.

    Args:
        part: A string indicating the part of the solution (e.g., 'part a').
        result: The result to be printed and checked.
        expected_answer: The expected answer to check against.
    """
    if result != "not implemented":
        result_str = str(result)
        print(f"Result for {part}:", result)
        print(f"Expected answer ({part}):", expected_answer)
        print(f"{part}:", "Correct!" if result_str == expected_answer else "Incorrect.")
    else:
        print(f"{part}: Not implemented yet.")


def print_result(part: str, result: str) -> None:
    """
    Prints the result for a given part of the solution.

    Args:
        part: A string indicating the part of the solution (e.g., 'part a').
        result: The result to be printed.
    """
    if result != "not implemented":
        print(f"Result for {part}:", result)
    else:
        print(f"{part}: Not implemented yet.")


def timed_run(solution_function, data):
    """
    Executes the solution function with the provided data and measures the execution time.

    Args:
        solution_function: The solution function to be executed.
        data: The data to be passed to the solution function.

    Returns:
        The result of the solution function and the time taken to execute it in seconds.
    """
    start_time = time.perf_counter()
    result = solution_function(data)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    return result, execution_time


def run_example(read_data, solution_part_a, solution_part_b) -> None:
    """
    Runs the example case using the provided solution functions.

    Args:
        read_data: Function to read the input data.
        solution_part_a: Function for solving part A of the problem.
        solution_part_b: Function for solving part B of the problem.
    """
    data = read_data("example_input.txt")
    answer_a, answer_b = read_example_answers()

    result_a, time_a = timed_run(solution_part_a, data)
    print_and_check_results("part a", result_a, answer_a)
    print(f"Execution time (part a): {time_a:.4f} seconds.\n")

    if answer_b is not None:
        result_b, time_b = timed_run(solution_part_b, data)
        print_and_check_results("part b", result_b, answer_b)
        print(f"Execution time (part b): {time_b:.4f} seconds.\n")
    else:
        print("Part B: Answer not available.")


def run_real_data(read_data, solution_part_a, solution_part_b) -> None:
    """
    Runs the real data case using the provided solution functions.

    Args:
        read_data: Function to read the input data.
        solution_part_a: Function for solving part A of the problem.
        solution_part_b: Function for solving part B of the problem.
    """
    data = read_data("input.txt")

    result_a, time_a = timed_run(solution_part_a, data)
    if result_a != "not implemented":
        print_result("part a", result_a)
        print(f"Execution time (part a): {time_a:.4f} seconds.\n")
    else:
        print_result("part a", result_a)

    result_b, time_b = timed_run(solution_part_b, data)
    if result_b != "not implemented":
        print_result("part b", result_b)
        print(f"Execution time (part b): {time_b:.4f} seconds")
    else:
        print_result("part b", result_b)
