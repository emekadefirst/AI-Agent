from pathlib import Path
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse, HTMLResponse
from src.llm.core import stream_response

app = FastAPI()

@app.get("/stream")
async def chat_stream(
    prompt: str = Query(...),
    session_id: str = Query("default"),
    history: str = Query(None)  # Client sends last 10 messages
):
    async def event_generator():
        async for token in stream_response(prompt, session_id, history):
            yield token
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/", response_class=HTMLResponse)
async def chat_page():
    html_path = Path("src/templates/chat.html")
    return html_path.read_text(encoding="utf-8")
