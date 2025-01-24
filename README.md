<div align="center">
<p align="center">
  <img src="https://i.imgur.com/Lhy3ldn.png" alt="Comfy Tweaker Logo" width="200" height="200">
</p>
<h1 align="center">Comfy Tweaker</h1>
<div style="display: flex; gap: 5px; justify-content: center;">
<br>

</div>
</div>

[![Docs][docs-shield]][docs-url]
[![Discord][discord-shield]][discord-url]
[![Patreon][patreon-shield]][patreon-url]

[discord-shield]: https://img.shields.io/discord/895430371972358185?style=flat-square&logo=Discord&label=Discord
[discord-url]: https%3A%2F%2Fdiscord.gg%2F9QeqHvAd8r
[patreon-shield]: https://img.shields.io/badge/Patreon-orange?style=flat-square&logo=patreon&logoSize=auto
[patreon-url]:https%3A%2Fpatreon.com%2Fcomfytweaker
[docs-shield]: https://img.shields.io/badge/Docs-blue?style=flat-square&logo=gitbook&logoSize=auto
[docs-url]: https://google.com


Comfy Tweaker is a ComfyUI companion app for generating massive amounts of images with precise, user-defined tweaks.

It is ideal for:

- Running long queues of ComfyUI jobs
- Generating many variations of one workflow
- Large scale experiments of value tweaking, like optimizing LorA weights

## Features
 - Easy to use workflow management interface
 - Stop, re-order, and resume jobs during ComfyUI generation
    - Each workflow is queued only when the last one completes
    - Stop and restart the queue whenever you feel like
        - Great for performing quick experiments while also running longer jobs
    - Run thousands of workflows with ease
 - Declarative yaml syntax for creating precise variations of your workflows
    - Supports the standard `{a|b}` wildcard syntax
        - Includes backrefs and customizable weights for precise control
    - Randomly generated values are baked into the image workflow
        - No more messing with random number nodes and text outputs
    - Load a random image or file from a folder
    - Filter random selections by name or with regex patterns


## Installation
Download the latest .exe under [releases.](https://github.com/halkony/comfy-tweaker/releases)

Check out the quickstart guide in the docs to get started.

## Troubleshooting
- Windows users should ensure that the paths in their tweaks files use forward slashes.
- This repo has not been tested on Linux yet. If the released .exe doesn't work, try cloning this repo and running
```py
pip install -r ./requirements/base.txt
pip install .
comfy-tweaker
```
