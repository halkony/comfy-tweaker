<p align="center">
  <img src="https://i.imgur.com/Lhy3ldn.png" alt="Comfy Tweaker Logo" width="200" height="200">
</p>
<h1 align="center">Comfy Tweaker</h1>
<div style="display: flex; gap: 5px; justify-content: center;">
<a align="center" href="https://www.patreon.com/bePatron?u=70591568" style="
    display: inline-block;
    padding: 5px 10px;
    font-size: 12px;
    color: white;
    background-color:rgb(35, 18, 165);
    border-radius: 5px;
    text-decoration: none;
    text-align: center;
">
    Docs
</a>
<a align="center" href="https://discord.gg/9QeqHvAd8r" style="
    display: inline-block;
    padding: 5px 10px;
    font-size: 12px;
    color: white;
    background-color:rgb(159, 35, 248);
    border-radius: 5px;
    text-decoration: none;
    text-align: center;
">
    Discord
</a>
<a align="center" href="https://www.patreon.com/bePatron?u=70591568" style="
    display: inline-block;
    padding: 5px 10px;
    font-size: 12px;
    color: white;
    background-color: #f96854;
    border-radius: 5px;
    text-decoration: none;
    text-align: center;
">
    Support on Patreon
</a>
</div>


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
Download the latest installer under releases.

or

Install the app with pip
```sh
pip install comfy-tweaker
```

And run the UI with
```sh
comfy-tweaker
```

Check out the quickstart guide in the docs to get started.

## Troubleshooting
- Windows users should ensure that the paths in their tweaks files use forward slashes
