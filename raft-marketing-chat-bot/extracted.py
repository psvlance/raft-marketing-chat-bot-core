import os
import re
import logging

import openai

import requests

import tiktoken

import telebot

from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma, VectorStore


logger = logging.getLogger(__name__)
API_TOKEN = ''  # https://t.me/raft_test_bot


class GPT:
    GPT_MODEL = "gpt-3.5-turbo"
    GPT_MODEL_SNAP = "gpt-3.5-turbo-0301"
    ENCODING_NAME = "cl100k_base"
    EXPOSED_ENV = "OPENAI_API_KEY"

    def __init__(self, api_key=None):
        openai.api_key = api_key
        self._expose_env(api_key)

    def load_search_indexes(self, urls: [str]) -> VectorStore:
        """
        generate indexes from Google Docs (ppt only)
        """
        text = ""
        for url in urls:
            text += self._load_gcloud_url(url) + "\n\n"
        return self._create_embedding(text)

    # def answer(self, system, topic, temp=1):
    #     """
    #     Answer from LLM GPT
    #     """
    #     messages = [
    #         {"role": "system", "content": system},
    #         {"role": "user", "content": topic},
    #     ]
    #     completion = openai.ChatCompletion.create(model=self.GPT_MODEL, messages=messages, temperature=temp)
    #     return completion.choices[0].message.content

    def answer_index(self, search_index: VectorStore, system: str, topic: str, temperature=1):
        """
        Get partial index on answer
        """
        docs = search_index.similarity_search(topic, k=5)

        message_content = re.sub(
            r"\n{2}",
            " ",
            "\n ".join(
                [
                    f"\nОтрывок документа №{i + 1}\n=====================" + doc.page_content + "\n"
                    for i, doc in
                    enumerate(docs)
                ]
              )
        )
        messages = [
            {"role": "system", "content": system + f"{message_content}"},
            {"role": "user", "content": topic},
        ]

        # logger.debug(self._num_tokens_from_messages(messages=messages, model=self.GPT_MODEL_SNAP))
        completion = openai.ChatCompletion.create(model=self.GPT_MODEL, messages=messages, temperature=temperature)
        self._log_tokens_price(count=completion["usage"]["total_tokens"], factor=0.002)
        answer = self._insert_newlines(text=completion.choices[0].message.content)
        return answer

    @classmethod
    def _insert_newlines(cls, text: str, max_len: int = 170) -> str:
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            if len(current_line + " " + word) > max_len:
                lines.append(current_line)
                current_line = ""
            current_line += " " + word
        lines.append(current_line)
        return "\n".join(lines)

    @classmethod
    def _load_gcloud_url(cls, url: str) -> str:
        # >>> TODO remove unuseful code
        result = re.search('/(document|presentation)/d/([a-zA-Z0-9-_]+)', url)
        if result is None:
            raise ValueError('Invalid Google Docs URL')
        doc_type = result.group(1)
        doc_id = result.group(2)
        # <<< TODO remove unuseful code

        response = requests.get(f'https://docs.google.com/{doc_type}/d/{doc_id}/export?format=txt')
        response.encoding = 'utf-8'
        response.raise_for_status()
        return str(response.text)

    @classmethod
    def _create_embedding(cls, data):
        """ Create LLM GPT embedding from text """

        chunks = []
        splitter = CharacterTextSplitter(separator="\n", chunk_size=1024, chunk_overlap=0)

        for chunk in splitter.split_text(data):
            chunks.append(Document(page_content=chunk, metadata={}))

        index = Chroma.from_documents(chunks, OpenAIEmbeddings(), )

        count = cls._get_tokens_count(' '.join([x.page_content for x in chunks]), cls.ENCODING_NAME)
        cls._log_tokens_price(count)

        return index

    @classmethod
    def _log_tokens_price(cls, count, factor=0.0004):
        logger.debug(f'token`s {count=}, average price {factor * (count / 1000)}$')

    @classmethod
    def _get_tokens_count(cls, text: str, encoding_name: str) -> int:
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(text))
        return num_tokens

    # @classmethod
    # def _num_tokens_from_messages(cls, messages, model=GPT_MODEL_SNAP):
    #     """Returns the number of tokens used by a list of messages."""
    #     try:
    #         encoding = tiktoken.encoding_for_model(model)
    #     except KeyError:
    #         encoding = tiktoken.get_encoding(cls.ENCODING_NAME)
    #     if model == cls.GPT_MODEL_SNAP:  # note: future models may deviate from this
    #         num_tokens = 0
    #         for message in messages:
    #             num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
    #             for key, value in message.items():
    #                 num_tokens += len(encoding.encode(value))
    #                 if key == "name":  # if there's a name, the role is omitted
    #                     num_tokens += -1  # role is always required and always 1 token
    #         num_tokens += 2  # every reply is primed with <im_start>assistant
    #         return num_tokens
    #     else:
    #         raise NotImplementedError(
    #             f"""\
    #             num_tokens_from_messages() is not presently implemented for model {model}.
    #             See https://github.com/openai/openai-python/blob/main/chatml.md
    #             for information on how messages are converted to tokens."""
    #         )

    @classmethod
    def _expose_env(cls, api_key):
        if api_key is not None:
            os.environ[cls.EXPOSED_ENV] = api_key
        elif cls.EXPOSED_ENV not in os.environ:
            raise EnvironmentError(
                "You must either set the OPENAI_API_KEY environment variable or pass an api_key to the constructor"
            )


marketing_urls = [
    'https://docs.google.com/presentation/d/10MFhwdoVfWaAmjH6kPbtpoEl5l2qsZGQ',
    'https://docs.google.com/presentation/d/1aZUl9rLOOIlTKLf1PioltXC5x-nthfiv',
]

marketing_chat_prompt = """\
Ты менеджер поддержки в чате компании, компания продает услуги по разработке программного обеспечения.
У тебя есть большой документ со всеми материалами о продуктах компании.
Тебе задает вопрос клиент в чате, дай ему ответ, опираясь на документ, постарайся ответить так, 
чтобы человек захотел после ответа воспользоваться услугами компании.
Документ с информацией для ответа клиенту: 
"""


bot = telebot.TeleBot(API_TOKEN)


gpt = GPT('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')
marketing_index = gpt.load_search_indexes(marketing_urls)


@bot.message_handler(func=lambda message: True)
def echo_message(message):

    # def answer_index(system, topic, search_index, temp=1):

    answer = gpt.answer_index(system=marketing_chat_prompt, topic=message.text, search_index=marketing_index)
    bot.reply_to(message, answer)


bot.infinity_polling()
