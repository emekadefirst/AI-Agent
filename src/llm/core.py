import asyncio
import logging
import json
from src.configs.env import GEMINI_API_KEY
from src.llm.prompt import SYSTEM_PROMPT
from src.tools.registry import tools
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

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

# Create agent WITHOUT tools first (for general chat)
agent = create_agent(
    model, 
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)

def extract_text_content(msg: BaseMessage) -> str:
    """Extract text from Gemini's content list structure."""
    if not hasattr(msg, 'content') or msg.content is None:
        return ""
    
    content = msg.content
    
    # Handle Gemini's structured content
    if isinstance(content, list):
        text_parts = []
        for block in content:
            if isinstance(block, dict):
                if block.get('type') == 'text':
                    text_parts.append(block.get('text', ''))
                # Handle tool calls or other structured content
                elif 'text' in block:
                    text_parts.append(str(block['text']))
            elif isinstance(block, str):
                text_parts.append(block)
        return ' '.join(text_parts).strip()
    
    elif isinstance(content, str):
        return content.strip()
    
    return str(content).strip()


def get_session_config(session_id: str) -> dict:
    """Get configuration for agent stream with session context."""
    return {
        "configurable": {
            "thread_id": session_id
        }
    }


async def stream_response(user_input: str, session_id: str, client_history: str = None):
    """Resume from client-stored history + save new messages."""
    try:
        config = get_session_config(session_id)
        
        # Parse client history (fallback to empty)
        initial_messages = []
        if client_history:
            try:
                history = json.loads(client_history)
                for msg in history[-10:]:  # Last 10 messages max
                    if msg['sender'] == 'user':
                        initial_messages.append(HumanMessage(content=msg['content']))
                    elif msg['sender'] == 'ai':
                        initial_messages.append(AIMessage(content=msg['content']))
            except:
                pass
        
        # Add new user input
        initial_messages.append(HumanMessage(content=user_input))
        
        input_state = {"messages": initial_messages}
        full_response = []

        # Stream with full context
        async for chunk in agent.astream(input_state, config=config, stream_mode="values"):
            if "messages" in chunk:
                latest_msg = chunk["messages"][-1]
                if isinstance(latest_msg, AIMessage):
                    content = extract_text_content(latest_msg)
                    if content and content not in full_response[-1:] if full_response else True:
                        full_response.append(content)
                        yield f"data: {content}\n\n"

        yield "data: [DONE]\n\n"
        
    except Exception as e:
        yield f"data: ⚠️ Error: {str(e)}\n\n"