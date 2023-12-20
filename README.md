# NYT Spelling Bee Solver

## Overview
The NYT Spelling Bee Solver is a Python program designed to solve the New York Times Spelling Bee game. This game challenges players to form as many words as possible from a set of seven letters, with one designated as the "center" letter. The solver finds all valid words that can be created using these letters, including "pangrams" — words that use all seven letters.

## Features
- Prompts for user input of the center and outer letters.
- Command-line argument support for specifying letters.
- Validation of user inputs.
- Identification and listing of valid words and pangrams.

## Prerequisites
- Python 3.7 or higher

## Installation

Before running the program, install the necessary dependencies using the provided `requirements.txt` file. This can be done by running the following command in your terminal:

```bash
pip install -r requirements.txt
```

## Usage
The program can be run in two modes: interactive and command-line argument mode.

### Interactive Mode
Run the program without arguments. It will prompt you to enter the center and outer letters:

```bash
python bee_solver.py
```

### Command-Line Argument Mode
```bash
python bee_solver.py -c [center_letter] -l [outer_letters]
```

#### Arguments
- `-c`, `--center`: Specify the center letter (required).
- `-l`, `--letters`: Specify the outer letters (up to six characters).

Example:
```bash
python bee_solver.py -c e -l a b c k l o
```

## Input Requirements
- **Center Letter**: A single alphabetical character.
- **Outer Letters**: Up to six distinct alphabetical characters.

## Output
- A list of valid words, sorted alphabetically.
- The count of pangrams found.

## Example Output

```yaml
44 words, including 3 pangrams, were found:
	able
	allele
	allocable
    ...
```

## Troubleshooting/FAQ
**Q: The program is not accepting my input. What should I do?**
A: Ensure that you are entering single alphabetical characters for the center letter and up to six distinct alphabetical characters for the outer letters.

**Q: How do I stop the program?**
A: You can terminate the program at any time by pressing `Ctrl+C` in the terminal.

## Contributing
Contributions to the NYT Spelling Bee Solver are welcome! If you have suggestions for improvements or bug fixes, please feel free to fork the repository and submit a pull request.

## Contact
For any questions or feedback regarding the program, please open an issue in the repository.

## License
This project is open-source and available under [GNU GPLv3](COPYING).
