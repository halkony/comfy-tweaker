#This is an example that uses the websockets api to know when a prompt execution is done
#Once the prompt execution is done it downloads the images using the /history endpoint

from loguru import logger
import websockets

import asyncio
import json
import os
import time
import urllib.parse
import urllib.request
import uuid
from io import BytesIO

from filelock import FileLock, Timeout
import websocket  # NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
from PIL import Image, PngImagePlugin

def queue_prompt(prompt, client_id):
    server_address = os.getenv("COMFYUI_SERVER_ADDRESS")
    p = {"prompt": prompt, "client_id": str(client_id)}
    data = json.dumps(p).encode('utf-8')
    req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    server_address = os.getenv("COMFYUI_SERVER_ADDRESS")
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()

def get_history(prompt_id):
    server_address = os.getenv("COMFYUI_SERVER_ADDRESS")
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())

def add_job_metadata_to_image(image_path, job):
    lock_path = f"{image_path}.lock"
    lock = FileLock(lock_path, timeout=20)
    try:
        with lock:
            img = Image.open(image_path)
            img.info['workflow'] = json.dumps(job.workflow.gui_workflow)
            img.info['tweaks'] = json.dumps(job.tweaks._original_yaml)
            metadata = PngImagePlugin.PngInfo()
            for k, v in img.info.items():
                metadata.add_text(k, v)
            img.save(image_path, "PNG", pnginfo=metadata)
    except Timeout:
        logger.error(f"Failed to acquire lock for {image_path}. Image taking too long to write from ComfyUI?")

async def generate_images(ws, job):
    """
    Generate the images, and write the GUI workflow into the resulting file.
    """
    workflow = job.workflow
    prompt = workflow.api_workflow
    prompt_id = queue_prompt(prompt, job.client_id)['prompt_id']

    if not os.environ.get("COMFYUI_OUTPUT_FOLDER"):
        raise ValueError("COMFYUI_OUTPUT_FOLDER is not set. This is required to save the images.")

    history_check_timer = time.time()
    while True:
        # if time.time() - history_check_timer > 15:  # Check every 5 seconds
        #     try:
        #         get_history(prompt_id)[prompt_id]
        #         break
        #     except KeyError:
        #         history_check_timer = time.time()

        out = await ws.recv()
        try:
            message = json.loads(out)

            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    logger.info("Prompt is done executing.")
                    break #Execution is done
                else:
                    continue
        except:
            pass

        try:
            bytesIO = BytesIO(out[8:])
            # If you want to be able to decode the binary stream for latent previews, here is how you can do it:
            # preview_image = Image.open(bytesIO).resize((512, 512)) # This is your preview in PIL image format, store it in a global

            # we shouldm monitor if this bogs down systems with huge image workflows
            job.preview_image = bytesIO.getvalue()
            continue #previews are binary data
        except:
            continue

    # this code is executed after the workflow is done executing
    logger.info("Getting outputs from prompt history...")
    history = get_history(prompt_id)[prompt_id]
    for node_id in history['outputs']:
        node_output = history['outputs'][node_id]
        if 'images' in node_output:
            for image in node_output['images']:
                # we have to use the comfyui output folder to reconstruct the path of the image and apply our metadata
                if "ComfyUI_temp" in image["filename"]:
                    # Comfyui writes these files for things like image previews, which we don't want to write GUI data too
                    # as far as I can tell, comfy deletes them after the workflow is done
                    continue
                logger.info(f"Found an output image named {image['filename']}...")
                comfyui_output_folder = os.getenv("COMFYUI_OUTPUT_FOLDER")

                image_path = os.path.join(comfyui_output_folder, image['subfolder'], image['filename'])
                if os.path.dirname(image_path) == os.path.join(comfyui_output_folder, "output"):
                    # this is a special case, when saved to root output folder
                    # if the subfolder is the root comfyui output folder, we don't need to re add the subfolder
                    image_path = os.path.join(comfyui_output_folder, image['filename'])

                # the API workflow is already written in 'prompt', we just have to write 'workflow'
                # this wave of writing out the metadata requires loading the image into memory
                # this takes a long time with 4096x4096 images but is fine for general use
                gui_workflow_data = json.dumps(workflow.gui_workflow)

                # we need a lock on the file because when comfyUI is working quickly,
                # it can say a job is done but still be writing to a file
                try:
                    add_job_metadata_to_image(image_path, gui_workflow_data)
                except Timeout:
                    logger.info(f"Failed to acquire lock for {image_path}. Image taking too long to write?")
                    break
                logger.info(f"Successfully saved gui workflow to {image['filename']}...")

                # this feels naughty in the ComfyUI module, but im not sure how
                # else to store this information
                job.output_location = image_path

async def run_job_on_server(job):
    server_address = os.getenv("COMFYUI_SERVER_ADDRESS")
    uri = f"ws://{server_address}/ws?clientId={job.client_id}"

    async with websockets.connect(uri) as ws:
        # turn the prompt into a string
        images = await generate_images(ws, job)
        # The connection will be automatically closed when exiting the async with block

import aiohttp


async def check_if_connected():
    server_address = os.getenv("COMFYUI_SERVER_ADDRESS")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"http://{server_address}/", timeout=1) as response:
                return response.status == 200
        except aiohttp.ClientError:
            return False
        except asyncio.TimeoutError:
            return False

# for in case this example is used in an environment where it will be repeatedly called, like in a Gradio app. otherwise, you'll randomly receive connection timeouts
#Commented out code to display the output images:

# for node_id in images:
#     for image_data in images[node_id]:
#         from PIL import Image
#         import io
#         image = Image.open(io.BytesIO(image_data))
#         image.show()
