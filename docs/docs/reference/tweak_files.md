# Tweak Files

Tweak files define the changes made to a workflow before it runs. They are stored in a yaml format.

The following tweaks would change the "description" and "strength" values the node with ID 12 and the "text" value of the node named "Positive Prompt". These changes are applied directly before the workflow runs.
```yaml
tweaks:
    - selector:
        id: "12"
      changes:
        description: "This is the new value"
        strength: 2
    - selector:
        name: "Positive Prompt"
      changes:
        text: "A giraffe wearing a hat"
```

Each tweak is defined under `tweaks`. Each item in tweak should have a `selector` and `changes`.

A selector expects the `id` of the node or the `name` of the node, but not both. As of right now, you cannot use a selector that would match to more than one node in a workflow.

Any values under `changes` will be applied to the workflow when it is run with Comfy Tweaker. These changes are preserved when you drag and drop the resulting image into ComfyUI. If you press `Save As...` in the GUI, you can save the workflow JSON directly.

## Filters
::: comfy_tweaker.filters