from flask_restful import Resource, request
from flask import make_response
import langchain

from utils.error_handler import error_handler
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema.document import Document
import chromadb
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory, FileChatMessageHistory
from langchain import LLMChain, ConversationChain
from langchain.prompts import MessagesPlaceholder, HumanMessagePromptTemplate, ChatPromptTemplate


# class RetrievalView(Resource):
#
#     @error_handler
#     def post(self):
#         data = request.get_json()
#         if (query := data.get('query', None)) is None:
#             return make_response({"status": False, "detail": "query is required"}, 400)
#         if (session_id := data.get('session_id', None)) is None:
#             return make_response({"status": False, "detail": "session_id is required"}, 400)
#
#         chroma_client = chromadb.HttpClient(host="43.205.120.186", port=8000)
#         llm = OpenAI(temperature=0.2)
#         embeddings = OpenAIEmbeddings()
#         db4 = Chroma(
#             client=chroma_client,
#             collection_name="ss_chatbot",
#             embedding_function=embeddings,
#         )
#         # query = "What speciality does sculptsoft provide in mobile app development"
#         results = db4.similarity_search_with_score(query, k=5)
#         contexts = ''
#         for res in results:
#             contexts += res[0].page_content
#
#         # if loaded_chat_memory := ConversationBufferMemory.load_from_file("chat_history.json") is None:
#         loaded_chat_memory = ConversationBufferMemory(
#             chat_memory=FileChatMessageHistory(f"sessions/chat_history_{str(session_id)}.json"),
#             memory_key="chat_history",
#             return_messages=True,
#             llm=llm,
#         )
#
#         # chain = load_qa_chain(OpenAI(), chain_type="stuff")
#         prompt = ChatPromptTemplate(
#             input_variables=['query'],
#             messages=[
#                 MessagesPlaceholder(
#                     variable_name="chat_history"
#                 ),
#                 HumanMessagePromptTemplate.from_template(
#                     "When responding, imagine you are a virtual assistant representing a specialized app development company. Provide answers exclusively based on the given context. In accordance with the provided {contexts}, please reply to the following {query} as if you were this virtual assistant. Ensure that your response is solely derived from the provided contexts, refraining from generating answers independently. If no answer is found, kindly state 'I'm sorry, but I'm unable to provide an answer to that question at the moment. It could be a topic outside my current knowledge or capabilities. If you have another question or need assistance with something else, feel free to ask, and I'll do my best to help!' Strictly adhere to the given contexts and give answers solely from the provided context.",
#                     partial_variables={"contexts": contexts}
#                 ),
#             ]
#         )
#
#         chain = LLMChain(
#             llm=llm,
#             prompt=prompt,
#             memory=loaded_chat_memory,
#             verbose=True
#         )
#         langchain.debug = True
#         v = chain({"query": query})
#         return make_response({"status": True, "detail": v.get("text", None)}, 200)


class RetrievalView(Resource):

    # @error_handler
    def post(self):
        data = request.get_json()
        if (query := data.get('query', None)) is None:
            return make_response({"status": False, "detail": "query is required"}, 400)
        if (session_id := data.get('session_id', None)) is None:
            return make_response({"status": False, "detail": "session_id is required"}, 400)

        chroma_client = chromadb.HttpClient(host="43.205.120.186", port=8000)
        llm = OpenAI(temperature=0.2)
        embeddings = OpenAIEmbeddings()
        db4 = Chroma(
            client=chroma_client,
            collection_name="ss_chatbot",
            embedding_function=embeddings,
        )
        # query = "What speciality does sculptsoft provide in mobile app development"
        results = db4.similarity_search_with_score(query, k=5)
        contexts = ''
        for res in results:
            contexts += res[0].page_content

        # if loaded_chat_memory := ConversationBufferMemory.load_from_file("chat_history.json") is None:
        loaded_chat_memory = ConversationBufferMemory(
            chat_memory=FileChatMessageHistory(f"sessions/chat_history_{str(session_id)}.json"),
            memory_key="chat_history",
            return_messages=True,
            llm=llm,
        )

        # chain = load_qa_chain(OpenAI(), chain_type="stuff")
        prompt = ChatPromptTemplate(
            input_variables=['query'],
            messages=[
                MessagesPlaceholder(
                    variable_name="chat_history"
                ),
                HumanMessagePromptTemplate.from_template(
                    "When responding, imagine you are a virtual assistant representing a specialized app development company. Provide answers exclusively based on the given context. In accordance with the provided {contexts}, please reply to the following {query} as if you were this virtual assistant. Ensure that your response is solely derived from the provided contexts, refraining from generating answers independently. If no answer is found, kindly state 'I'm sorry, but I'm unable to provide an answer to that question at the moment. It could be a topic outside my current knowledge or capabilities. If you have another question or need assistance with something else, feel free to ask, and I'll do my best to help!' Strictly adhere to the given contexts and give answers solely from the provided context.",
                    partial_variables={"contexts": contexts}
                ),
            ]
        )

        chain = LLMChain(
            llm=llm,
            prompt=prompt,
            memory=loaded_chat_memory,
            verbose=True
        )
        langchain.debug = True
        v = chain({"query": query})
        return make_response({"status": True, "detail": v.get("text", None)}, 200)
