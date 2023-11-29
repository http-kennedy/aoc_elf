# aoc_elf: Advent of Code Utility Script

## Description

`aoc_elf` is a Python utility designed to streamline the experience of participating in the [Advent of Code](https://adventofcode.com/) (AoC) challenges. It provides a range of features to set up `AoC solutions environments`, `fetch puzzle inputs|examples`, and `submit answers to AoC puzzles`. There is also a prebuilt `python solution template` that provides `runtime metrics` and ability to `test against example input`.

## Features

- **Setup AoC Environment**: Automate the creation of directories and copy solution templates for AoC puzzles.
- **Fetch Puzzle Input**: Retrieve puzzle inputs and example inputs for specified AoC days and years.
- **Submit Answers**: Interface for submitting answers to AoC puzzles.
- **Python Solution Template & Helper**: Prebuilt python solution template copied into AoC environment with helper script.
- **Python solution Metrics**: When using the prebuilt solution template you will get runtime metrics.
- **Run Python Solution against Example**: Ability to run your solution against example input.

## Requirements

- Python 3.x
- Access to command-line/terminal

## Installation

1. Clone the repository: `git clone https://github.com/http-kennedy/aoc_elf.git`
2. Navigate to the cloned directory: `cd aoc_elf`
3. `pip install -r requirements.txt`

## Usage

To access the main functions:

```bash
python aoc_elf.py
```

Follow the on-screen menu to select and execute various operations.
___________________________________

To run your solution against the example input:

```bash
cd /your/aoc/solutions/environment/YYYY/day_DD/

python solution.py --example
```


## Configuration

- **Modifying Configurations**: You can change configurations by selecting the `Setup|Modify aoc_elf configurations` option in the menu.

## Contributing

Contributions to `aoc_elf` are welcome.

## Acknowledgments

Special thanks to [Advent of Code](https://adventofcode.com/) for providing engaging and challenging programming puzzles.
