import os
import argparse
from helper import split_example_file, run_example, run_real_data


def read_data(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines()]


def solution_part_a(data):
    return "not implemented"


def solution_part_b(data):
    return "not implemented"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Advent of Code solution.")
    parser.add_argument("--example", action="store_true", help="Use example data")
    args = parser.parse_args()

    if args.example:
        try:
            split_example_file()
            run_example(read_data, solution_part_a, solution_part_b)
        except Exception as e:
            print(f"Error processing example.txt:\n\n {e}\n")
            print("This format of example.txt is not currently supported.")
    else:
        run_real_data(read_data, solution_part_a, solution_part_b)
