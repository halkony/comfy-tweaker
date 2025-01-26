from __future__ import annotations
from typing import ClassVar

from loguru import logger

__version__ = "0.1.2"

import asyncio
import json
import re
import threading
import time
import traceback
import uuid
from copy import copy, deepcopy
from dataclasses import dataclass, field
from datetime import timedelta
from enum import Enum
import functools
from comfy_tweaker.plugins import PluginType

from jinja2 import Environment, Template
from PIL import Image
from yaml import safe_dump, safe_load

from comfy_tweaker.plugins import Plugin
from comfy_tweaker.comfyui import run_job_on_server
from comfy_tweaker.exceptions import (IncompleteImageWorkflowError,
                                      InvalidSelectorError, NodeFieldNotFound,
                                      NodeNotFoundError,
                                      NonUniqueSelectorError)


# Filters
class JobStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Job:
    """
    A job is a workflow with specified tweaks that is sent to the server for processing. It has a status that is updated as the job progresses.
    """
    workflow: Workflow
    tweaks: Tweaks
    status: JobStatus = JobStatus.PENDING
    id: uuid.UUID = field(default_factory=uuid.uuid4, init=False)
    output_location: str = field(default="", init=False)
    preview_image: Image = field(default=None, init=False)
    amount: int = field(default=1)
    progress: int = field(default=0, init=False)

    @property
    def remaining(self):
        return self.amount - self.progress

    def __post_init__(self):
        self.original_workflow = deepcopy(self.workflow)

@dataclass
class JobQueue:
    """
    A job queue manages a list of jobs. Starting the queue sends the next job to the server. Stopping the queue will stop further processing after the current job has been completed.
    """
    queue: list[Job] = field(default_factory=list)
    _stop_event: asyncio.Event = field(default_factory=asyncio.Event, init=False)
    history: list[Job] = field(default_factory=list)

    def __post_init__(self):
        self._running_thread_lock = threading.Lock()

    def add(self, workflow, tweaks, amount=1, validate=True):
        """Add a job to the queue with the provided workflows and tweaks. If validate is set to True, the workflow will be validated before it is added to the queue.

        Args:
            workflow (Workflow): the workflow you want to run on ComfyUI
            tweaks (Tweaks): the tweaks that will be applied to the workflow at runtime
            validate (bool, optional): Whether or not the workflow should be validated before adding to the queue. Defaults to True.
            amount (int, optional): The amount of times the job should be run. Defaults to 1.
        """
        if validate:
            workflow.validate(tweaks)
        self.queue.append(Job(workflow, tweaks, amount=amount))

    @property
    def running(self):
        """Returns True if the queue is currently in progress, False otherwise."""
        return not self._stop_event.is_set()

    def remove(self, job_id):
        """Removes the job with the specified id from the queue.

        Args:
            job_id (UUID): the id of the job you want to remove

        Raises:
            KeyError: If the job is not found in the queue
        """
        for i, job in enumerate(self.queue):
            if job.id == job_id:
                self.queue.pop(i)
                return
        for i, job in enumerate(self.history):
            if job.id == job_id:
                self.history.pop(i)
                return
        raise KeyError("Job not found in queue or history: id" + str(job_id))

    def clear(self):
        """
        Clears the queue and history.
        """
        self.queue = []
        self.history = []

    @property
    def remaining(self):
        """Returns the total amount of generations remaining, summing up the amounts from each current job."""
        return len(self.queue)

    @property
    def running(self):
        """Returns True if the queue is currently in progress, False otherwise."""
        return not self._stop_event.is_set()

    @property
    def all_jobs(self):
        """Returns all jobs, including those that have already been completed."""
        return self.queue + self.history

    def position_of(self, job_id):
        """Returns the positiong of the job with the specified id in the queue. If the job is not found, returns None.

        Args:
            job_id (UUID): the id of the job you want to find

        Returns:
            int, None: the position of the job in the queue
        """
        for i, job in enumerate(self.queue):
            if job.id == job_id:
                return i + 1
        return None

    def restart(self):
        """Restarts an active queue."""
        self._stop_event.clear()

    @property
    def mid_job(self):
        return self._running_thread_lock.locked()

    def start(self):
        """Starts a queue that is not currently in progress."""
        with self._running_thread_lock:
            logger.info("Starting queue...")
            self._stop_event.clear()
            while self.queue:
                logger.info("Starting next job in queue...")
                try:
                    job = self.queue[0]
                    if self._stop_event.is_set():
                        logger.info("The queue is paused. Waiting for resume.")
                        return
                    # run the workflow
                    logger.info("Sending workflow to server...")
                    for i in range(job.remaining):
                        if not self.queue:
                            break
                        if self._stop_event.is_set():
                            logger.info("The queue is paused. Waiting for resume.")
                            job.status = JobStatus.PENDING
                            while self._stop_event.is_set():
                                time.sleep(1)
                        if self.queue[0] != job:
                            logger.info("Job no longer at front of queue. Breaking out of loop...")
                            job.status = JobStatus.PENDING
                            break
                        job.status = JobStatus.IN_PROGRESS
                        start_time = time.time()
                        job.workflow = job.original_workflow.apply_tweaks(job.tweaks)
                        # regenerate the tweaks for new random values and to add one to iteration
                        job.tweaks = job.tweaks.regenerate()
                        logger.info(f"Running job ({job.progress + 1}/{job.amount})...")
                        run_job_on_server(job)
                        job.progress = i + 1
                        end_time = time.time()
                        elapsed_time = timedelta(seconds=end_time - start_time)
                        logger.info(f"Total time taken: {elapsed_time}")
                    else:
                        job.progress = job.amount
                        job.status = JobStatus.COMPLETED
                        self.history.append(self.queue.pop(0))
                except Exception as e:
                    traceback.print_exc()
                    job.status = JobStatus.FAILED
                    logger.info(f"Job failed with error: {e}")
                    logger.info("Stopping the queue...")
                    traceback.print_exc()
                    self.history.append(self.queue.pop(0))
                    self.stop()
                    return
            logger.info("Queue completed.")

    def stop(self):
        """Stops the queue, preventing further processing after the current job has been completed."""
        self._stop_event.set()


@dataclass
class Workflow:
    gui_workflow: dict[str, str] = field(default_factory=dict)
    api_workflow: dict[str, str] = field(default_factory=dict)
    name: str = "Default Workflow"

    @classmethod
    def from_image(cls, image_path, name="Default Workflow"):
        """Creates a workflow from the "workflow" and "prompt" metadata on an image. The image requires both metadata to be present, otherwise an IncompleteImageWorkflowError is raised.

        The workflow metadata is needed to reconstruct the GUI after generation, and the prompt metadata is needed to repopulate the GUI workflow with any dynamically determined values (e.g. wildcards)."""
        with Image.open(image_path) as image:
            try:
                metadata = image.info
                gui_workflow = json.loads(metadata["workflow"])
                api_workflow = json.loads(metadata["prompt"])
            except KeyError as e:
                traceback.print_exc()
                missing_key = re.search(r"'(.+)'", str(e)).group(1)
                raise IncompleteImageWorkflowError(f"The provided image does not have the required metadata: \"{missing_key}\"")
            return cls(gui_workflow, api_workflow, name=name)

    def save(self, gui_workflow_path, api_workflow_path=None):
        """Saves the GUI workflow and optionally an API workflow to the specified paths."""
        with open(gui_workflow_path, "w") as gui_file:
            json.dump(self.gui_workflow, gui_file)
        if api_workflow_path:
            with open(api_workflow_path, "w") as api_file:
                json.dump(self.api_workflow, api_file)

    def find_gui_node(self, selector):
        """Find a node in the GUI workflow using the provided selector. If the selector is not unique, a NonUniqueSelectorError is raised. If the node is not found, a NodeNotFoundError is raised.

        Args:
            selector (dict[str, str]): a dictionary with either a "name" or "id" key

        Returns:
            dict[any, any]: returns the json gui node from the workflow
        """
        def node_filter(node):
            if selector.get("name"):
                return node.get("title", "") == selector["name"] == selector["name"]
            elif selector.get("id"):
                return str(node["id"]) == str(selector["id"])
        if selector.get("name"):
            nodes = list(filter(node_filter, self.gui_workflow["nodes"]))
            if len(nodes) > 1:
                raise NonUniqueSelectorError("Multiple nodes with the same name found")
            if len(nodes) == 0:
                raise NodeNotFoundError(f'Node with the provided name not found: {selector.get("name")}')
            return nodes[0]
        elif selector.get("id"):
            nodes = list(filter(node_filter, self.gui_workflow["nodes"]))
            if len(nodes) > 1:
                raise NonUniqueSelectorError("Multiple nodes with the same id found")
            if len(nodes) == 0:
                raise NodeNotFoundError(f"Node with the provided id not found: {selector.get('id')}")
            return nodes[0]

    def find_api_node(self, selector):
        """Find a node in the API workflow using the provided selector. If the selector is not unique, a NonUniqueSelectorError is raised. If the node is not found, a NodeNotFoundError is raised.

        Args:
            selector (dict[str, str]): a dictionary with either a "name" or "id" key

        Returns:
            dict[any, any]: returns the json api node from the workflow
        """
        if selector.get("id"):
            try:
                return self.api_workflow[selector['id']]
            except KeyError:
                traceback.print_exc()
                raise NodeNotFoundError(f"Node with the provided id not found: {selector.get('id')}")
        elif selector.get("name"):
            def node_filter(node):
                if node.get("_meta"):
                    return node["_meta"].get("title") == selector["name"]
                return False
            nodes = list(filter(node_filter, self.api_workflow.values()))
            if len(nodes) > 1:
                traceback.print_exc()
                raise NonUniqueSelectorError("Multiple nodes with the same name found")
            elif len(nodes) == 0:
                traceback.print_exc()
                raise NodeNotFoundError(f"Node with the provided name not found: {selector.get('name')}")
            return nodes[0]

    def validate(self, tweaks: Tweaks):
        """This function simply applies tweaks, and passes up an error if it fails."""
        try:
            # print("Validating tweaks by applying them to the workflow...")
            self.apply_tweaks(tweaks)
            # print("Tweaks are valid with this workflow.")
        except Exception as e:
            traceback.print_exc()
            logger.error(f"Error validating tweaks: {type(e).__name__} {e}")
            raise e

    def apply_tweaks(self, tweaks):
        """Creates a new workflow with the tweaks applied. The original workflow is not modified."""
        # look for the nodes in the gui_workflow using the selector

        # copy is required here otherwise we end up mutating that state of our original workflow
        resulting_workflow = Workflow(copy(self.gui_workflow), copy(self.api_workflow))

        for tweak in tweaks.tweaks:
            # use the selector in the tweak to find the node in the gui_workflow
            gui_node = resulting_workflow.find_gui_node(tweak.selector)
            api_node = resulting_workflow.find_api_node(tweak.selector)
            for field_name, change in tweak.changes.items():
                # print(f"Tweaking {tweak.selector} field \"{field_name}\" to \"{change}\"...")
                # use the position of field_name inside the api workflow to change the value of "widgetValues"
                # get the position of field name in api_node["inputs"] so we can populate the widget values list
                # if the field name's value in the API workflow is a list, that means its a model link
                # which for our application, I don't mind overwriting
                try:
                    widget_value_index = list(api_node['inputs'].keys()).index(field_name)
                except ValueError:
                    traceback.print_exc()
                    raise NodeFieldNotFound(f"Field \"{field_name}\" was not found for selector {tweak.selector}")
                # calculate the data with the changes
                new_widget_values = gui_node["widgets_values"]
                new_widget_values[widget_value_index] = change
                api_node["inputs"][field_name] = change

                # apply changes to the resulting workflow
                for node in resulting_workflow.gui_workflow["nodes"]:
                    if node["id"] == gui_node["id"]:
                        node["widgets_values"] = new_widget_values
                resulting_workflow.api_workflow.update({gui_node["id"]: api_node})
        return resulting_workflow

@dataclass(frozen=True)
class Tweak:
    selector: dict[str, str] = field(default_factory=dict)
    changes: dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        valid_selectors = ["id", "name"]
        provided_selectors = list(set(self.selector.keys()) & set(valid_selectors))
        if len(provided_selectors) == 0:
            raise InvalidSelectorError("Tweak must have a valid selector")
        if len(provided_selectors) > 1:
            raise InvalidSelectorError(f"Tweak must have only one selector from the following {valid_selectors}")
        if provided_selectors[0] == "id":
            # we need to cast ids as strings for direct comparison with
            # the comfyui workflows
            self.selector["id"] = str(self.selector["id"])

@dataclass(frozen=True)
class Tweaks:
    tweaks: list[Tweak] = field(default_factory=list)
    name: str = "Default Tweaks"
    _original_yaml: str = field(default="")
    _iteration: int = field(default=0)

    _plugins_initialized: ClassVar[bool] = field(default=False, init=False)

    def __len__(self):
        return len(self.tweaks)

    def initialize_plugins():
        # runs all the registered tweaks plugins inside of filters
        if Tweaks._plugins_initialized:
            return
        else:
            import comfy_tweaker.filters

    def regenerate(self):
        """Regenerates the tweaks from the original yaml. Call this function if you want regenerate random numbers or selections.

        Returns:
            Tweaks: a new Tweaks object with the same tweaks as the original with all random values regenerated
        """
        return Tweaks.from_yaml(self._original_yaml, name=self.name, iteration=self._iteration + 1)

    def save(self, tweaks_file_path):
        """Save the tweaks to a yaml file.

        Args:
            tweaks_file_path (str): the path to the file where the tweaks will be saved
        """
        with open(tweaks_file_path, "w") as file:
            tweaks_yaml = {"tweaks": [{"selector": tweak.selector, "changes": tweak.changes} for tweak in self.tweaks]}
            safe_dump(tweaks_yaml, file)

    def add(self, tweak):
        return Tweaks(self.tweaks + [tweak])

    @classmethod
    def register(cls, plugin_name=None, plugin_type=PluginType.GLOBALS):
        """Registers a function for use as a Jinja filter. If plugin name is not provided, defaults to the function name."""
        def decorator(func):
            if not plugin_name:
                _plugin_name = func.__name__
            plugin = Plugin(_plugin_name, func, plugin_type)
            cls.plugins.append(plugin)
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @classmethod
    def environment(cls):
        env = Environment()
        for plugin in cls.plugins:
            if plugin.plugin_type == PluginType.GLOBALS:
                env.globals[plugin.name] = plugin.func
            elif plugin.plugin_type == PluginType.FILTERS:
                env.filters[plugin.name] = plugin.func
        return env

    @classmethod
    def from_yaml(cls, yaml_string, name="Default Tweaks", iteration=0):
        """Import tweaks from a yaml string. The iteration key argument is a custom variable passed into the yaml. This way people can use jinja to modify their workflows."""
        cls.initialize_plugins()
        env = Tweaks.environment()
        env.globals["iteration"] = iteration
        if yaml_string:
            template = env.from_string(yaml_string)
            rendered_yaml = safe_load(template.render())
            result = cls([Tweak(tweak["selector"], tweak["changes"]) for tweak in rendered_yaml["tweaks"]], name=name, _original_yaml=yaml_string, _iteration=iteration)
        else:
            result = cls(name=name)
        return result

    @classmethod
    def from_file(cls, tweaks_file_path, name="Default Tweaks"):
        """Import tweaks from a yaml file. Renders the template with jinja before returning."""
        with open(tweaks_file_path) as file:
            return cls.from_yaml(file.read(), name=name)

Tweaks.plugins = []