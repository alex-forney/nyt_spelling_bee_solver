"""
NYT Spelling Bee Solver

This program is designed to solve the New York Times Spelling Bee game, a word puzzle
that challenges players to create as many words as possible from a set of seven letters,
with one letter designated as the "center" letter. The program prompts the user to input
the center letter and the outer letters, validates the inputs, and then searches a
pre-defined word list to find all valid words that can be formed using these letters.
It also identifies "pangrams," which are words that use all seven letters.

Usage:
    Run the program and follow the prompts to input the center and outer letters.
    Alternatively, use command-line arguments to specify the center and outer letters.

Command-line Arguments:
    -c, --center: Specify the center letter
    -l, --letters: Specify the outer letters

Input:
    - Center Letter: A single alphabetical character.
    - Outer Letters: Up to six distinct alphabetical characters.

Output:
    - A list of valid words sorted in alphabetical order.
    - The number of pangrams found.
"""

import string
import sys
from argparse import Action, ArgumentParser, ArgumentTypeError, Namespace

from InquirerPy.resolver import prompt
from num2words import num2words

# Constants
ALPHABET = set(string.ascii_lowercase)
FILE_PATH = "nyt.txt"


def validate_char(char: str) -> bool:
    """Validate that the input is a single alphabetical character.

    Args:
        char (str): The input character to validate.

    Returns:
        bool: True if the input is a valid character, False otherwise.
    """
    return char.isalpha() and len(char) == 1


def check_duplicate(char: str, letters: list[str]) -> bool:
    """Check if a character is a valid non-duplicate letter.

    Args:
        char (str): The character to check.
        letters (list[str]): The list of letters to check against.

    Returns:
        bool: True if the character is valid and not a duplicate, False otherwise.
    """
    return validate_char(char) and char not in letters


def get_center(letters: list[str] | None) -> str:
    """Get the center letter from the user.

    Args:
        letters (list[str] | None): The list of outer letters. Defaults to None.

    Returns:
        str: The center letter input by the user.
    """
    validate = (
        validate_char
        if letters is None
        else lambda result: check_duplicate(result, letters)
    )
    invalid_message = (
        "Input must be a single letter"
        if letters is None
        else "Input must be a single letter and cannot be in outer letters"
    )
    center_prompt_settings = [
        {
            "name": "center",
            "type": "input",
            "message": "Please enter the center letter:",
            "qmark": "",
            "amark": "",
            "validate": validate,
            "invalid_message": invalid_message,
            "transformer": lambda result: result.lower(),
        }
    ]
    center_prompt = prompt(center_prompt_settings, style={"answermark": ""})
    return center_prompt["center"].lower()


def get_letters(center: str, old_letters: list[str]) -> list[str]:
    """Prompt the user to input the outer letters for the game.

    Args:
        center (str): The center letter.
        old_letters (list[str]): The initial list of outer letters.

    Returns:
        list[str]: The final list of outer letters.
    """
    letters = [center] if old_letters is None else [center] + old_letters
    while len(letters) < 7:
        nth = num2words(len(letters), to="ordinal")
        letter_prompt_settings = [
            {
                "name": "letter",
                "type": "input",
                "message": f"Please enter the {nth} outer letter:",
                "qmark": "",
                "amark": "",
                "validate": lambda result: check_duplicate(result, letters),
                "invalid_message": (
                    "Input must be a single letter and cannot be repeated"
                ),
                "transformer": lambda result: result.lower(),
            }
        ]
        letter_prompt = prompt(letter_prompt_settings, style={"answermark": ""})
        letters.append(letter_prompt["letter"].lower())
    return letters


def get_words() -> list[str]:
    """Retrieve the list of words from the NYT word file.

    Returns:
        list[str]: The list of words.
    """
    try:
        with open(FILE_PATH, encoding="utf-8") as file:
            return [x.lower() for x in file.read().splitlines()[2:]]
    except FileNotFoundError:
        print(f"Error: File {FILE_PATH} not found.")
        sys.exit(1)


def solver(
    word_list: list[str], acceptable: list[str], center: str
) -> tuple[list[str], int]:
    """Find all valid words and pangrams in the word list.

    Args:
        word_list (list[str]): The list of words to check.
        acceptable (list[str]): The list of acceptable letters.
        center (str): The center letter.

    Returns:
        tuple[list[str], int]: A tuple containing the list of valid words and the number
            of pangrams found.
    """
    words = set()
    num_pan = 0
    unacceptable = ALPHABET - set(acceptable)
    for word in word_list:
        if center in word and not any(el in unacceptable for el in word):
            if all(el in word for el in acceptable):
                words.add(word.upper())
                num_pan += 1
            else:
                words.add(word)
    return sorted(words, key=str.casefold), num_pan


def print_results(words: list[str], num_pan: int) -> None:
    """Print the results of the word search.

    Args:
        words (list[str]): The list of words found in the word search.
        num_pan (int): The number of pangrams found in the word search.

    Returns:
        None
    """
    num_words = len(words)
    if num_words == 0:
        print("No words were found.")
    else:
        pan_str = (
            f", including {num_pan} pangram{'s' if num_pan != 1 else ''},"
            if num_pan > 0
            else ""
        )
        verb = "were" if num_words != 1 else "was"
        ess = "s" if num_words != 1 else ""
        print(f"{num_words} word{ess}{pan_str} {verb} found:")
        for word in words:
            print(f"\t{word}")


def check_letter(value: str) -> str:
    """Validate a letter argument for the argparse module.

    Args:
        value (str): The argument value to validate.

    Returns:
        str: The validated argument value.
    """
    if not validate_char(value):
        raise ArgumentTypeError("input must only contain single letters")
    return value.lower()


def validate_contain(center: str, letters: list[str]) -> None:
    """Validate that the center letter is not in the outer letters.

    Args:
        center (str): The center letter.
        letters (list[str]): The list of outer letters.

    Returns:
        None
    """
    if center and letters:
        if center in letters:
            print("Error: Center letter cannot be contained in outer letters.")
            sys.exit(1)


class ValidatedLetters(Action):
    """An argparse action to validate a list of outer letters."""

    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        values: str | None,
        option_string: str | None = None,
    ) -> None:
        """Validate and store the outer letters.

        Args:
            parser (ArgumentParser): The argparse parser.
            namespace (Namespace): The argparse namespace.
            values (str | None): The outer letters to validate.
            option_string (str | None): The option string used in the command line.

        Returns:
            None
        """
        input_len = 0
        input_set_len = 0
        if values:
            input_len = len(values)
            input_set_len = len(set(values))
        if not 1 <= input_len <= 6:
            opt = "/".join(self.option_strings)
            print(
                f"Error: argument {opt}: Outer letters can have between one and six"
                " entries."
            )
            sys.exit(1)
        if input_set_len != input_len:
            opt = "/".join(self.option_strings)
            print(f"Error: argument {opt}: Outer letters cannot contain duplicates")
            sys.exit(1)
        setattr(namespace, self.dest, values)


def get_args() -> tuple[str, list[str]]:
    """Parse and validate the command line arguments.

    Returns:
        tuple[str, list[str]]: A tuple containing the center letter and the list of
            outer letters.
    """
    description = "Command-line tool for playing the New York Times Spelling Bee"
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "-c",
        "--center",
        type=check_letter,
        default=None,
        action="store",
        help="center letter",
    )
    parser.add_argument(
        "-l",
        "--letters",
        type=check_letter,
        default=None,
        nargs="+",
        action=ValidatedLetters,
        help="outer letters",
    )
    args = parser.parse_args()
    center = args.center
    letters = args.letters
    validate_contain(center, letters)
    return center, letters


def main() -> None:
    """The main function to run the Spelling Bee solver.

    Returns:
        None
    """
    center, letters = get_args()
    if not center:
        center = get_center(letters)
    acceptable = get_letters(center, letters)
    word_list = get_words()
    words, num_pan = solver(word_list, acceptable, center)
    print_results(words, num_pan)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("Operation canceled by user.")
        sys.exit(1)
