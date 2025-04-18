# Extract the four objectives from the document

# from langchain.retrievers import VectorStoreRetriever
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from modules.vector_store import get_vector_store

import os
from dotenv import load_dotenv
load_dotenv()

# function to extract functional requirements from SRS
def extract_functional_requirements():
    # Load the vector store
    vector_store = get_vector_store()

    # 1. Wrap the vector store retriever in a retriever object
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    # 2. Define the prompt template for our question-answering chain
    template = """
    You are a precise assistant specialized in extracting functional requirements from a Software Requirements Specification (SRS). 
    Given the following context from an SRS document, return **only** a valid JSON object with exactly these four keys:

    1. "endpoints": an array of endpoint objects, each with:
    - "path" (string)
    - "method" (string)
    - "params" (array of strings)
    - "description" (string)

    2. "logic": a concise description of all business rules and computations.

    3. "db_schema": a concise description of the database schema, including table names, relationships, and constraints.

    4. "auth": a concise description of the authentication and authorization requirements.

    Do **not** include any extra keys, commentary, or explanation—output must be pure JSON.
    ***Do not include any extra decorative backtick or quotes in the ends***

    Context:
    {context}
    """

    prompt = PromptTemplate(imput_variables=["context"], template=template)
    # prompt = PromptTemplate.from_template(template=template)

    groqLLM = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.1,
        max_retries=2,
        api_key=os.getenv("GROQ_API_KEY"),
    )

    # 3. Create the retrieval chain with the retriever and the prompt
    qa_chain = RetrievalQA.from_chain_type(
        llm = groqLLM,  # use the custom LLM
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False,
        chain_type_kwargs={"prompt": prompt}
    )

    # 4. Run the chain on the document
    query = "Extract the functional requirements from the document for upcoming project."
    response = qa_chain.run(query)
    print("Here is the requirements from the given SRS docuemt -> \n\n", response)
    return response