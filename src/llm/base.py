# from typing import Optional, List, Dict, Any, Tuple
# from src.configs.env import GEMINI_API_KEY
# from src.llm.prompt import active_prompt
# from src.configs.http import AsyncHTTPRequest, Methods
# from sr tools.registry import ToolRegistry
# from src.libs.amadeus.core.flight import AmadeusFlightTool
# from src.libs.amadeus.core.hotel import AmadeusHotelTool

# class GeminiService:
#     URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

#     @classmethod
#     def _build_payload(
#         cls,
#         prompt: str,
#         history: Optional[List[Dict[str, Any]]] = None,
#     ) -> Dict[str, Any]:
#         contents = history or []

#         if not contents:
#             contents.append({
#                 "role": "user",
#                 "parts": [{"text": active_prompt}]
#             })

#         contents.append({
#             "role": "user",
#             "parts": [{"text": prompt}]
#         })

#         payload = {
#             "contents": contents,
#             "generationConfig": {
#                 "temperature": 0.7,
#                 "maxOutputTokens": 1024,
#             }
#         }

#         # Add tool definitions
#         tool_registry = ToolRegistry()
#         payload["tools"] = tool_registry.as_gemini_tools()

#         return payload

#     @classmethod
#     async def get_response(
#         cls,
#         prompt: str,
#         history: Optional[List[Dict[str, Any]]] = None,
#     ) -> Tuple[Optional[str], List[Dict[str, Any]]]:

#         history = history or []
#         payload = cls._build_payload(prompt, history)

#         response_data = await AsyncHTTPRequest.request(
#             method=Methods.POST,
#             url=cls.URL,
#             json=payload,
#             headers={
#                 "x-goog-api-key": GEMINI_API_KEY,
#                 "Content-Type": "application/json",
#             }
#         )

#         try:
#             # Add user message to history
#             history.append({
#                 "role": "user",
#                 "parts": [{"text": prompt}]
#             })

#             parts = response_data["candidates"][0]["content"]["parts"]
#             response_text = None
#             tool_call = None

#             for part in parts:
#                 if "text" in part:
#                     response_text = part["text"]
#                 elif "functionCall" in part:
#                     tool_call = part["functionCall"]

#             # Handle tool calls
#             if tool_call:
#                 tool_name = tool_call.get("name")
#                 tool_args = tool_call.get("args", {})

#                 try:
#                     # Execute the tool
#                     if tool_name.startswith("flight_") or tool_name in ["search_flight", "get_flight_price", "book_flight"]:
#                         tool_result = await FlightToolRouter.execute(tool_name, tool_args)
#                     elif tool_name.startswith("hotel_") or tool_name in ["fetch_hotel", "fetch_hotel_offers", "fetch_hotel_rating", "book_hotel"]:
#                         tool_result = await HotelToolRouter.execute(tool_name, tool_args)
#                     else:
#                         response_text = f"Tool '{tool_name}' is not yet supported."
#                         tool_result = None

#                     if tool_result is not None:
#                         response_text = f"Tool '{tool_name}' executed successfully. Result: {tool_result}"

#                 except Exception as e:
#                     response_text = f"Error executing tool '{tool_name}': {str(e)}"
#                     import traceback
#                     traceback.print_exc()

#             # Add assistant response to history
#             if response_text:
#                 history.append({
#                     "role": "model",
#                     "parts": [{"text": response_text}]
#                 })

#             return response_text, history

#         except Exception as e:
#             print("Parse error:", response_data, e)
#             return None, history


from src.configs.env import GEMINI_API_KEY
from src.llm.prompt import SYSTEM_PROMPT
from src.tools.registry import tools  
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import logging

# Optional: logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

# --- Initialize LLM ---
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    streaming=True
)


agent = create_agent(model, tools=tools)

async def stream_response(user_input: str):
    """
    Streams responses from the agent including tool execution.
    """
    try:
        # System + user messages
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_input)
        ]

        # async streaming
        for chunk in agent.stream(messages):
            if hasattr(chunk, "content") and chunk.content:
                yield f"data: {chunk.content}\n\n"
        # signal end of stream
        yield "event: end\ndata: done\n\n"

    except Exception as e:
        logger.error(f"Agent streaming error: {e}")
        yield f"data: ⚠️ Error: {str(e)}\n\n"