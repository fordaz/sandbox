import os
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    load_index_from_storage,
    StorageContext,
)
from llama_index.core.chat_engine.types import BaseChatEngine, ChatMode
from llama_index.llms.openai import OpenAI
from utils import ChatbotArgs, parse_chatbot_args

args: ChatbotArgs = parse_chatbot_args()

print(
    f"Using:\nChat mode: '{args.chat_mode}'\nSystem prompt: '{args.system_prompt}'\nDocs: {args.raw_data_dir}"
)

llm = OpenAI(
    model="gpt-4",
    system_prompt=args.system_prompt,
)

if os.path.exists(f"{args.persistence_index_dir}/docstore.json"):
    print(f"Loading existing index ...")
    storage_context = StorageContext.from_defaults(persist_dir=args.persistence_index_dir)
    vector_index = load_index_from_storage(storage_context)
else:
    print(f"Loading raw data and indexing it ...")
    data = SimpleDirectoryReader(input_dir=args.raw_data_dir).load_data()
    # we use the storage context for persisting our index
    storage_context = StorageContext.from_defaults()
    # the in memory index that allows the chat to find relevant pieces of content
    vector_index = VectorStoreIndex.from_documents(
        data, show_progress=True, storage_context=storage_context
    )
    # saving the index for future use
    vector_index.storage_context.persist(persist_dir=args.persistence_index_dir)


def interact_with_user(chat: BaseChatEngine):
    usr_msg = ""
    while True:
        usr_msg = input("\nHow can I help you?\n")
        if usr_msg.lower() != "bye":
            response = chat.chat(usr_msg)
            print(response)
        else:
            return


# best, condense_question, context, condense_plus_context
chat_engine: BaseChatEngine = vector_index.as_chat_engine(
    chat_mode=args.chat_mode, llm=llm, verbose=True
)

interact_with_user(chat_engine)
