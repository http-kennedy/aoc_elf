import os
import argparse
from helper import (
    extract_example_data_and_answers,
    run_example,
    run_real_data,
    profile,
    infer_type,
)


def read_data(data):
    return [infer_type(line.strip()) for line in data.splitlines()]


@profile
def solution_part_a(data):
    return "not implemented"


@profile
def solution_part_b(data):
    return "not implemented"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Advent of Code solution.")
    parser.add_argument("--example", action="store_true", help="Use example data")
    args = parser.parse_args()

    if args.example:
        try:
            example_data_and_answers = extract_example_data_and_answers()
            run_example(
                example_data_and_answers, read_data, solution_part_a, solution_part_b
            )
        except Exception as e:
            print(f"Error processing example.txt:\n\n {e}\n")
            print("This format of example.txt is not currently supported.")

    else:
        run_real_data(read_data, solution_part_a, solution_part_b)
