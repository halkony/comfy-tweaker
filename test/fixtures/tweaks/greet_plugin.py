# Metadata for the plugin
__plugin_name__ = "My Example Plugin"
__plugin_description__ = "A plugin that says hello when you call it in a tweaks file."

# Import the required decorator from your project
from comfy_tweaker import Tweaks

# Use the decorator to mark this function as a plugin
@Tweaks.register()
def greet(name: str) -> str:
    """Greets the user by name."""
    return f"Hello, {name}!"