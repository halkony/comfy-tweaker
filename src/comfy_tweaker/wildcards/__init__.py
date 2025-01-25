import os
import random

import attrs
import regex as re

from .exceptions import (EmptyWildcardFile, InvalidWildcardFormat,
                         WildcardNotFound)


@attrs.define()
class WildcardProcessor:
    """
    A class to handle wildcard replacements in text.

    Attributes:
        directory (str): The directory where wildcard files are stored.
    """

    directory: str = attrs.field(default=None)
    seed: int = attrs.field(default=None)

    def __attrs_post_init__(self):
        if self.seed:
            random.seed(self.seed)

    def process(self, text):
        """
        Replaces wildcards in the given text with random choices or evaluated wildcards.
        This method processes the input text to replace wildcards of the form `{a|b|c}`
        with a random choice from the given options, and wildcards of the form `__etsy/colors__`
        with the result of evaluating the wildcard file.
        Args:
            text (str): The input text containing wildcards to be replaced.
        Returns:
            str: The text with wildcards replaced by their respective values.
        """

        # Pattern to match {a|b|c} or {a::5, b::3, c::2}
        pattern = re.compile(r"\{(?!@)((?:[^{}]*|(?R))*)\}")
        ref_pattern = re.compile(r"\{@(.*?)\}")
        # Pattern to match __etsy/colors__
        file_wildcard_pattern = re.compile(r"__(\w+[\/\w+]*)__")
        context = {}

        def replace(match):
            def replace_file_wildcard(match):
                file_wildcard = f"__{match.group(1)}__"
                return self.evaluate_file_wildcard(file_wildcard)

            content = match.group(1).split("@")
            options = re.split(r"\|(?![^{]*\})", content[0])
            for index, option in enumerate(options):
                new_pattern = re.compile(r"(.*?)\{(?!@)((?:[^{}]*|(?R))*)\}(.*?)")
                if pattern.search(option):
                    substitution = replace(pattern.search(option))
                    options[index] = new_pattern.sub(rf"\1{substitution}\3", option)
            weighted_options = []
            for option in options:
                if "::" in option:
                    value, weight = option.split("::")
                    weighted_options.extend([value.strip()] * int(weight.strip()))
                else:
                    weighted_options.append(option.strip())
            result = random.choice(weighted_options)
            result = file_wildcard_pattern.sub(replace_file_wildcard, result)
            if len(content) > 1:
                if content[1] in context:
                    raise ValueError(f"Duplicate ref key found: {content[1]}")
                context[content[1]] = result
            return result

        # Replace nested {} expressions first
        while pattern.search(text):
            text = pattern.sub(replace, text)

        # Replace {@ref} syntax in place
        while ref_pattern.search(text):
            text = ref_pattern.sub(lambda match: context[match.group(1)], text)
        return text

    def evaluate_file_wildcard(self, file_wildcard):
        """
        Args:
            file_wildcard (str): The wildcard string to evaluate. It should be in the format
                                 `__path/to/file__`.

        Returns:
            str: A randomly selected line from the file specified by the wildcard.

        Raises:
            InvalidWildcardFormat: If the wildcard does not start and end with double underscores.
            WildcardNotFound: If the file specified by the wildcard does not exist.
            EmptyWildcardFile: If the file specified by the wildcard is empty.
        """
        # Extract the path from the wildcard
        if not self.directory:
            raise ValueError("Wildcard directory not set")
        if not file_wildcard.startswith("__") or not file_wildcard.endswith("__"):
            raise InvalidWildcardFormat("Invalid wildcard format")

        path = file_wildcard.strip("__").replace("/", os.sep) + ".txt"
        file_path = os.path.join(self.directory, path)

        if not os.path.exists(file_path):
            raise WildcardNotFound(f"Wildcard file not found: {file_path}")

        with open(file_path, "r") as file:
            lines = file.read().splitlines()

        if not lines:
            raise EmptyWildcardFile(f"No lines found in file: {file_path}")

        return random.choice(lines)
