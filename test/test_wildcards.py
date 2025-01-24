import os
import re

import comfy_tweaker.wildcards.exceptions as exceptions
import pytest
from comfy_tweaker.wildcards import WildcardProcessor


@pytest.fixture
def valid_color_values(wildcard_processor):
    colors = os.path.join(wildcard_processor.directory, "etsy/colors.txt")
    with open(colors, "r") as colors_file:
        valid_values = colors_file.read().splitlines()
    return valid_values


@pytest.fixture
def wildcard_processor(wildcards_directory):
    return WildcardProcessor(wildcards_directory)


@pytest.mark.rng
def test_weighted_wildcards(mocker, wildcard_processor):
    mock_random_choice = mocker.patch("random.choice", return_value="a")
    text = "{a::5|b::4|c}"
    result = wildcard_processor.process(text)
    assert result == "a"
    mock_random_choice.assert_called_with(
        ["a", "a", "a", "a", "a", "b", "b", "b", "b", "c"]
    )


def test_can_refer_to_a_generated_value_by_id(wildcard_processor):
    text = "{testvalue@main} is a {@main}"
    result = wildcard_processor.process(text)
    assert result == "testvalue is a testvalue"


def test_wildcard_ref_names_must_be_unique(wildcard_processor):
    text = "{a@main} {a@main}"
    with pytest.raises(ValueError):
        wildcard_processor.process(text)


def test_wildcard_references(wildcard_processor):
    text = "{a|b|c@a} {d|e|f@b} {{h|i}|g@c} {@a} {@b} {@c}"
    result = wildcard_processor.process(text)
    # match to anything of the for a b c a b c
    assert re.match(r"^[abc] [def] [ghi] [abc] [def] [ghi]$", result)


def test_wildcard_references_with_weights(wildcard_processor):
    text = "{a::5|b::4|c::1@a} {d::2|e::3|f::5@b} {{h::1|i::2}|g::3@c} {@a} {@b} {@c}"
    result = wildcard_processor.process(text)
    # match to anything of the form a b c a b c
    assert re.match(r"^[abc] [def] [ghi] [abc] [def] [ghi]$", result)


def test_wildcard_evaluates_nested_wildcards(wildcard_processor):
    for _ in range(300):
        text = "{a|b|{c|d}}"
        result = wildcard_processor.process(text)
        assert result in ["a", "b", "c", "d"]
    for _ in range(300):
        text = "{a{b|c}}"
        result = wildcard_processor.process(text)
        assert result in ["ab", "ac"]


def test_can_make_wildcard_processor_with_no_directory():
    processor = WildcardProcessor()
    result = processor.process("{a|b|c}")
    assert result in ["a", "b", "c"]


def test_wildcard_processor_throws_value_error_if_no_directory():
    with pytest.raises(ValueError):
        WildcardProcessor().evaluate_file_wildcard("__etsy/colors__")


@pytest.mark.repeat(20)
def test_process(wildcard_processor):
    values = range(1, 6)
    text = f"{{{'|'.join(map(str, values))}}}"
    result = wildcard_processor.process(text)
    assert int(result) in values


def test_process_uses_contents_of_wildcards_folder(
    wildcard_processor, valid_color_values
):
    pattern = "|".join(valid_color_values)
    text = "{__etsy/colors__} {1|2|3}"
    result = wildcard_processor.process(text)
    assert re.match(f"^({pattern}) [123]$", result)


@pytest.mark.repeat(20)
def test_process_works_with_multiple_replacements(wildcard_processor):
    text = "{a|b|c} {1|2|3} {x|y|z}"
    result = wildcard_processor.process(text)
    assert re.match(r"^[abc] [123] [xyz]$", result)


@pytest.mark.repeat(20)
def test_can_evaluate_file_wildcard(wildcard_processor, valid_color_values):
    value = wildcard_processor.evaluate_file_wildcard("__etsy/colors__")
    assert value in valid_color_values


def test_format_error_with_invalid_wildcard_string(wildcard_processor):
    with pytest.raises(exceptions.InvalidWildcardFormat):
        wildcard_processor.evaluate_file_wildcard("invalid format")


def test_raises_error_if_file_not_found(wildcard_processor):
    with pytest.raises(exceptions.WildcardNotFound):
        wildcard_processor.evaluate_file_wildcard("__etsy/does_not_exist__")


def test_raises_error_if_wildcard_file_empty(wildcard_processor):
    with pytest.raises(exceptions.EmptyWildcardFile):
        wildcard_processor.evaluate_file_wildcard("__empty__")
