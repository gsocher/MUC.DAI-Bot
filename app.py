import os
import openai
import gradio as gr
#import nest_asyncio
import time
import asyncio
#nest_asyncio.apply()

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings

Settings.llm = OpenAI(model="gpt-3.5-turbo-0125")
# change to Huggingface embedding model 
Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")
Settings.node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=128)
Settings.num_output = 512
Settings.context_window = 3900


from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    PromptTemplate,
    load_index_from_storage
)

from llama_index.readers.file import PyMuPDFReader

from theme import CustomTheme  

system_prompt = (
    "You are a helpful assistant in the Bavarian ministry of science and education. "
)

context = (
    "Context information is below. \n"
    "----------------------\n"
    "{context_str}\n"
    "----------------------\n"
    "Given the context information and not prior knowledge, "
    "If you don't know the answer, tell the user that you can't answer the question - DO NOT MAKE UP AN ANSWER. "
    "Do not make up your own answers, refer only from the given information. "
    "Your answers use correct grammar and your texting style is casual. "
    "Always be friendly, always reply in German! "
    "Put the page number of the information that you are referring to in brackets after the answer. "
)

prompt = (
    "Context information is below. \n"
    "----------------------\n"
    "{context_str}\n"
    "----------------------\n"
    "Given the context information and not prior knowledge, "
    "If you don't know the answer, tell the user that you can't answer the question - DO NOT MAKE UP AN ANSWER. "
    "Do not make up your own answers, refer only from the given information. "
    "Your answers use correct grammar and your texting style is casual. "
    "Always be friendly, always reply in German! "
    "Put the page number of the information that you are referring to in brackets after the answer. "
)

prompt_template = PromptTemplate(prompt)



# check if storage already exists
if not os.path.exists("./storage"):
    # load the documents and create the index
    #documents = SimpleDirectoryReader("data").load_data()
    loader = PyMuPDFReader()
    documents = loader.load(file_path="./data/Rahmenvereinbarung-2023-2027_ohne-Unterschrift.pdf")
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist()
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context)

chat_engine = index.as_chat_engine(
    chat_mode= "context", system_prompt=system_prompt, context_template=context)

query_engine = index.as_query_engine(streaming=True)
#query_engine = index.as_query_engine(similarity_top_k=5)
query_engine.update_prompts(
    {"response_synthesizer:text_qa_template": prompt_template}
)


default_text="Ich beantworte Fragen zur Rahmenvereinbarung Hochschulen 2023 - 2027 gemäß Art. 8 Abs. 1 BayHIG. Wie kann ich helfen?"

bot_examples = [
    "Was sind die 3 zentralen Themen im Text?",
    "Erstelle jeweils eine Zusammenfassung zu den zentralen Themen",
    "Welche Vereinbarungen wurden zwischen den Universitäten und dem Ministerium getroffen?",
    "Wie unterscheiden sich die Vereinbarungen der Universitäten von den Vereinbarungen der Hochschulen für angewandte Wissenschaften?",
    "Welche Maßnahmen sind zum Ausbau der Wissenschaftskommunikation vorgesehen?",
]

submit_button = gr.Button(
    value="Ask me",
    elem_classes=["ask-button"],
)

def response(message, history):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    histories = chat_engine.chat_history
    answer = chat_engine.stream_chat(message, chat_history=histories)

    output_text = ""
    for token in answer.response_gen:
        time.sleep(0.1)

        output_text += token
        yield output_text

    #return str(answer)


def main():
    openai.api_key = os.environ["OPENAI_API_KEY"]
    custom_theme = CustomTheme()

    desc = "[Rahmenvereinbarung Hochschulen 2023 - 2027 gemäß Art. 8 Abs. 1 BayHIG](https://www.stmwk.bayern.de/download/22215_Rahmenvereinbarung_inkl_Unterschriften.pdf%C2%A0)"

    # default_text noch einbauen
    chatbot = gr.Chatbot(
        layout='bubbles',
        #height=600,
        value=[[None, default_text]]
    )

    chat_interface = gr.ChatInterface(
        fn=response,
        retry_btn=None,
        undo_btn=None,
        title="MUC.DAI Chatbot",
        submit_btn=submit_button,
        clear_btn=None,
        theme=custom_theme,
        chatbot=chatbot,
        description=desc,
        css="style.css",
        examples=bot_examples,
    )

    chat_interface.launch(inbrowser=True, debug=True)


if __name__ == "__main__":
    main()
