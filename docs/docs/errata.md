## Why do I have to specify an image and not a workflow JSON?
ComfyUI uses two JSON styles for managing workflows -- the visual workflow for use in the web UI and one the API workflow that the computer runs directly.

Normally, workflows queued from other programs do not have the visual workflow attached to them. But ComfyTweaker uses a workaround that attaches it after generation. This requires both versions of the JSON, which are conveniently paired any workflow generated image.

ComfyTweaker will eventually support import JSON workflows directly.

## When I move to front, the numbers change but the job doesn't move.

Either right click, Refresh or add another job to get it to update. This is a known bug.