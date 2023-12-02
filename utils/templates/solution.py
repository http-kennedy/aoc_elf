import helper as helper


@helper.profile
def solution_p1(data, debug_mode: bool = False):
    """
    Placeholder for the solution to Part 1 of the puzzle.

    Args:
    data (list): Input data for the puzzle.
    debug_mode (bool): Flag to enable debugging mode.
    """
    if helper.debug_solution_mode:
        print(helper.green_text("Debugging is enabled in solution_p1"))
    return None


@helper.profile
def solution_p2(data, debug_mode: bool = False):
    """
    Placeholder for the solution to Part 2 of the puzzle.

    Args:
    data (list): Input data for the puzzle.
    debug_mode (bool): Flag to enable debugging mode.
    """
    if helper.debug_solution_mode:
        print(helper.green_text("\nDebugging is enabled in solution_p2"))
    return None


if __name__ == "__main__":
    args = helper.parse_arguments()
    if args.example:
        helper.run_example_solutions(solution_p1, solution_p2, args)
    else:
        helper.run_solutions(args.input, solution_p1, solution_p2, args)
