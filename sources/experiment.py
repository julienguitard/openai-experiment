import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader, TextLoader
from langchain_community.document_loaders.csv_loader import CSVLoader


from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain


os.environ["OPENAI_API_KEY"] = "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"


loader = WebBaseLoader("https://en.wikipedia.org/wiki/Agglutinative_language")
docs = loader.load()
embeddings = OpenAIEmbeddings(api_key=os.environ["OPENAI_API_KEY"])
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)
llm = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"])
prompt_0 = ChatPromptTemplate.from_messages([
    ("system", "You are world class {field} specialist"),
    ("user", "{input}")
])
output_parser = StrOutputParser()


chain = prompt_0 | llm | output_parser

field = "Agglutinative language lexicography"
input_0 = "Give a list of 10-12 agglutinative language ranked by number of native speakers as a list of wikipedia pages"

response_0 = chain.invoke({"field": field,
                           "input": input_0})


prompt_1 = ChatPromptTemplate.from_template(
    """Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt_1)
retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)
input_1 = "Give a list of dictionaries for the {language} language"

response_1 = retrieval_chain.invoke(
    {"input": input_1.format(language="Finnish")})
print(list(map(lambda x: x.split(' ')[-1], response_0.split('\n'))))
print(response_1["answer"])
