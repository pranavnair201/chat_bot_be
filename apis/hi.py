from flask_restful import Resource, request
from flask import make_response
import langchain
from utils.markdown import parser

import re
from utils.error_handler import error_handler
from utils.logger import get_logger
from utils.markdown import parser
from utils.custom_message_placeholder import CustomMessagesPlaceholder
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import chromadb
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory, RedisChatMessageHistory, FileChatMessageHistory
from langchain import LLMChain
from langchain.prompts import MessagesPlaceholder, HumanMessagePromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate


class RetrievalView(Resource):

    @error_handler
    def post(self):
        data = request.get_json()
        if (query := data.get('query', None)) is None:
            return make_response({"status": False, "detail": "query is required"}, 400)
        if (session_id := data.get('session_id', None)) is None:
            return make_response({"status": False, "detail": "session_id is required"}, 400)

        chroma_client = chromadb.HttpClient(host="43.205.120.186", port=8000)
        llm = OpenAI(model='gpt-3.5-turbo-instruct', temperature=0.2)
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

        # memory = FileChatMessageHistory(f"sessions/chat_history_{str(session_id)}.json")
        memory = RedisChatMessageHistory(
            session_id=f"chat_history_{str(session_id)}",
            url="redis://redis_service:6379/0",
        )
        loaded_chat_memory = ConversationBufferMemory(
            chat_memory=memory,
            memory_key="chat_history",
            return_messages=True,
            llm=llm,
        )
        system_history_msg = '''
                The following is a friendly conversation between a Human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says "I'm sorry, but I'm unable to provide an answer to that question at the moment.". Don't give answer as AI.
                '''

        system_query_msg = '''
                Context: {contexts}
                When responding, imagine you are a virtual assistant representing Sculptsoft, a . Provide answers to the below query exclusively based on the above context. Ensure that your response is solely derived from the provided contexts, refraining from generating answers independently.
                '''

        human_query_msg = '''
                Query: {query}
                '''
        system_post_msg = '''
                Answer text should not contain "AI:" or "System:" and answer should be more descriptive. If you don't have answer to the query, kindly state "I'm sorry, but I'm unable to provide an answer to that question at the moment."
                '''
        # chain = load_qa_chain(OpenAI(), chain_type="stuff")

        messages = [
            SystemMessagePromptTemplate.from_template(system_query_msg, partial_variables={"contexts": contexts}),
            HumanMessagePromptTemplate.from_template(human_query_msg),
            SystemMessagePromptTemplate.from_template(system_post_msg)
        ]
        if len(memory.messages) > 0:
            messages.insert(0, CustomMessagesPlaceholder(variable_name="chat_history"))
            messages.insert(0, SystemMessagePromptTemplate.from_template(system_history_msg))
        prompt = ChatPromptTemplate(
            input_variables=['query'],
            messages=messages
        )

        chain = LLMChain(
            llm=llm,
            prompt=prompt,
            memory=loaded_chat_memory,
            verbose=True
        )
        langchain.debug = True
        v = chain({"query": query})
        if (answer := v.get("text", None)) is not None:
            answer = parser(answer=answer)

        logger = get_logger(session_id=session_id)
        logger.info(str({"query": query, "text": answer, "contexts": contexts}))
        return make_response({"status": True, "detail": answer}, 200)

#
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
#         llm = OpenAI(model='gpt-3.5-turbo-instruct', temperature=0.2)
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
#         loaded_chat_memory = ConversationBufferMemory(
#             chat_memory=FileChatMessageHistory(f"sessions/chat_history_{str(session_id)}.json"),
#             # chat_memory=RedisChatMessageHistory(
#             #     session_id=f"chat_history_{str(session_id)}",
#             #     url="redis://redis_service:6379/0",
#             # ),
#             memory_key="chat_history",
#             return_messages=True,
#             llm=llm,
#         )
#
#         system_history_msg = '''
#         The following is a friendly conversation between a Human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says "I'm sorry, but I'm unable to provide an answer to that question at the moment.".
#         '''
#
#         system_query_msg = '''
#         Context: {contexts}
#         When responding, imagine you are a virtual assistant representing Sculptsoft. Provide answers to the below query exclusively based on the above context. Ensure that your response is solely derived from the provided contexts, refraining from generating answers independently.
#         If you don't have answer to the query, kindly state "I'm sorry, but I'm unable to provide an answer to that question at the moment."
#         '''
#
#         human_query_msg = '''
#         Query: {query}
#         '''
#         system_post_msg = '''
#         Answer text should not contain "AI:" or "System:".
#         '''
#         # chain = load_qa_chain(OpenAI(), chain_type="stuff")
#         prompt = ChatPromptTemplate(
#             input_variables=['query'],
#             messages=[
#                 SystemMessagePromptTemplate.from_template(system_history_msg),
#                 MessagesPlaceholder(variable_name="chat_history"),
#                 SystemMessagePromptTemplate.from_template(system_query_msg, partial_variables={"contexts": contexts}),
#                 HumanMessagePromptTemplate.from_template(human_query_msg),
#                 SystemMessagePromptTemplate.from_template(system_post_msg),
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
#         answer = v.get("text", None)
#         # if (answer := v.get("text", None)) is not None:
#         #     link_pattern = re.compile(r'\[(.*?)\]\((.*?)\)')
#         #     results = link_pattern.findall(answer)
#         #     for result in results:
#         #         link_text, url = result
#         #         markdown_link = f'[link]({url})'
#         #         answer = answer.replace(f'[{link_text}]({url})', markdown_link)
#
#         logger = get_logger(session_id=session_id)
#         logger.info(str({"query": query, "text": answer, "contexts": contexts}))
#         return make_response({"status": True, "detail": answer}, 200)


class TimeoutView(Resource):
    @error_handler
    def post(self):
        data = request.get_json()

        if (session_id := data.get('session_id', None)) is None:
            return make_response({"status": False, "detail": "session_id is required"}, 400)

        chat_memory = RedisChatMessageHistory(
            session_id=f"chat_history_{str(session_id)}",
            url="redis://redis_service:6379/0"
        )
        chat_memory.clear()

        return make_response({"status": True, "detail": "Timed out successfully"}, 200)
