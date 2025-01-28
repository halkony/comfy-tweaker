# Plugins
Comfy Tweaker can be extended with custom plugins.

## Template Plugins
A template plugin is a .py file similar to the following
```py
# Metadata for the plugin
__plugin_name__ = "My Example Plugin"
__plugin_description__ = "A plugin that says hello when you call it in a tweaks file."

# Import the required decorator from your project
from comfy_tweaker.plugins import tweaks_plugin

# Use the decorator to mark this function as a plugin
@tweaks_plugin
def greet(name: str) -> str:
    """Greets the user by name."""
    return f"Hello, {name}!"
```

This plugin can be used in the tweaks file like any other function.

```yaml
tweaks:
    - selector:
        id: "12"
      changes:
        value: {{ "Ted" | greet }}
```

To install a plugin, place the .py file in `%appdata%/ComfyTweaker/ComfyTweaker/plugins`. Restart Comfy Tweaker and it will now recognize the plugin.