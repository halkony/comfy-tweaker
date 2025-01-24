import json
import os

from appdirs import user_data_dir


def get_settings_file_path():
    config_dir = user_data_dir("ComfyTweaker", "ComfyTweaker", roaming=True)
    os.makedirs(config_dir, exist_ok=True)
    if not os.path.exists(os.path.join(config_dir, "settings.json")):
        with open(os.path.join(config_dir, "settings.json"), "w") as f:
            json.dump({"comfy_ui_server_address": "127.0.0.1:8188"}, f)
    return os.path.join(config_dir, "settings.json")


def save_settings(settings):
    settings_file = get_settings_file_path()
    with open(settings_file, "w") as f:
        json.dump(settings, f)


def load_settings():
    settings_file = get_settings_file_path()
    if os.path.exists(settings_file):
        with open(settings_file, "r") as f:
            return json.load(f)
    return {}
