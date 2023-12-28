from flask_restful import Resource, request
from flask import make_response

from utils.error_handler import error_handler
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema.document import Document
import chromadb
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

class RetrievalView(Resource):

    @error_handler
    def post(self):
        data = request.get_json()
        query = data.get('query', None)
        chroma_client = chromadb.HttpClient(host="43.205.120.186", port=8000)
        os.environ["OPENAI_API_KEY"] = "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"
        embeddings = OpenAIEmbeddings()
        db4 = Chroma(
            client=chroma_client,
            collection_name="ss_chatbot",
            embedding_function=embeddings,
        )
        # query = "What speciality does sculptsoft provide in mobile app development"
        results = db4.similarity_search_with_score(query, 5)
        contexts = []
        for res in results:
            print(res)
            contexts.append(res[0])
        print(contexts)

        chain = load_qa_chain(OpenAI(), chain_type="stuff")
        v = chain.run(input_documents=contexts, question=query)
        print('ans ---' + v)
        return make_response({"status": True, "detail": v}, 200)
