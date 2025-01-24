Note: This software is considered pre-Alpha. APIs may change in the future.

# Quickstart

Launch the UI by running the latest `comfy-tweaker.exe` from the [releases page.](https://github.com/halkony/comfy-tweaker/releases)

Go to `Edit>Preference` and set the ComfyUI folder to the root of your ComfyUI installation (the folder that contains both "input" and "output").

Open an image in ComfyUI and note the id of the prompt node. Enable "Node ID Badges" in your ComfyUI settings if you haven't.

Drag and drop the image into Comfy Tweaker.

Create a yaml file and use the node id to define changes.

For example, if the node id was 20, the following would change the text value of the node to "an old man sitting on a bench":

```yaml
tweaks:
    - selector:
        id: "20"
      changes:
        text: "An old man sitting on a bench."
```

Drag and drop this yaml file into Comfy Tweaker. Click `Add Job`, then click `Start`. When the job finishes, right click it in the list, then select `Go To Folder` to jump the output folder.

The image should contain an old man sitting on a bench.

You can save the tweaked workflow without generating it by clicking the `Save As...` button.

---

You can also refer to a node by its name.

For example, if your prompt node was named "Positive Prompt", this tweak would have the same effect:

```yaml
tweaks:
    - selector:
        name: "Positive Prompt"
      changes:
        text: "An old man sitting on a bench."
```

Usually the name of the change is the same as its placeholder text. If you don't see the name of the input you're trying to change, right click the node in ComfyUI and hover over "Convert Widget to Input". It should be there.

## Random Values
Tweak files support an extended Jinja syntax for dynamically generated values.

For example, the following tweak randomly sets the strength of "Lora Loader 1" between 0 and 1 every time the workflow runs.
```yaml
tweaks:
    - selector:
        name: "Lora Loader 1"
      changes:
        model_strength: {{ random_float(0, 1) }}
```

You can make a random choice from a list with `random_choice`.
```yaml
tweaks:
    - selector:
        name: "Lora Loader 1"
      changes:
        lora_name: {{ random_choice(["lora1.safetensors", "lora2.safetensors"]) }}
```

## Selecting Random Files

After setting your models folder under `Edit>Preferences`, you can dynamically select files from it. The following tweak will select a random file in the lora models folder.
```yaml
tweaks:
    - selector:
        name: "Lora Loader 1"
     changes:
        lora_name: {{ from_models_folder("lora") }}
```

By default, it only selects ".safetensors" files, but it also supports other file patterns. The following would select a random ".pth" file.
```yaml
tweaks:
    - selector:
        name: "Lora Loader 1"
     changes:
        lora_name: {{ from_models_folder("lora", file_glob="*.pth") }}
```

You can also specify an absolute path with the `from_folder` function.

## Cycling through Files
You can cycle through the files in a folder using the cycle keyword argument. The following example would use the next LorA in the folder every time the workflow runs.
```yaml
tweaks:
    - selector:
        name: "Lora Loader 1"
     changes:
        lora_name: {{ from_models_folder("lora", cycle=True) }}
```

## Reusing Random Values
You can use Jinja variables to reuse any generated values. The following example would use the same weight for boths LorAs.
```yaml
{% set random_value = random_int(0, 100) %}
tweaks:
    - selector:
        name: "Lora Loader 1"
      changes:
        strength: {{ random_value }}
    - selector:
        name: "Lora Loader 2"
      changes:
        strength: {{ random_value }}
```

This is useful for naming outputs while cycling through files. The following example would include the lora name in the workflow output.
```yaml
{% set lora_name = from_models_folder("lora", cycle=True) %}
tweaks:
    - selector:
        name: "Lora Loader 1"
      changes:
        lora_name: {{ lora_name }}
    - selector:
        name: "Save Image"
      changes:
        prefix: "Output_{{ lora_name }}_Image""
```

It's important to set a variable if you want to reuse a cycled value. Calling a cycling function again in the same tweak file will produce the next value, which is not recommended.

## Filtering By Name
To filter a random selection by its contents, use the `match` or `regex_match` keyword argument. The following example would select a random lora with the word "cartoon" in it.

```yaml
tweaks:
    - selector:
        name: "Lora Loader 1"
     changes:
        lora_name: {{ from_models_folder("lora", match="cartoon") }}
```

## Loading Images
After you've set your ComfyUI folder in `Edit>Preferences`, you can load an image using the `as_image` Jinja filter and an absolute path to the image.

For example, this tweak would select a random depth map from a folder.
```yaml
tweaks:
    - selector:
        name: "Depth Map Image"
     changes:
        image: {{ from_folder_absolute("/path/to/depth/images") | as_image }}
```

This copies the image into your inputs folder and returns its filename, which is what ComfyUI expects. Every time it is evaluated, it will copy the image to the inputs folder, so be mindful when working with large images.

## Wildcards
Comfy Tweaker supports standard stable diffusion wildcards. You can set your wildcards directory in `Edit>Preferences`.

The following tweak would either set the prompt to "human" or an entry from the "animals.txt" file in your wildcards directory.
```yaml
tweaks:
    - selector:
        name: "Positive Prompt"
     changes:
        value: {{ "a {human|__animals__} wearing a baseball cap" | wildcards }}
```

### Backrefs
If you want to reuse a wildcard later in the prompt, you can use the `@` backref notation.

For example, any wildcard whose contents end with `@animal` can be referred to with `{@animal}` later in the text. The following would produce a prompt describing two of the same animal.

```yaml
tweaks:
    - selector:
        name: "Positive Prompt"
     changes:
        value: {{ "a {bear|cat|dog@animal} wearing a baseball cap and another {@animal} wearing a cowboy hat" | wildcards }}
```

### Custom Weights
You can specify the weights of each wildcard entry using the `::` syntax.

The weights are normalized and do not need to add up to one. For example, the following tweak would select human 2 times, koala 3 times, and bear 5 times for every 10 generations of the prompt.
```yaml
tweaks:
    - selector:
        name: "Positive Prompt"
     changes:
        value: {{ "a {human::2|koala::3|bear::5} wearing a baseball cap" | wildcards }}
```

The weights only influence the random selection of the wildcard, so a perfect ratio of selection is not guaranteed.