import os.path
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

# check if storage already exists
PERSIST_DIR = "./storage"
if not os.path.exists(PERSIST_DIR):
    # load the documents and create the index
    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

context = (
    "Context information is below. \n"
    "----------------------\n"
    "{context_str}\n"
    "----------------------\n"
    "Given the context information and not prior knowledge, "
    "If you don't know the answer, tell the user that you can't answer the question - DO NOT MAKE UP AN ANSWER. "
    "Do not make up your own answers, refer only from the given information. "
    "Give exact answers to the questions and only answer if you are sure about the answer."
    "Your answers use correct grammar and your texting style is formal. "
    "Always be friendly, always reply in German! "
)

# Either way we can now query the index
query_engine = index.as_chat_engine(
    context_template = context
)

response = query_engine.query("Was sind die drei zentralen Themen im Text? Nummeriere die Themen von 1 bis 3.")
print(response)