from pathlib import Path
from fastapi import FastAPI, Query
from src.llm.base import stream_response
from fastapi.responses import StreamingResponse, HTMLResponse

app = FastAPI()

@app.get("/stream")
async def chat_stream(prompt: str = Query(...)):
    async def event_generator():
        async for token in stream_response(prompt):
            yield f"data: {token}\n\n"

        # optional: signal completion
        yield "event: end\ndata: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@app.get("/", response_class=HTMLResponse)
async def chat_page():
    html_path = Path("src/templates/chat.html")
    return html_path.read_text(encoding="utf-8")