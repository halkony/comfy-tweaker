import asyncio
import os

import pytest

import comfy_tweaker as tweaker
from comfy_tweaker import Tweak, Tweaks, Workflow
from comfy_tweaker.exceptions import (IncompleteImageWorkflowError,
                                      InvalidSelectorError)


@pytest.fixture
def workflow(tweaks_directory):
    return Workflow.from_image(tweaks_directory / "valid_workflow_image.png")


@pytest.fixture
def tweaks(tweaks_directory):
    return Tweaks.from_file(tweaks_directory / "tweaks_file.yaml")


def test_tweak_must_have_valid_selector():
    with pytest.raises(InvalidSelectorError):
        tweak = tweaker.Tweak(
            {"nonsense": "nonsense"}, {"lora_name": "test.safetensors"}
        )


def test_tweak_cant_have_multiple_selectors():
    with pytest.raises(InvalidSelectorError):
        tweak = tweaker.Tweak(
            {"id": "346", "name": "test"}, {"lora_name": "test.safetensors"}
        )


def test_can_define_tweak():
    """Tweaks are single changes applied to a node"""
    tweak = tweaker.Tweak({"id": "346"}, {"lora_name": "test.safetensors"})
    assert tweak is not None


def test_tweak_is_immutable():
    tweak = tweaker.Tweak({"id": "346"}, {"lora_name": "test.safetensors"})
    with pytest.raises(AttributeError):
        tweak.selector = {"name": "test"}


def test_can_create_tweaks():
    """Tweaks are collections of tweaks that can be applied to a workflow"""
    tweaks = tweaker.Tweaks()
    assert tweaks is not None


def test_can_validate_tweaks(workflow, tweaks):
    workflow.validate(tweaks)


def test_workflow_from_image_raises_error_with_invalid_image(tweaks_directory):
    with pytest.raises(IncompleteImageWorkflowError):
        workflow = tweaker.Workflow.from_image(
            tweaks_directory / "invalid_workflow_image.png"
        )


def test_can_get_tweaks_from_file(snapshot, tweaks_directory):
    tweaks_file_path = tweaks_directory / "tweaks_file.yaml"

    tweaks = tweaker.Tweaks.from_file(tweaks_file_path)
    assert tweaks is not None
    assert tweaks.tweaks == snapshot


def test_can_create_workflow_from_image(tweaks_directory, snapshot):
    workflow = tweaker.Workflow.from_image(tweaks_directory / "valid_workflow_image.png")
    assert workflow == snapshot


def test_creating_workflow_with_invalid_image_raises_error(tweaks_directory):
    with pytest.raises(IncompleteImageWorkflowError):
        workflow = tweaker.Workflow.from_image(
            tweaks_directory / "invalid_workflow_image.png"
        )

def test_can_save_workflow_to_files(tweaks_directory, snapshot):
    workflow = tweaker.Workflow.from_image(tweaks_directory / "valid_workflow_image.png")
    new_gui_workflow_path = tweaks_directory / "new_example_workflow.json"
    new_api_workflow_path = tweaks_directory / "new_API_example_workflow.json"

    workflow.save(new_gui_workflow_path, new_api_workflow_path)
    assert new_gui_workflow_path.exists()
    assert new_api_workflow_path.exists()


def test_can_save_tweaks_to_yaml_file(snapshot, tmpdir):
    tweaks_file_path = tmpdir / "tweaks_file.yaml"
    tweaks = Tweaks()
    tweaks = tweaks.add(tweaker.Tweak({"id": "346"}, {"lora_name": "test.safetensors"}))

    tweaks.save(tweaks_file_path)
    tweaks = Tweaks.from_file(tweaks_file_path)
    assert tweaks == snapshot


def test_models_can_take_match_arg(models_directory):
    os.environ["MODELS_FOLDER"] = str(models_directory)
    for _ in range(200):
        tweaks_yaml = """
        tweaks:
            - selector:
                id: 346
              changes:
                lora_name: {{ from_models_folder("lora", match="1") }}
        """
        tweaks = tweaker.Tweaks.from_yaml(tweaks_yaml)
        assert tweaks.tweaks[0].changes["lora_name"] == "test1.safetensors"


def test_models_can_take_regex_match_arg(models_directory):
    os.environ["MODELS_FOLDER"] = str(models_directory)
    for _ in range(200):
        tweaks_yaml = """
        tweaks:
            - selector:
                id: 346
              changes:
                lora_name: {{ from_models_folder("lora", regex_match=".*?1\.safetensors") }}
        """
        tweaks = tweaker.Tweaks.from_yaml(tweaks_yaml)
        assert tweaks.tweaks[0].changes["lora_name"] == "test1.safetensors"


def test_can_get_random_choice(mocker):
    tweaks_yaml = """
    tweaks:
        - selector:
            id: 346
          changes:
            lora_name: {{ random_choice(["test.safetensors", "test.safetensors2"]) }}
    """
    expected_value = "expected_value.safetensors"
    mocked_random_choice = mocker.patch("random.choice", return_value=expected_value)

    tweaks = tweaker.Tweaks.from_yaml(tweaks_yaml)
    mocked_random_choice.assert_called_with(["test.safetensors", "test.safetensors2"])
    assert tweaks.tweaks[0].changes["lora_name"] == expected_value


def test_can_evaluate_rng_tweak_tags(tweaks_directory, mocker):
    yaml_string = """
    tweaks:
        - selector:
            id: 346
          changes:
            strength: {{ random_float(0.0, 1.0) }}
    """
    mocked_random = mocker.patch("random.uniform", return_value=0.5)
    tweaks = tweaker.Tweaks.from_yaml(yaml_string)

    assert tweaks.tweaks[0].changes["strength"] == 0.5
    mocked_random.assert_called_with(0.0, 1.0)


def test_can_apply_tweaks_to_workflow(tweaks_directory, snapshot):
    workflow_image_path = tweaks_directory / "valid_workflow_image.png"
    tweaks_file_path = tweaks_directory / "tweaks_file.yaml"

    tweaks = tweaker.Tweaks.from_file(tweaks_file_path)
    workflow = tweaker.Workflow.from_image(workflow_image_path)

    result = workflow.apply_tweaks(tweaks)
    assert result == snapshot


def test_can_use_wildcards_in_tweaks_file(mocker):
    tweaks_data = """
    tweaks:
        - selector:
            id: 346
          changes:
            value: {{  "__animals__" | wildcards }}
    """

    expected_result = "This is expected."
    mocker.patch(
        "comfy_tweaker.wildcards.WildcardProcessor.process", return_value=expected_result
    )

    tweaks = tweaker.Tweaks.from_yaml(tweaks_data)
    assert tweaks.tweaks[0].changes == {"value": expected_result}


def test_tweaks_file_wildcards_can_use_file_wildcards(mocker, wildcards_directory):
    tweaks_data = """
    tweaks:
        - selector:
            id: 346
          changes:
            value: {{ "{__animals__}" | wildcards }}
    """
    os.environ["WILDCARDS_DIRECTORY"] = str(wildcards_directory)

    tweaks = tweaker.Tweaks.from_yaml(tweaks_data)
    assert tweaks.tweaks[0].changes["value"] in ["cow", "dog", "cat", "moose"]


def test_tweaks_file_can_product_random_int(mocker):
    mocked_randint = mocker.patch("random.randint", return_value=50)

    tweaks_data = """
    tweaks:
        - selector:
            id: 346
          changes:
            strength: {{random_int(0, 100)}}
    """
    tweaks = tweaker.Tweaks.from_yaml(tweaks_data)
    mocked_randint.assert_called_with(0, 100)
    assert tweaks.tweaks[0].changes == {"strength": 50}


def test_can_get_models_from_folder(mocker, models_directory):
    os.environ["MODELS_FOLDER"] = str(models_directory)

    tweaks_yaml = """
    tweaks:
        - selector:
            id: 346
          changes:
            lora_name: {{ from_models_folder("lora") }}
    """
    tweaks = tweaker.Tweaks.from_yaml(tweaks_yaml)
    assert tweaks.tweaks[0].changes["lora_name"] in [
        "test1.safetensors",
        "test2.safetensors",
    ]


def test_can_match_to_lora_names(models_directory):
    os.environ["MODELS_FOLDER"] = str(models_directory)

    # this isnt how you would use it practically, but returning the list directly keeps rng out of our test
    tweaks_yaml = """
    tweaks:
        - selector:
            id: 346
          changes:
            lora_name: {{ from_models_folder("lora", match="1") }}
    """
    tweaks = tweaker.Tweaks.from_yaml(tweaks_yaml)
    assert tweaks.tweaks[0].changes["lora_name"] == "test1.safetensors"


def test_tweaks_id_selector_works_with_ints_and_string():
    tweaks_yaml = """
    tweaks:
        - selector:
            id: 346
          changes:
            strength: 50
        - selector:
            id: "348"
          changes:
            strength: 50
    """
    tweaks = tweaker.Tweaks.from_yaml(tweaks_yaml)
    assert tweaks.tweaks[0].selector["id"] == "346"
    assert tweaks.tweaks[1].selector["id"] == "348"


def test_can_reusue_random_values_with_jinja():
    tweaks_yaml = """
    {% set random_value = random_int(0, 100) %}
    tweaks:
        - selector:
            id: 346
          changes:
            strength: {{ random_value }}
        - selector:
            id: 348
          changes:
            strength: {{ random_value }}
    """
    tweaks = tweaker.Tweaks.from_yaml(tweaks_yaml)
    assert tweaks.tweaks[0].changes["strength"] == tweaks.tweaks[1].changes["strength"]


def test_tweaks_file_can_cycle_through_files_in_folder(tmpdir):
    tweaks_yaml = f"""
    tweaks:
        - selector:
            id: 346
          changes:
            lora_name: {{{{ from_file_in_folder("{str(tmpdir).replace(os.sep, "/")}", cycle=True) }}}}
    """
    file1 = tmpdir / "file1.txt"
    file2 = tmpdir / "file2.txt"

    file1.write_text("file1", encoding="utf-8")
    file2.write_text("file2", encoding="utf-8")

    tweaks = tweaker.Tweaks.from_yaml(tweaks_yaml)
    assert tweaks.tweaks[0].changes["lora_name"] == "file1"
    for i in range(200):
        tweaks = tweaks.regenerate()
        if i % 2 == 0:
            expected_value = "file2"
        else:
            expected_value = "file1"
        assert tweaks.tweaks[0].changes["lora_name"] == expected_value


def test_tweaks_file_supports_folder_cycle(models_directory):
    os.environ["MODELS_FOLDER"] = str(models_directory)

    tweaks_yaml = """
    tweaks:
        - selector:
            id: 346
          changes:
            lora_name: {{ from_models_folder("lora", cycle=True) }}
    """

    tweaks = tweaker.Tweaks.from_yaml(tweaks_yaml)
    assert tweaks.tweaks[0].changes["lora_name"] == "test1.safetensors"
    for i in range(200):
        tweaks = tweaks.regenerate()
        if i % 2 == 0:
            expected_value = "test2.safetensors"
        else:
            expected_value = "test1.safetensors"
        assert tweaks.tweaks[0].changes["lora_name"] == expected_value


def test_empty_tweaks_wont_change_workflow(workflow):
    tweaks = Tweaks()
    result = workflow.apply_tweaks(tweaks)
    assert result == workflow


def test_can_regex_match_to_lora_names(models_directory):
    os.environ["MODELS_FOLDER"] = str(models_directory)

    # this isnt how you would use it practically, but returning the list directly keeps rng out of our test
    tweaks_yaml = """
    tweaks:
        - selector:
            id: 346
          changes:
            lora_name: {{ in_models_folder("lora") | regex_match(".*?2.*?") }}
        - selector:
            id: 348
          changes:
            lora_name: {{ in_models_folder("lora") }}
    """
    tweaks = tweaker.Tweaks.from_yaml(tweaks_yaml)
    assert tweaks.tweaks[0].changes["lora_name"] == ["test2.safetensors"]
    assert tweaks.tweaks[1].changes["lora_name"] == [
        "test1.safetensors",
        "test2.safetensors",
    ]

def test_can_make_xy_matrix_in_jinja():
    tweaks_yaml = """
    {% macro lora1_strength(iteration) %}{{ (iteration // 10) * 0.05 }}{% endmacro %}
    {% macro lora2_strength(iteration) %}{{ (iteration % 10) * 0.05 }}{% endmacro %}
    tweaks:
        - selector:
            name: "Lora Loader 1"
          changes:
            strength: {{ lora1_strength(iteration) }}
        - selector:
            name: "Lora Loader 2"
          changes:
            strength: {{ lora2_strength(iteration) }}
    """

    tweaks = tweaker.Tweaks.from_yaml(tweaks_yaml)
    for i in range(200):
        assert tweaks.tweaks[0].changes["strength"] == (i // 10) * 0.05
        assert tweaks.tweaks[1].changes["strength"] == (i % 10) * 0.05
        tweaks = tweaks.regenerate()

def test_can_generate_tweaks_with_an_iterator():
    tweaks_yaml = """
    tweaks:
        - selector:
            id: 346
          changes:
            lora_strength: {{ iteration }}
    """
    tweaks = tweaker.Tweaks.from_yaml(tweaks_yaml)
    for i in range(200):
        assert tweaks.tweaks[0].changes["lora_strength"] == i
        tweaks = tweaks.regenerate()

@pytest.mark.skip("Mocker not functional")
@pytest.mark.asyncio
async def test_job_queue_start(workflow, tweaks, mocker):
    mocked_comfyui = mocker.patch("comfy_tweaker.comfyui.send_workflow_to_server")
    job = tweaker.Job(workflow, tweaks, amount=2)
    queue = tweaker.JobQueue(queue=[job])
    task = asyncio.create_task(queue.start())

    await task
    assert len(queue.queue) == 0
    assert mocked_comfyui.send_workflow_to_server.call_count == 2


@pytest.mark.skip("Mocker not functional")
@pytest.mark.asyncio
async def test_job_queue_pause(workflow, tweaks, mock_send_workflow_to_server):
    job = tweaker.Job(workflow, tweaks, amount=10)
    queue = tweaker.JobQueue(queue=[job])
    task = asyncio.create_task(queue.start())
    raise AssertionError("Queue not processing jobs")
    attempts = 15
    while mock_send_workflow_to_server.call_count < 5:
        if attempts == 0:
            raise AssertionError("Queue not processing jobs")
        attempts -= 1

    queue.pause()
    await task
    assert len(queue.queue) == 1
    assert mock_send_workflow_to_server.call_count == 5
