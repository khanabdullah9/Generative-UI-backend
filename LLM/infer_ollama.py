from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import requests
import time
import json

import utils


BASE_URL = utils.construct_llm_url()
SOURCE = utils.get_llm_source()

# default LLM is ollama # utilize SOURCE to instantiate other llm classes
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
            "output": utils.get_form_layout()
        }
    ]
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a senior UI architect"),
    ("system", "You are supposed to design the layout for react based forms and describe them in json."),
    ("system", "You are only supposed to return JSON"),
    ("system", f"Supported field types are {utils.get_supported_field_types()}"),
    few_shot_prompt,
    ("user", "{user_prompt}")
])
partial_prompt = prompt.partial(format_instructions=parser.get_format_instructions())

# ollama_chain = prompt | llm
ollama_chain = partial_prompt | llm | parser


def is_ollama_running():
    try:
        response = requests.get(f"{BASE_URL}/api/tags", timeout=30)
        utils.log_info(f"pinging pod .... -> {str(response.status_code)}")
        return response.status_code == 200
    except Exception as err:
        utils.log_error(str(err))
        return False

def execute_chain(prompt: str):
    try:
        start = time.perf_counter()
        response = ollama_chain.invoke({
            "user_prompt": prompt
        })
        end = time.perf_counter()

        utils.log_info(f"Exec time: {(end - start)}s")
        return response
    except Exception as err:
        utils.log_error(str(err))
        return {}


def calculate_num_tokens(prompt: str):
    rendered_prompt = partial_prompt.format(user_prompt=prompt)
    return len(rendered_prompt)