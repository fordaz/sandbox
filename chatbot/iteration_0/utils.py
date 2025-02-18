import argparse
from dataclasses import dataclass

from llama_index.core.chat_engine.types import ChatMode

# where the raw text data will be stored
RAW_TXT_0_DATA_DIR = "./data/txt_0"
RAW_TXT_1_DATA_DIR = "./data/txt_1"

# where the vector index will be saved
PERSISTENCE_INDEX_0_DIR = "./data/persistence_0"
PERSISTENCE_INDEX_1_DIR = "./data/persistence_1"

# Very simple instruction to prompt the model as a philosophy chatbot
SYSTEM_PROMPT_V0 = "You are a helpful chatbot assistant, specialized in providing support for an opensource called Relminer."
SYSTEM_PROMPT_V1 = "You are a helpful chatbot assistant, specialized in providing support for an opensource called Relminer. If the relevant context for the answer is not provided, avoid coming up with logical explanations and just say you don't know."

parser = argparse.ArgumentParser(
    description="A Q&A Chatbot for the RelMiner documentation"
)
parser.add_argument(
    "--mode",
    type=str,
    help="The chat mode, ex: best, condense_question, context, condense_plus_context",
    default="best",
)
parser.add_argument(
    "--prompt",
    type=str,
    help="The version of the prompt to use, ex: v0, v1",
    default="v0",
)
parser.add_argument(
    "--docs",
    type=str,
    help="To use the basic document or the one with pricing information, ex: basic, pricing",
    default="basic",
)


@dataclass
class ChatbotArgs:
    system_prompt: str
    chat_mode: ChatMode
    raw_data_dir: str
    persistence_index_dir: str

def parse_chatbot_args():
    args = parser.parse_args()

    system_prompt = SYSTEM_PROMPT_V0 if args.prompt == "v0" else SYSTEM_PROMPT_V1

    chat_mode = (
        args.mode
        if args.mode in ["best", "condense_question", "context", "condense_plus_context"]
        else "condense_plus_context"
    )
    chat_mode = getattr(ChatMode, chat_mode.upper())

    raw_data_dir = RAW_TXT_0_DATA_DIR if args.docs == "basic" else RAW_TXT_1_DATA_DIR

    persistence_index_dir = (
        PERSISTENCE_INDEX_0_DIR if args.docs == "basic" else PERSISTENCE_INDEX_1_DIR
    )

    return ChatbotArgs(
        system_prompt, chat_mode, raw_data_dir, persistence_index_dir
    )
