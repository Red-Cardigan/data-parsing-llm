# Standard library imports
import random
from abc import ABC
from typing import Dict, List, Optional, Any
import os

# Related third party imports
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from modal import Image, Secret, Stub, method, web_endpoint
# from sentence_transformers import SentenceTransformer

# Local application/library specific imports
# from langchain.chat_models.base import ChatOpenAI
# from langchain.chat_models.base import SimpleChatModel
# from langchain.schema import BaseMessage, ChatResult, AIMessage, ChatGeneration
# from langchain.callbacks import StdOutCallbackHandler

# Constants
NAME = 'embedding'
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"
MODEL_PATH = "/my-model"

# Define a function to download the model to a particular directory
def download_model_to_folder():
    from huggingface_hub import snapshot_download

    os.makedirs(MODEL_PATH, exist_ok=True)

    snapshot_download(
        MODEL_NAME,
        local_dir=MODEL_PATH,
        token=os.environ["HUGGINGFACE_TOKEN"],
    )

# Define the image
image = (
    Image.from_registry("nvcr.io/nvidia/pytorch:22.12-py3")
    .pip_install(
        "torch==2.0.1+cu118", index_url="https://download.pytorch.org/whl/cu118"
    )
    .pip_install(
        "vllm @ git+https://github.com/vllm-project/vllm.git@651c614aa43e497a2e2aab473493ba295201ab20"
    )
    .pip_install("hf-transfer~=0.1")
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
    .run_function(
        download_model_to_folder,
        secret=Secret.from_name("mozart-secret"),
        timeout=60 * 20,
    )
    from langchain.chat_models.base import ChatOpenAI
    from langchain.chat_models.base import SimpleChatModel
    from langchain.schema import BaseMessage, ChatResult, AIMessage, ChatGeneration
    from langchain.callbacks import StdOutCallbackHandler
)

# Initialize stub and auth scheme
stub = Stub(name = NAME)
auth_scheme = HTTPBearer()

# Load model if inside stub
with image.run_inside():
    model = SentenceTransformer(MODEL_PATH)
    model.to('cuda')

# Pydantic models
class JsonObjects(BaseModel):
    json_objects: List[Dict] = Field(..., min_items=1)

# Chat models
class MozartMistral(SimpleChatModel, ABC):
    def __init__(self, model_dir: str, template: str, temperature: float, top_p: float, max_tokens: int, presence_penalty: float):
        self.model_dir = model_dir
        self.template = template
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.presence_penalty = presence_penalty

    def __enter__(self):
        from vllm import LLM, SamplingParams
        from sentence_transformers import SentenceTransformer
        self.llm = LLM(self.model_dir)

    def _generate(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[StdOutCallbackHandler] = None,
            **kwargs: Any,
    ) -> ChatResult:
        user_questions = [message.content for message in messages]
        prompts = [self.template.format(system="", user=q) for q in user_questions]
        sampling_params = SamplingParams(
            temperature=self.temperature,
            top_p=self.top_p,
            max_tokens=self.max_tokens,
            presence_penalty=self.presence_penalty,
        )
        result = self.llm.generate(prompts, sampling_params)
        output_str = result[0].outputs[0].text
        message = AIMessage(content=output_str)
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])

# FastAPI application
app = FastAPI()

# Endpoints
@app.post("/embed")
async def embed_endpoint(request_data: JsonObjects):
    return await main(request_data)

@app.get("/health")
def health():
    return {"status": "healthy"}

# for route in app.routes:
#     print(route.path, route.methods, route.name)