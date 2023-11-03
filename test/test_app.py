import textwrap
import openai
import os

from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from CustomRetriever import CustomRetriever
from write_to_md import write_test_to_md

import config


class llm_engine:
    def __init__(self):
        # Initialize the environment variables
        self.setup()
        self.database = self.load_database()
        self.retriever = self.load_retriever(self.database)
        self.llm = self.load_llm()
        self.qa = self.create_search_engine(self.llm, self.retriever)

    def setup(self):
        try:
            load_status = load_dotenv(find_dotenv())
            print(f"load_dotenv: {load_status}/n")
        except Exception as e:
            print(e)
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def load_database(self):
        VECTORDB = 'vectordb'
        embeddings = OpenAIEmbeddings()
        vector_store_dir = f"embeddings/{VECTORDB}/"
        vectordb = Chroma(
            persist_directory=vector_store_dir, embedding_function=embeddings
        )

        return vectordb

    def load_retriever(self, database):
        k = config.SEARCH_DOCUMENTS
        retriever = CustomRetriever(
            vectorstore=database,
            retrieve_type=config.RETRIEVE_TYPE,
            search_type=config.SEARCH_TYPE,
            max_elements=k,
            filter=config.FILTER,
            search_kwargs={"k": k * 10},
        )

        return retriever

    def load_llm(self):
        return ChatOpenAI(model=config.OPENAI_MODEL, temperature=config.TEMPERATURE)

    def create_search_engine(self, llm, retriever):
        template_string = config.TEMPLATE_STRING

        prompt_template = PromptTemplate(
            template=template_string, input_variables=["context", "question"]
        )

        chain_type_kwargs = {"prompt": prompt_template}

        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type=config.CHAIN_TYPE,
            retriever=retriever,
            chain_type_kwargs=chain_type_kwargs,
            return_source_documents=True,
        )
        return qa

    def ask_question(self, question):
        result = self.qa(question)
        return result


# Function to get better output in terminal
def wrap_text_preserve_newlines(text, width=110):
    # Split the input text into lines based on newline characters
    lines = text.split("\n")

    # Wrap each line individually
    wrapped_lines = [textwrap.fill(line, width=width) for line in lines]

    # Join the wrapped lines back together using newline characters
    wrapped_text = "\n".join(wrapped_lines)

    return wrapped_text


# prints response form LLM in terminal
def process_llm_response(llm_response):
    print(wrap_text_preserve_newlines(llm_response["result"]))
    print("\n\nSources:")
    # sort res by each elements metadata["score"] descending
    llm_response["source_documents"] = sorted(
        llm_response["source_documents"], key=lambda x: x.metadata["score"], reverse=True)
    for source in llm_response["source_documents"]:
        print(
            f"{source.metadata['source'].split('/')[-1]} | score: {str(format(source.metadata['score'], '.4f'))} | har_mindretall: {str(source.metadata['har_mindretall'])}"
        )
    print()


def main():
    engine = llm_engine()
    query_list = config.QUERYLIST

    answer_list = []
    for i, q in enumerate(query_list):
        answer = engine.ask_question(q)
        answer_list.append(answer)
        print(f"Test: {i+1}")
        process_llm_response(answer)
    write_test_to_md(config.FILENAME, query_list, answer_list)


if __name__ == "__main__":
    main()
