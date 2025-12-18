"""
exp-001: Modal + iPhone Voice Input
Hypothesis: Modal.com can receive text via POST from iPhone Shortcuts
"""
import modal

image = modal.Image.debian_slim().pip_install("fastapi")
app = modal.App("voice-receiver", image=image)


@app.function()
@modal.fastapi_endpoint(method="POST", docs=True)
def receive_voice(data: dict) -> dict:
    """
    Tar emot text från iPhone Shortcuts (tal-till-text)

    Expected JSON body:
    {"text": "Din dikterade text här"}
    """
    text = data.get("text", "")
    return {
        "status": "success",
        "received": text,
        "length": len(text),
        "message": f"Mottog {len(text)} tecken"
    }


@app.function()
@modal.fastapi_endpoint(method="GET", docs=True)
def health() -> dict:
    """Health check endpoint"""
    return {"status": "ok"}
