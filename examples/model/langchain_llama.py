# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import json
from typing import Any, List, Optional

import torch
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.chat_models.base import SimpleChatModel
from langchain.schema import (
    AIMessage,
    BaseMessage,
    ChatMessage,
    HumanMessage,
    SystemMessage,
)
from transformers import AutoTokenizer, LlamaForCausalLM

B_ROUND, E_ROUND = "<s>", "</s>"
B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

SPECIAL_TAGS = [B_INST, E_INST, "<<SYS>>", "<</SYS>>"]
UNSAFE_ERROR = "Error: special tags are not allowed as part of the prompt."


class ChatLlama(SimpleChatModel):
    # read from config.json
    max_context_length: int = 2048
    max_new_tokens: int = 4096
    temperature: float = 0.0
    top_p: float = 1
    top_k: int = 50
    tokenizer: Any
    model: Any

    def __init__(self, model_path):
        super().__init__()

        self.model = LlamaForCausalLM.from_pretrained(
            model_path, torch_dtype=torch.float16, device_map="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        with open(f"{model_path}/config.json") as f:
            config = json.load(f)
        self.max_context_length = config["max_position_embeddings"]

    @property
    def _llm_type(self) -> str:
        return "llama2-chat"

    def _assemble_prompt(self, messages: List[BaseMessage]) -> str:
        prompt = ""
        temp = []
        for message in messages:
            if isinstance(message, ChatMessage):
                role = message.role
            elif isinstance(message, HumanMessage):
                role = "user"
            elif isinstance(message, AIMessage):
                role = "assistant"
            elif isinstance(message, SystemMessage):
                role = "system"
            else:
                raise ValueError(f"Got unknown type {message}")
            temp.append({"role": role, "content": message.content})
        messages = temp
        if messages[0]["role"] == "system":
            messages = [
                {
                    "role": messages[1]["role"],
                    "content": B_SYS
                    + messages[0]["content"]
                    + E_SYS
                    + messages[1]["content"],
                }
            ] + messages[2:]
        assert all([msg["role"] == "user" for msg in messages[::2]]) and all(
            [msg["role"] == "assistant" for msg in messages[1::2]]
        ), (
            "model only supports 'system', 'user' and 'assistant' roles, "
            "starting with 'system', then 'user' and alternating (u/a/u/a/u...)"
        )
        prompts: List[str] = [
            f"{B_ROUND}{B_INST} {(prompt['content']).strip()} {E_INST} {(answer['content']).strip()} {E_ROUND}"
            for prompt, answer in zip(
                messages[::2],
                messages[1::2],
            )
        ]
        prompt = "".join(prompts)
        assert (
            messages[-1]["role"] == "user"
        ), f"Last message must be from user, got {messages[-1]['role']}"
        prompt += f"{B_ROUND}{B_INST} {(messages[-1]['content']).strip()} {E_INST}"
        return prompt

    def _call(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        unsafe = any(
            tag in message.content for message in messages for tag in SPECIAL_TAGS
        )
        if unsafe:
            return UNSAFE_ERROR
        prompt = self._assemble_prompt(messages)

        input_ids = self.tokenizer(
            prompt, return_tensors="pt", add_special_tokens=False
        ).input_ids.to("cuda")
        assert len(input_ids[0]) <= self.max_context_length, (
            f"Prompt is too long, got {len(input_ids[0])} tokens, "
            f"max is {self.max_context_length}"
        )
        generate_input = {
            "input_ids": input_ids,
            "max_new_tokens": self.max_new_tokens,
            "repetition_penalty": 1.0,
            "eos_token_id": self.tokenizer.eos_token_id,
            "bos_token_id": self.tokenizer.bos_token_id,
            "pad_token_id": self.tokenizer.pad_token_id,
        }
        if self.temperature == 0.0:
            generate_input["do_sample"] = False
        else:
            generate_input["do_sample"] = True
            generate_input["temperature"] = self.temperature
            generate_input["top_p"] = self.top_p
            generate_input["top_k"] = self.top_k

        generate_ids = self.model.generate(**generate_input)
        generate_ids = [item[len(input_ids[0]) : -1] for item in generate_ids]
        # output
        output = self.tokenizer.batch_decode(
            generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )[0]
        return output
