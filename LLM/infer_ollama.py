from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import requests
import time
import json

from utils import get_ollama_conf, log_error, log_info, get_form_layout, get_supported_field_types, EMPTY_DICT

OLLAMA_CONF = get_ollama_conf()
POD_ID = OLLAMA_CONF["POD_ID"]
PORT = OLLAMA_CONF["PORT"]
BASE_URL = f"https://{POD_ID}-{str(PORT)}.proxy.runpod.net"

llm = ChatOllama(
    model="llama3:8b",
    base_url=BASE_URL,
    num_ctx=4096,
    num_predict=1024,
    temperature=0
)

parser = JsonOutputParser()

pre_prompt = ChatPromptTemplate.from_messages([
    ("user", "{prompt}"),
    ("assistant", "{output}")
])

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=pre_prompt,
    examples=[
        {
            "prompt": "Create a form to collect student data for admission.",
            "output": get_form_layout()
        }
    ]
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a senior UI architect"),
    ("system", "You are supposed to design the layout for react based forms and describe them in json."),
    ("system", "You are only supposed to return JSON"),
    ("system", f"Supported field types are {get_supported_field_types()}"),
    few_shot_prompt,
    ("user", "{user_prompt}")
])
partial_prompt = prompt.partial(format_instructions=parser.get_format_instructions())

# ollama_chain = prompt | llm
ollama_chain = partial_prompt | llm | parser


def is_ollama_running():
    try:
        response = requests.get(f"{BASE_URL}/api/tags", timeout=5)
        log_info(f"pinging pod .... -> {str(response.status_code)}")
        return response.status_code == 200
    except Exception as err:
        log_error(str(err))
        return False

def execute_chain(prompt: str):
    try:
        form_layout = get_form_layout()
        if not form_layout:
            return EMPTY_DICT

        start = time.perf_counter()
        response = ollama_chain.invoke({
            "form_layout": form_layout,
            "user_prompt": prompt
        })
        end = time.perf_counter()

        log_info(f"Exec time: {(end - start)}s")
        return json.dumps(response)
    except Exception as err:
        log_error(str(err))
        return EMPTY_DICT


def calculate_num_tokens(prompt: str):
    rendered_prompt = partial_prompt.format(user_prompt=prompt)
    return len(rendered_prompt)