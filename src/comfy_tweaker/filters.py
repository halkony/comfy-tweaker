import glob
import hashlib
import itertools
import os
import random
import re
import json

from PIL import Image

from comfy_tweaker.utils import filter_collection
from comfy_tweaker.utils import match as match_
from comfy_tweaker.utils import regex_match as regex_match_
from comfy_tweaker.wildcards import WildcardProcessor
from comfy_tweaker import Tweaks

from comfy_tweaker.plugins import PluginType

@Tweaks.register(plugin_type=PluginType.FILTERS)
def match(text, pattern):
    """
    Filters a list to all the elements containing the pattern as a substring.

    Args:
        text (list): The list of strings to filter.
        pattern (str): The substring pattern to match.

    Returns:
        list: A list of elements containing the pattern.
    """
    return match_(text, pattern)

@Tweaks.register()
def from_file(file_path):
    """
    Returns the text contents of a file.

    Example:
    ```yaml
    tweaks:
    - selector:
        id: "12"
      changes:
        text: {{ from_file("/path/to/file.txt") }}
    ```

    If the text file contains newlines, the following is preferred for easier yaml parsing. The bar yaml syntax is useful for text files that may contain colons as they otherwise generate a parsing error.

    ```yaml
    tweaks:
    - selector:
        name: "Positive Prompt"
      changes:
        value: |
        {{ from_file_in_folder("/path/to/folder") | replace('\\n', ' ') }}
    ```

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The contents of the file.
    """
    with open(file_path) as file:
        return file.read()

@Tweaks.register(plugin_type=PluginType.FILTERS)
def regex_match(text, pattern):
    """
    Filters a list to all the elements matching the regex pattern.

    Example:
    ```yaml
    tweaks:
    - selector:
        id: "12"
      changes:
        lora_name: {{ random_choice(in_models_folder("lora") | regex_match(".*?cartoon.*?")) }}
    ```
    Args:
        text (list): The list of strings to filter.
        pattern (str): The regex pattern to match.

    Returns:
        list: A list of elements matching the regex pattern.
    """
    return regex_match_(text, pattern)

@Tweaks.register()
def in_folder_absolute(folder, file_glob="*.safetensors"):
    """
    Returns a list of files in a folder that match the glob pattern. Recurses through subdirectories. Same as `in_folder`, but returns the full paths.

    Args:
        folder (str): The folder to search in.
        file_glob (str, optional): The glob pattern to match. Defaults to "*.safetensors".

    Returns:
        list: A list of files with their full paths.
    """
    return [
        file
        for file in glob.glob(os.path.join(folder, "**", file_glob), recursive=True)
    ]

@Tweaks.register()
def from_folder_absolute(
    folder, file_glob="*.safetensors", match=None, regex_match=None, cycle=False
):
    """
    Returns a random choice from a folder that matches the glob pattern. Same as `from_folder` but returns the absolute path to the file.

    Args:
        folder (str): The folder to search in.
        file_glob (str, optional): The glob pattern to match. Defaults to "*.safetensors".
        match (str, optional): The substring pattern to match. Defaults to None.
        regex_match (str, optional): The regex pattern to match. Defaults to None.
        cycle (bool, optional): Cycle through the files in the folder instead of making a random selection. Defaults to False.

    Returns:
        str: The absolute path to the randomly chosen file.
    """
    return _fetch_cycleable_file(
        in_folder_absolute, folder, file_glob, match, regex_match, cycle
    )

@Tweaks.register()
def from_file_in_folder(
    folder, file_glob="*.txt", match=None, regex_match=None, cycle=False
):
    """
    Returns the contents of a random file in the specified folder, matching the glob pattern.

    ```yaml
    tweaks:
    - selector:
        name: "Positive Prompt"
      changes:
        text: {{ from_file_in_folder("/path/to/folder", cycle=True) }}
    ```
    Args:
        folder (str): The folder to search in.
        file_glob (str, optional): The glob pattern to match. Defaults to "*.txt".
        match (str, optional): The substring pattern to match. Defaults to None.
        regex_match (str, optional): The regex pattern to match. Defaults to None.
        cycle (bool, optional): Cycle through the files in the folder instead of making a random selection. Defaults to False.

    Returns:
        str: The contents of the randomly chosen file.
    """
    path = from_folder_absolute(folder, file_glob, match, regex_match, cycle)
    return from_file(path)

@Tweaks.register()
def in_models_folder(folder, file_glob="*.safetensors"):
    """
    Returns a list of files that are in the specified folder of the models directory. Returns only the base name of the file.

    Args:
        folder (str): The folder to search in.
        file_glob (str, optional): The glob pattern to match. Defaults to "*.safetensors".

    Raises:
        ValueError: If the MODELS_FOLDER environment variable is not set.

    Returns:
        list: A list of files with their base names.
    """
    models_folder = os.getenv("MODELS_FOLDER")
    if not models_folder:
        raise ValueError("MODELS_FOLDER environment variable is not set")
    folder = os.path.join(models_folder, folder)
    return in_folder(folder, file_glob)


def get_cycled_item(key, items):
    if not hasattr(get_cycled_item, "_cycle_iter"):
        get_cycled_item._cycle_iter = {}
    if key not in get_cycled_item._cycle_iter:
        get_cycled_item._cycle_iter[key] = itertools.cycle(items)
    return next(get_cycled_item._cycle_iter[key])


def _fetch_cycleable_file(
    fetching_function, folder, file_glob, match, regex_match, cycle
):
    files = filter_collection(fetching_function(folder, file_glob), match, regex_match)
    if cycle:
        key = (folder, file_glob, match, regex_match)
        return get_cycled_item(key, files)
    else:
        return random.choice(files)

@Tweaks.register()
def from_models_folder(
    folder, file_glob="*.safetensors", match=None, regex_match=None, cycle=False
):
    """
    Returns a random choice from the specified folder in the ComfyUI models folder. Only returns the base name.

    Example:
    ```yaml
    tweaks:
    - selector:
        name: "Lora Loader 1"
      changes:
        lora_name: {{ from_models_folder("lora") }}
    ```
    Args:
        folder (str): The folder to search in.
        file_glob (str, optional): The glob pattern to match. Defaults to "*.safetensors".
        match (str, optional): The substring pattern to match. Defaults to None.
        regex_match (str, optional): The regex pattern to match. Defaults to None.
        cycle (bool, optional): Cycle through the files in the folder instead of making a random selection. Defaults to False.

    Returns:
        str: The base name of the randomly chosen file.
    """
    return _fetch_cycleable_file(
        in_models_folder, folder, file_glob, match, regex_match, cycle
    )

@Tweaks.register()
def in_folder(folder, file_glob="*.safetensors"):
    """
    Returns a list of files in a folder that match the glob pattern, including subdirectories. The results are the paths relative to the folder.

    Args:
        folder (str): The folder to search in.
        file_glob (str, optional): The glob pattern to match. Defaults to "*.safetensors".

    Returns:
        list: A list of files with their base names.
    """
    return [
        os.path.relpath(file, folder)
        for file in glob.glob(os.path.join(folder, "**", file_glob), recursive=True)
    ]

@Tweaks.register(plugin_type=PluginType.FILTERS)
def as_image(absolute_file_path):
    """
    Moves an image into the comfyui input folder and returns its final name. This is useful for providing image inputs like depth maps and canny outlines. In the input folder, the image will have its original filename appended with an MD5 hash so it is easily referenced.

    Example:
    ```yaml
    tweaks:
    - selector:
        id: "12"
        changes:
        image: {{ from_folder_absolute("/path/to/images", "*.png") | as_image }}
    ```

    Args:
        absolute_file_path (str): The absolute file path to an image (e.g. *.png, *.webp).

    Raises:
        ValueError: If the COMFYUI_INPUT_FOLDER environment variable is not set.

    Returns:
        str: The name of the image in the top level of the comfyui inputs directory.
    """
    comfyui_input_folder = os.getenv("COMFYUI_INPUT_FOLDER")
    if not comfyui_input_folder:
        raise ValueError("COMFYUI_INPUT_FOLDER environment variable is not set")

    image_folder = os.path.join(comfyui_input_folder)
    os.makedirs(image_folder, exist_ok=True)
    image = Image.open(absolute_file_path)
    image_bytes = image.tobytes()
    image_hash = hashlib.md5(image_bytes).hexdigest()
    image_name = f"{os.path.basename(absolute_file_path)}-{image_hash}.png"
    final_output_path = os.path.join(image_folder, image_name)
    if not os.path.exists(final_output_path):
        image.save(final_output_path)
    return os.path.relpath(final_output_path, comfyui_input_folder)

@Tweaks.register()
def random_int(min_value, max_value):
    """
    Returns a random integer from min_value to max_value, inclusive.

    Args:
        min_value (int): The minimum value.
        max_value (int): The maximum value.

    Returns:
        int: A random integer between min_value and max_value.

    """
    return random.randint(min_value, max_value)


def from_folder(
    folder, file_glob="*.safetensors", match=None, regex_match=None, cycle=False
):
    """
    Returns a random choice from a folder that matches the glob pattern. Returns only the basename of the file.

    Args:
        folder (str): The folder to search in.
        file_glob (str, optional): The glob pattern to match. Defaults to "*.safetensors".
        match (str, optional): The substring pattern to match. Defaults to None.
        regex_match (str, optional): The regex pattern to match. Defaults to None.
        cycle (bool, optional): Cycle through the files in the folder instead of making a random selection. Defaults to False.

    Returns:
        str: The base name of the randomly chosen file.
    """
    return _fetch_cycleable_file(
        in_folder, folder, file_glob, match, regex_match, cycle
    )

@Tweaks.register(plugin_type=PluginType.FILTERS)
def wildcards(text):
    """
    Replaces stable diffusion style wildcards within a piece of text. The directory for file wildcards is in the environment variable `WILDCARDS_DIRECTORY`, which you can set under `Edit>Preferences` in the UI.

    Example:
    ```yaml
    tweaks:
    - selector:
        id: "12"
      changes:
        text: {{ "a {dog|cat} wearing a hat" | wildcards }}
    ```

    Args:
        text (str): The text containing wildcards.

    Returns:
        str: The text with wildcards replaced.
    """
    processor = WildcardProcessor(directory=os.getenv("WILDCARDS_DIRECTORY"))
    return processor.process(text)

@Tweaks.register()
def random_seed():
    """
    Returns a random seed, which is an integer between 0 and 1125899906842624 inclusive.

    Returns:
        int: A random seed.
    """
    return random.randint(0, 1125899906842624)

@Tweaks.register()
def random_float(min_value, max_value):
    """
    Returns a random float from min_value to max_value, inclusive.

    Args:
        min_value (float): The minimum value.
        max_value (float): The maximum value.

    Returns:
        float: A random float between min_value and max_value.
    """
    return random.uniform(min_value, max_value)

@Tweaks.register()
def random_choice(choices):
    """
    Returns a random choice from the list of choices.

    Args:
        choices (list): The list of choices.

    Returns:
        Any: A randomly chosen element from the list.
    """
    return random.choice(choices)

@Tweaks.register(plugin_type=PluginType.FILTERS)
def as_json_property(file_path, *keys):
    """Grabs a JSON property from the given absolute file path. Pass in as many strings as you need accessors."""
    with open(file_path) as file:
        data = json.load(file)
        for key in keys:
            data = data[key]
        return data