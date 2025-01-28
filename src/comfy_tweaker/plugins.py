from dataclasses import dataclass, field
from enum import Enum
import importlib.util
import sys

def import_plugin(module_name, plugin_path):
    spec = importlib.util.spec_from_file_location(module_name, plugin_path)
    plugin = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = plugin
    spec.loader.exec_module(plugin)
    return plugin


class PluginType(Enum):
    GLOBALS = "globals"
    FILTERS = "filters"


@dataclass
class Plugin:
    name: str
    func: callable
    plugin_type: PluginType = field(default=PluginType.GLOBALS.value)
